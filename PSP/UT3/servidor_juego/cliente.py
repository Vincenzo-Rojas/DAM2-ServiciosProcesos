import socket
import threading
import sys

# Dirección y puerto del servidor al que se conectará el cliente
dir_server = ("127.0.0.1", 5000)

# Se crea un socket TCP (SOCK_STREAM)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se establece la conexión con el servidor
sock.connect(dir_server)

# Bandera global para indicar que el cliente debe finalizar
terminado = False

def main():
    """
    Hilo principal encargado de:
    - Leer mensajes recibidos del servidor
    - Detectar fin del juego
    - Enviar mensajes escritos por el usuario
    """
    global terminado

    while not terminado:
        # ================================
        # LECTURA DESDE EL SERVIDOR
        # ================================
        try:
            # Recibe mensajes enviados por el servidor (hasta 1024 bytes)
            mensaje = sock.recv(1024).decode()

            # Si el servidor envía la palabra "FIN", el juego termina
            if "FIN" in mensaje:
                print("El juego ha terminado. Cerrando cliente...")
                break

            # Muestra en pantalla el mensaje recibido
            print(mensaje)

        except:
            # Si ocurre un error al leer del socket
            print("Error de lectura")
        
        # ================================
        # ENVÍO HACIA EL SERVIDOR
        # ================================
        try:
            # Lee entrada desde teclado del usuario
            mensaje = input("")

            # Si el usuario escribe "stop" o "quit", se termina el cliente
            if mensaje.strip().lower() in ["stop", "quit"]:
                break

            # Envía el mensaje al servidor codificado en bytes
            sock.send(mensaje.encode())

        except:
            # Error al intentar enviar datos al servidor
            print("Error durante la escritura")
    
# Se crea el hilo de ejecución que gestionará lectura/escritura del socket
hilo_main = threading.Thread(target=main)

# Se inicia el hilo
hilo_main.start()

# Si la variable `terminado` ha cambiado, se cierra el socket
if terminado:
    sock.close()
    print("Cliente cerrado correctamente")
