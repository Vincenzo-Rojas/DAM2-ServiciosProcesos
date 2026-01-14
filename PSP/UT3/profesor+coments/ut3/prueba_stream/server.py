# Este script implementa un servidor TCP que envía la hora actual a los clientes que se conectan.
# Funcionalidad:
# - Escucha en 127.0.0.1:5000.
# - Cada vez que un cliente se conecta, le envía la hora actual y cierra la conexión.
# Posibles fallos:
# 1. No hay manejo de excepciones si ocurre un error en la conexión o envío.
# 2. No hay control de concurrencia; clientes múltiples se atienden secuencialmente.
# 3. No se utiliza un formato de hora estandarizado; solo el formato de datetime.time.
# 4. El servidor imprime la hora en consola cada conexión, lo que podría ser innecesario.

import socket  # Para crear y manejar sockets TCP
from datetime import datetime  # Para obtener la fecha y hora actual

direccion = ("127.0.0.1", 5000)  
# Dirección IP y puerto donde el servidor escuchará

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# Crea un socket TCP usando IPv4

socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
# Permite reutilizar la dirección inmediatamente

socket_server.bind(direccion)  
# Asocia el socket a la dirección y puerto definidos

socket_server.listen()  
# Pone el socket en modo escucha para aceptar conexiones entrantes

print(datetime.now().time())  
# Muestra en consola la hora actual al iniciar el servidor

while True:
    cliente, address_cliente = socket_server.accept()  
    # Espera una nueva conexión y obtiene el socket del cliente y su dirección

    print(address_cliente)  
    # Muestra la dirección del cliente que se conectó

    hora = datetime.now().time()  
    # Obtiene la hora actual

    print(hora)  
    # Muestra la hora actual en consola

    cliente.send(f"{hora}".encode())  
    # Envía la hora al cliente codificada en bytes

    cliente.close()  
    # Cierra la conexión con el cliente
