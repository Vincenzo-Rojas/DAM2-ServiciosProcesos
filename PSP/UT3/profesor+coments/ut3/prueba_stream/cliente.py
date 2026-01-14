# Este script implementa un cliente TCP que se conecta a un servidor y solicita la hora actual.
# Funcionalidad:
# - Se conecta al servidor en 127.0.0.1:5000.
# - Envía un mensaje simple ("hola") al servidor.
# - Recibe la hora actual del servidor y la muestra.
# Posibles fallos:
# 1. No hay manejo de errores si el servidor no está disponible.
# 2. Solo funciona con servidores que respondan con la hora al recibir "hola".
# 3. El tamaño máximo de mensaje recibido es de 1024 bytes.
# 4. No hay cierre explícito del socket después de recibir la hora.

import socket  # Para crear y manejar sockets TCP

direccion_server = ("127.0.0.1", 5000)  
# Dirección IP y puerto del servidor al que se conectará

socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# Crea un socket TCP usando IPv4

socket_cliente.connect(direccion_server)  
# Conecta el cliente al servidor

socket_cliente.send("hola".encode())  
# Envía el mensaje "hola" al servidor codificado en bytes

hora = socket_cliente.recv(1024).decode()  
# Recibe hasta 1024 bytes del servidor y los decodifica a string

print(f"La hora actual del servidor es: {hora}")  
# Muestra la hora recibida en consola
