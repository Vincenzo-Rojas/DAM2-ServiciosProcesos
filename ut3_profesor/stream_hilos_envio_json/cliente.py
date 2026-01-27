'''
Cliente TCP para recibir datos JSON desde un servidor.
Funcionalidad:
- Conecta con un servidor TCP en 127.0.0.1:5000.
- Recibe un mensaje JSON y lo decodifica a un diccionario Python.
- Muestra el contenido del JSON en pantalla.

Posibles fallos:
- No maneja desconexiones inesperadas del servidor.
- El tamaño máximo de recepción está limitado a 1024 bytes.
- No valida el formato del JSON recibido; si el servidor envía datos no válidos, se produce un error.
'''

import json  # Para decodificar mensajes JSON
import socket  # Para crear la conexión TCP

# Dirección del servidor al que se conectará el cliente
direccion_server = ("127.0.0.1", 5000)

# Crear socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectarse al servidor
sock.connect(direccion_server)

# Recibe hasta 1024 bytes del servidor y decodifica JSON
datos_json = json.loads(sock.recv(1024))

# Muestra los datos recibidos
print(datos_json)
