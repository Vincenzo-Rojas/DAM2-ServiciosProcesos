'''
Servidor TCP para enviar la hora actual a clientes.
Funcionalidad:
- Escucha conexiones TCP en 127.0.0.1:5000.
- Para cada cliente, envía la hora actual como string.
- Maneja múltiples clientes simultáneamente mediante hilos.

Posibles fallos:
- No valida que la hora se haya enviado correctamente antes de cerrar la conexión.
- No maneja desconexiones inesperadas del cliente.
- El formato de la hora es el que devuelve datetime.time(), no es un estándar NTP.
'''

from threading import Thread  # Para manejar múltiples clientes simultáneamente
from datetime import datetime  # Para obtener la hora actual
import socket  # Para manejar sockets TCP

def peticion(sock_cliente, dir_cliente):
    """
    Función que maneja cada cliente.
    Parámetros:
    - sock_cliente: socket del cliente
    - dir_cliente: dirección IP y puerto del cliente
    """
    hora = datetime.now().time()  # Obtiene la hora actual
    sock_cliente.send(f"{hora}".encode())  # Envía la hora al cliente
    print(f"Cliente: {dir_cliente} servido")  # Mensaje de log en el servidor
    sock_cliente.close()  # Cierra la conexión con el cliente

# Configuración del servidor
direccion = ("127.0.0.1", 5000)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea socket TCP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reutilizar la dirección
sock.bind(direccion)  # Asocia el socket con la dirección y puerto
sock.listen()  # Pone el socket en modo escucha
print(f"Servidor NTP escuchando en {direccion}...")  # Mensaje de estado

# Bucle principal para aceptar clientes
while True:
    cliente, direccion = sock.accept()  # Espera y acepta conexión de un cliente
    Thread(target=peticion, args=(cliente, direccion)).start()  
    # Crea un hilo para atender al cliente simultáneamente
