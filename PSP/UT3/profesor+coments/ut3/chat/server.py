# Este script implementa un servidor UDP que escucha en 127.0.0.1:3000.
# Recibe mensajes de clientes, los muestra por consola y permite responder.
# Posibles fallos:
# 1. No hay manejo de excepciones: si ocurre un error de red, el servidor se cierra.
# 2. Bucle infinito sin forma de salir salvo con Ctrl+C.
# 3. No hay validación del contenido recibido ni límites de tamaño de mensaje.
# 4. Se asume que la respuesta del usuario siempre será enviada correctamente.

import socket  # Importa el módulo para trabajar con sockets

direccion = ("127.0.0.1", 3000)  
# Define la dirección IP y puerto donde el servidor escuchará

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Crea un socket UDP usando IPv4
server.bind(direccion)  
# Asocia el socket a la dirección y puerto definidos para recibir mensajes

while True:  
    # Bucle infinito para mantener al servidor activo
    data, address = server.recvfrom(1024)  
    # Espera recibir datos de algún cliente (máximo 1024 bytes)
    # 'address' contiene la dirección IP y puerto del cliente que envió el mensaje

    datos = data.decode()  
    # Decodifica los datos recibidos de bytes a string

    print(f"El cliente[{address}] ha mandado:", datos)  
    # Muestra por consola la dirección del cliente y el mensaje recibido

    texto = input("Ingresa tu respuesta:\t")  
    # Solicita al usuario del servidor que ingrese un mensaje de respuesta

    server.sendto(texto.encode(), address)  
    # Envía la respuesta codificada al cliente desde el que se recibió el mensaje
