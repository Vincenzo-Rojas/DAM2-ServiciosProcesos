import socket
import threading
import sys

dir_server = ("127.0.0.1", 5000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(dir_server)

terminado = False

def main():
    global terminado
    while not terminado:
        try:
            mensaje = sock.recv(1024).decode()
            if "FIN" in mensaje:
                print("El juego ha terminado. Cerrando cliente...")
                break
            print(mensaje)
        except:
            print("Error de lecutura")
        
        try:
            mensaje = input("")
            if mensaje.strip().lower() in ["stop", "quit"]:
                break
            sock.send(mensaje.encode())
        except:
            print("Error durante la escritura")
    

hilo_main = threading.Thread(target=main)

hilo_main.start()

if terminado:
    sock.close()
    print("Cliente cerrado correctamente")
