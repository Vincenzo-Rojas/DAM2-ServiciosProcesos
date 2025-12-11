# Este script implementa un cliente TCP que se conecta a un servidor en 127.0.0.1:5000.
# Permite enviar y recibir mensajes de manera simultánea usando hilos.
# Posibles fallos:
# 1. No hay reconexión si el servidor cae.
# 2. Si el servidor cierra la conexión inesperadamente, el programa puede terminar abruptamente.
# 3. No hay límite de tamaño de mensajes ni control de flujo.
# 4. No hay manejo de mensajes largos que superen 1024 bytes.

import socket  # Importa el módulo para trabajar con sockets
import threading  # Importa el módulo para manejar hilos de ejecución
import sys  # Importa el módulo sys (aunque no se usa en este script)

dir_server = ("127.0.0.1", 5000)  
# Define la dirección IP y puerto del servidor TCP

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# Crea un socket TCP usando IPv4

sock.connect(dir_server)  
# Se conecta al servidor en la dirección definida

parar = False  
# Variable global para indicar cuándo detener los hilos

def leer():
    # Función que lee mensajes del servidor de forma continua
    global parar
    while not parar:  
        # Mientras no se indique parar
        try:
            mensaje = sock.recv(1024).decode()  
            # Recibe hasta 1024 bytes y los decodifica a string
            print(mensaje)  
            # Muestra el mensaje recibido por consola
        except Exception as e:
            print(f"Ha habido un problema leyendo: {e}")  
            # Muestra el error ocurrido al recibir datos
            parar = True  
            # Marca que los hilos deben parar

def escribir():
    # Función que envía mensajes al servidor de forma continua
    global parar
    while not parar:  
        # Mientras no se indique parar
        try:
            mensaje = input("")  
            # Solicita mensaje al usuario
            if mensaje.strip().lower() in ["stop", "quit"]:  
                # Si el mensaje es 'stop' o 'quit' (ignorando mayúsculas y espacios)
                sock.close()  
                # Cierra el socket
                parar = True  
                # Señala a los hilos que deben detenerse
            else:
                sock.send(mensaje.encode())  
                # Envía el mensaje codificado al servidor
        except Exception as e:
            print(f"Ha habido un problema escribiendo: {e}")  
            # Muestra el error ocurrido al enviar datos
            parar = True  
            # Señala a los hilos que deben detenerse

hilo_leer = threading.Thread(target=leer)  
# Crea un hilo para ejecutar la función leer

hilo_escribir = threading.Thread(target=escribir)  
# Crea un hilo para ejecutar la función escribir

hilo_leer.start()  
# Inicia el hilo de lectura

hilo_escribir.start()  
# Inicia el hilo de escritura
