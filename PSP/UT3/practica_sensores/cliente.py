import socket
import json
import time
from datetime import datetime

FREC_ENVIO = 25 #ENVIO CADA 25 SEGUNDOS
DIR_SERVER = ("127.0.0.1", 5000)


def set_frec(valor):
    global FREC_ENVIO
    try:
        FREC_ENVIO = int(valor)
        print(f"Nueva frecuencia establecida por servidor: {FREC_ENVIO}")
    except Exception as e:
        print(f"Error durante el cambio de frecuencia: {e}")

def enviar(json_envio) -> bool:
    try:
        sock.send(json.dumps(json_envio).encode())
    except Exception as e:
        print(f"Error al enviar: {e}")
        return False
    return True

def enviar_datos(cliente, tipo, valor) -> bool:
    json_envio = {
        "sensor_id": {
            "ip": cliente.getsockname()[0],
            "puerto": cliente.getsockname()[1],
            "fd": cliente.fileno()
        },
        "fecha": datetime.now().isoformat(),
        "tipo": tipo,
        "valor": valor
    }
    return enviar(json_envio)

def recibir(cliente):
    """
    Recibe un mensaje JSON desde el servidor, lo decodifica. 
    Devuelve el diccionario resultadante.
    Si ocurre un error o se reciben datos vacíos,devuelve None.
    """
    try:
        data = sock.recv(1024)
        if not data:
            print("No hay datos recibidos")
            return None
        return json.loads(data.decode())
    except Exception as e:
        print(f"Error al recibir/parsear respuesta: {e}")
        return None

def envio(cliente, tipo, valor):
    tipo = input("Tipo de sensor: ")
    valor = input("Valor inicial: ")
    respuesta = None
    fin = False

    while not fin:
        # Enviar datos
        enviado = enviar_datos(sock, tipo, valor)

        if not enviado:
            print("Fallo al enviar, reintentando...")
            time.sleep(1)
        else:
            # Recibir respuesta
            respuesta = recibir(sock)

            if respuesta is None:
                print("Respuesta inválida, reintentando...")
                time.sleep(1)
            else:
                # Procesar comandos del servidor
                if respuesta.get("res") == "OK":
                    time.sleep(FREC_ENVIO)
                elif respuesta.get("res") == "SET_FREC":
                    set_frec(respuesta["valor"])
                elif respuesta.get("res") == "FIN":
                    print("Servidor ordenó FIN. Terminando envío.")
                    fin = True
                else:
                    print("Servidor devolvió error, reintentando...")

def menu():
    print("""
        ---------- MENU -------------
          1 - Iniciar sensor
          2 - Ajustar tiempo de envio
          3 - Terminar programa
    """)
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(DIR_SERVER)
    fin = False
    while not fin:
        menu()
        op = input("Elige una opcion")

        match(op):
            case 1:
                envio(sock)
            case 2:
                set_frec(input("Dime la nueva frecuencia de muestras del sensor en segundos"))
            case 3:
                fin = True

if __name__ == "__main__":
    main()