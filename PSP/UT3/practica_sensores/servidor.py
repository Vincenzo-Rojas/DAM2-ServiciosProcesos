# --------------------------------------------------------------------------------
# Cliente TCP para enviar datos simulados de sensores a un servidor
# Qué hace:
# - Simula sensores de temperatura y humedad.
# - Envía sus datos a un servidor TCP en localhost:6000.
# - Calcula un checksum MD5 de los datos para verificar integridad.
# - Usa framing: primero envía la longitud del mensaje, luego el JSON.
# - Reintenta el envío hasta 3 veces si hay errores.
# Fallos posibles:
# - No maneja desconexiones inesperadas del servidor más allá de los reintentos.
# - Solo funciona con servidores que esperen framing de 4 bytes + JSON.
# - No valida la respuesta del servidor más allá de decodificar JSON.
# --------------------------------------------------------------------------------

# Importamos la librería 'socket' para manejar conexiones TCP/IP con el servidor
import socket

# Importamos 'json' para poder convertir diccionarios de Python a JSON y viceversa
import json

# Importamos 'time' para obtener timestamps y pausas en la ejecución
import time

# Importamos 'hashlib' para calcular checksums (MD5) de los datos enviados
import hashlib

# Importamos 'random' para generar valores simulados de sensores
import random

# Definimos la dirección IP del servidor al que se conectará el cliente
HOST = "127.0.0.1"  # localhost, servidor en la misma máquina
# Definimos el puerto TCP donde escucha el servidor
PORT = 6000
# Número máximo de intentos de envío por mensaje en caso de error
INTENTO_MAX = 3

# --------------------------------------------------------------------------------
# Función para calcular un checksum MD5 de un diccionario
# Sirve para verificar que los datos no se han modificado durante el envío
# --------------------------------------------------------------------------------
def calcular_checksum(data_dict):
    # Convertimos el diccionario a una cadena JSON con claves ordenadas
    cadena = json.dumps(data_dict, sort_keys=True)
    # Calculamos y devolvemos el hash MD5 de la cadena codificada en bytes
    return hashlib.md5(cadena.encode()).hexdigest()

# --------------------------------------------------------------------------------
# Función que envía los datos de un sensor al servidor
# Parámetros:
# - sensor_id: identificador único del sensor
# - tipo: tipo de sensor ('temperatura', 'humedad', etc.)
# - valor: valor numérico medido por el sensor
# Qué hace:
# - Incluye un checksum para verificar integridad
# - Usa framing (envía la longitud del mensaje antes del JSON)
# - Reintenta en caso de fallo de conexión
# - Procesa la respuesta del servidor
# --------------------------------------------------------------------------------
def enviar_datos(sensor_id, tipo, valor):
    intento = 0  # Contador de intentos de envío
    enviado = False  # Indicador de si el mensaje fue enviado con éxito

    # Bucle que reintenta enviar el mensaje hasta INTENTO_MAX veces
    while intento < INTENTO_MAX and not enviado:
        intento += 1  # Aumentamos el contador de intentos
        try:
            # Creamos un socket TCP (SOCK_STREAM)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Establecemos un timeout de 5 segundos para evitar bloqueo indefinido
            s.settimeout(5)
            # Conectamos el socket al servidor
            s.connect((HOST, PORT))

            # Construimos el diccionario de datos del sensor
            data = {
                "sensor_id": sensor_id,      # Identificador del sensor
                "timestamp": time.time(),    # Momento en que se tomó la lectura
                "tipo": tipo,                # Tipo de sensor
                "valor": valor               # Valor medido
            }
            # Calculamos el checksum y lo añadimos al diccionario
            data["checksum"] = calcular_checksum(data)

            # Convertimos el diccionario a bytes usando JSON
            mensaje_bytes = json.dumps(data).encode()
            # Calculamos la longitud del mensaje en bytes
            longitud = len(mensaje_bytes)
            # Enviamos primero la longitud (4 bytes, big-endian) y luego el JSON
            s.sendall(longitud.to_bytes(4, "big") + mensaje_bytes)

            # ---------- Recepción de la respuesta del servidor ----------
            # Leemos los primeros 4 bytes, que indican la longitud del mensaje
            header = s.recv(4)
            # Si no recibimos 4 bytes completos, algo salió mal
            if not header or len(header) < 4:
                print("Error: no se recibió header de respuesta")
                s.close()
                continue  # Volvemos a intentar el envío

            # Convertimos los 4 bytes a un número entero (longitud del JSON)
            longitud_res = int.from_bytes(header, "big")
            recibido = b""  # Buffer donde almacenaremos los bytes recibidos

            # Bucle para leer todos los bytes del mensaje según la longitud
            while len(recibido) < longitud_res:
                paquete = s.recv(longitud_res - len(recibido))
                if not paquete:  # Si no recibimos más datos, salimos
                    break
                recibido += paquete

            # Intentamos decodificar el JSON recibido
            try:
                respuesta = json.loads(recibido.decode())
                print(f"Servidor respondió: {respuesta}")
                enviado = True  # Si llegó la respuesta correctamente, terminamos el bucle
            except json.JSONDecodeError:
                # Si el JSON está malformado, mostramos mensaje de error
                print("Error: JSON de respuesta malformado")

            # Cerramos el socket después de enviar y recibir
            s.close()

        # Si ocurre un timeout en la conexión, mostramos mensaje y reintentamos
        except socket.timeout:
            print("Timeout en conexión, reintentando...")

        # Si hay algún error de socket, mostramos el error y reintentamos
        except socket.error as e:
            print(f"Error de socket: {e}, reintentando...")

        # Capturamos cualquier otra excepción desconocida
        except Exception as e:
            print(f"Excepción desconocida: {e}")

# --------------------------------------------------------------------------------
# BLOQUE PRINCIPAL
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    # Lista de sensores simulados: ID y tipo
    sensores = [("S1", "temperatura"), ("S2", "humedad")]

    # Bucle que envía datos para cada sensor
    for sensor_id, tipo in sensores:
        # Generamos un valor aleatorio para el sensor
        # Temperatura: 20-30, Humedad: 30-70
        valor = random.uniform(20, 30) if tipo == "temperatura" else random.uniform(30, 70)
        # Llamamos a la función para enviar los datos
        enviar_datos(sensor_id, tipo, valor)
        # Esperamos 1 segundo antes de enviar el siguiente sensor
        time.sleep(1)
