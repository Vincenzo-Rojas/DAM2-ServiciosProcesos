import socket
import json
import time
import hashlib
import random

HOST = "127.0.0.1"
PORT = 6000
INTENTO_MAX = 3  # número máximo de reintentos por envío


def calcular_checksum(data_dict):
    """Calcula un checksum MD5 del diccionario JSON"""
    cadena = json.dumps(data_dict, sort_keys=True)
    return hashlib.md5(cadena.encode()).hexdigest()


def enviar_datos(sensor_id, tipo, valor):
    """
    Envía datos de un sensor al servidor:
    - Incluye checksum
    - Usa framing (longitud + JSON)
    - Reintenta en caso de error
    - Procesa la respuesta del servidor
    """
    intento = 0
    enviado = False
    while intento < INTENTO_MAX and not enviado:
        intento += 1
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)  # timeout de conexión
            s.connect((HOST, PORT))

            data = {
                "sensor_id": sensor_id,
                "timestamp": time.time(),
                "tipo": tipo,
                "valor": valor
            }
            data["checksum"] = calcular_checksum(data)

            # Framing: enviar longitud antes del mensaje
            mensaje_bytes = json.dumps(data).encode()
            longitud = len(mensaje_bytes)
            s.sendall(longitud.to_bytes(4, "big") + mensaje_bytes)

            # Recibir respuesta del servidor
            header = s.recv(4)
            if not header or len(header) < 4:
                print("Error: no se recibió header de respuesta")
                s.close()
                continue

            longitud_res = int.from_bytes(header, "big")
            recibido = b""
            while len(recibido) < longitud_res:
                paquete = s.recv(longitud_res - len(recibido))
                if not paquete:
                    break
                recibido += paquete

            try:
                respuesta = json.loads(recibido.decode())
                print(f"Servidor respondió: {respuesta}")
                enviado = True
            except json.JSONDecodeError:
                print("Error: JSON de respuesta malformado")

            s.close()
        except socket.timeout:
            print("Timeout en conexión, reintentando...")
        except socket.error as e:
            print(f"Error de socket: {e}, reintentando...")
        except Exception as e:
            print(f"Excepción desconocida: {e}")


if __name__ == "__main__":
    # Simulación de envío de sensores
    sensores = [("S1", "temperatura"), ("S2", "humedad")]
    for sensor_id, tipo in sensores:
        # Genera valores aleatorios para la simulación
        valor = random.uniform(20, 30) if tipo == "temperatura" else random.uniform(30, 70)
        enviar_datos(sensor_id, tipo, valor)
        time.sleep(1)  # espera 1 segundo entre envíos
