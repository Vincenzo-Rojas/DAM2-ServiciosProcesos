'''
Cliente TCP para recibir la hora desde un servidor.
Funcionalidad:
- Conecta con un servidor TCP en 127.0.0.1:5000.
- Recibe la hora enviada por el servidor como string.
- Muestra la hora en pantalla.

Posibles fallos:
- No maneja desconexiones inesperadas del servidor.
- El tamaño máximo de recepción está limitado a 1024 bytes.
- No valida el formato del mensaje recibido; si el servidor envía datos inesperados, puede fallar.
'''

import socket  # Para crear la conexión TCP

# Dirección y puerto del servidor
direccion_server = ("127.0.0.1", 5000)

# Crear socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectarse al servidor
sock.connect(direccion_server)

# Recibe hasta 1024 bytes del servidor y decodifica como string
hora = sock.recv(1024).decode()

# Muestra la hora recibida
print(hora)
