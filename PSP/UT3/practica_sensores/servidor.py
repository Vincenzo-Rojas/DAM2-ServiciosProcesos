import socket
import threading
import json
import time
import hashlib
import queue
import logging
import os

# Configuración de logging: crea un archivo server.log y registra mensajes con timestamps
logging.basicConfig(filename="server.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Archivo donde se guardarán los datos persistentes de los sensores
ARCHIVO_SENSORES = "sensores.json"

# Carga inicial de datos si ya existe el archivo, sino crea un diccionario vacío
if os.path.exists(ARCHIVO_SENSORES):
    with open(ARCHIVO_SENSORES, "r") as f:
        sensores = json.load(f)
else:
    sensores = {}

# Lock para proteger acceso concurrente a la estructura de sensores
lock_sensores = threading.Lock()

# Cola para almacenar mensajes entrantes y procesarlos en orden
cola_mensajes = queue.Queue()


# ---------- FUNCIONES AUXILIARES ----------

def calcular_checksum(data_dict):
    """Calcula un checksum MD5 del contenido de un diccionario JSON"""
    cadena = json.dumps(data_dict, sort_keys=True)  # ordenar para consistencia
    return hashlib.md5(cadena.encode()).hexdigest()


def validar_json(data):
    """
    Valida que el JSON tenga todos los campos, rangos correctos,
    timestamp coherente y checksum válido.
    """
    campos_obligatorios = ["sensor_id", "timestamp", "tipo", "valor", "checksum"]
    for campo in campos_obligatorios:
        if campo not in data:
            return False, f"Falta campo: {campo}"

    # Validación de checksum
    checksum_recibido = data["checksum"]
    copia = data.copy()
    copia.pop("checksum")
    if calcular_checksum(copia) != checksum_recibido:
        return False, "Checksum inválido"

    # Validación de rangos según tipo de sensor
    tipo = data["tipo"]
    valor = data["valor"]
    timestamp = data["timestamp"]
    if tipo == "temperatura" and not (-50 <= valor <= 100):
        return False, "Valor fuera de rango para temperatura"
    if tipo == "humedad" and not (0 <= valor <= 100):
        return False, "Valor fuera de rango para humedad"

    # Timestamp no puede estar en el futuro (+5s de tolerancia)
    if timestamp > time.time() + 5:
        return False, "Timestamp futuro no permitido"

    return True, "ok"


def guardar_sensores():
    """Guarda los datos de sensores en un archivo JSON para persistencia"""
    try:
        with lock_sensores:
            with open(ARCHIVO_SENSORES, "w") as f:
                json.dump(sensores, f)
    except Exception as e:
        logging.error(f"Error guardando sensores: {e}")


def procesar_mensajes():
    """
    Hilo que procesa mensajes de la cola.
    Extrae mensajes, valida, detecta duplicados y guarda los datos.
    """
    while True:
        mensaje, conn = cola_mensajes.get()  # obtiene un mensaje de la cola
        try:
            valido, mensaje_validacion = validar_json(mensaje)
            if valido:
                sensor_id = mensaje["sensor_id"]
                timestamp = mensaje["timestamp"]

                with lock_sensores:
                    id_timestamp = f"{sensor_id}_{timestamp}"
                    if id_timestamp not in sensores:
                        # Guardar datos válidos y persistir
                        sensores[id_timestamp] = mensaje
                        guardar_sensores()
                        respuesta = {"status": "ok", "mensaje": "Datos recibidos"}
                        logging.info(f"Sensor {sensor_id}: datos aceptados")
                    else:
                        respuesta = {"status": "error", "mensaje": "Duplicado detectado"}
                        logging.warning(f"Sensor {sensor_id}: mensaje duplicado")
            else:
                # JSON inválido
                respuesta = {"status": "error", "mensaje": mensaje_validacion}
                logging.warning(f"Validación fallida: {mensaje_validacion}")

            enviar_respuesta(conn, respuesta)
        except Exception as e:
            logging.error(f"Error procesando mensaje: {e}")
            try:
                enviar_respuesta(conn, {"status": "error", "mensaje": str(e)})
            except:
                pass  # si falla el envío, se ignora


def enviar_respuesta(conn, respuesta):
    """
    Envía un JSON al cliente usando framing:
    primero se envía 4 bytes con la longitud, luego el JSON.
    Esto permite que el cliente sepa cuánto leer.
    """
    try:
        mensaje_bytes = json.dumps(respuesta).encode()
        longitud = len(mensaje_bytes)
        conn.sendall(longitud.to_bytes(4, "big") + mensaje_bytes)
    except Exception as e:
        logging.error(f"Error enviando respuesta: {e}")


def manejar_cliente(conn, addr):
    """
    Hilo que recibe datos de un cliente.
    - Recibe el tamaño del mensaje (4 bytes)
    - Recibe el mensaje completo según la longitud
    - Pone el mensaje en la cola para procesarlo
    """
    while True:
        try:
            # Leer longitud del mensaje
            header = conn.recv(4)
            if not header or len(header) < 4:
                return  # cliente desconectado
            longitud = int.from_bytes(header, "big")

            # Leer el mensaje completo
            recibido = b""
            while len(recibido) < longitud:
                paquete = conn.recv(longitud - len(recibido))
                if not paquete:
                    return
                recibido += paquete

            try:
                data = json.loads(recibido.decode())
                cola_mensajes.put((data, conn))  # poner en la cola para procesar
            except json.JSONDecodeError:
                respuesta = {"status": "error", "mensaje": "JSON malformado"}
                enviar_respuesta(conn, respuesta)
                logging.warning(f"JSON malformado recibido de {addr}")
        except socket.error:
            return  # desconexión o error de socket
        except Exception as e:
            logging.error(f"Excepción cliente {addr}: {e}")
            return


def servidor(host="0.0.0.0", port=6000):
    """Función principal del servidor"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(10)
    logging.info(f"Servidor de sensores escuchando en {host}:{port}")

    # Hilo de procesamiento de cola
    threading.Thread(target=procesar_mensajes, daemon=True).start()

    while True:
        try:
            conn, addr = s.accept()
            # Crear un hilo por cliente
            threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True).start()
        except Exception as e:
            logging.error(f"Error aceptando cliente: {e}")


if __name__ == "__main__":
    servidor()
