# Este script implementa un cliente UDP que se conecta a un servidor en la dirección 127.0.0.1 y puerto 3000.
# Permite enviar mensajes al servidor y recibir respuestas. 
# Posibles fallos:
# 1. No hay manejo de excepciones: si el servidor no está disponible, el programa fallará.
# 2. No hay límite de mensajes ni posibilidad de salir del bucle salvo con Ctrl+C.
# 3. No se valida que el texto ingresado no esté vacío.
# 4. Se asume que la respuesta del servidor siempre cabe en 1024 bytes.

import socket  # Importa el módulo para trabajar con sockets de red

dir_server = ("127.0.0.1", 3000)  
# Define la dirección IP y el puerto del servidor al que se enviarán los mensajes.

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
# Crea un socket UDP (SOCK_DGRAM) usando IPv4 (AF_INET).

while True:  
    # Bucle infinito que permite enviar mensajes de manera continua
    texto = input("Escribe tu mensaje:\t")  
    # Solicita al usuario que ingrese un mensaje por consola

    cliente.sendto(texto.encode(), dir_server)  
    # Envía el mensaje codificado en bytes al servidor UDP especificado

    respuesta, _ = cliente.recvfrom(1024)  
    # Espera recibir una respuesta del servidor (máximo 1024 bytes)
    # El segundo valor (_) contiene la dirección del servidor que envió el mensaje, pero aquí no se usa

    print("SERVIDOR:", respuesta.decode())  
    # Decodifica la respuesta recibida y la muestra en consola
