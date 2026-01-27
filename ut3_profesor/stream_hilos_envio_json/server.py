'''
Servidor TCP para enviar bromas a clientes.
Funcionalidad:
- Escucha conexiones TCP en 127.0.0.1:5000.
- Para cada cliente, realiza una petición a la API "https://icanhazdadjoke.com/" para obtener una broma.
- Envía un JSON con la dirección del cliente al cliente conectado y cierra la conexión.
- Maneja múltiples clientes simultáneamente con hilos.

Posibles fallos:
- La variable json_datos está vacía, por lo que nunca se procesa correctamente la broma.
- No se valida la respuesta HTTP; si la API falla, el cliente no recibe la broma.
- No hay manejo de desconexión del cliente ni errores de socket.
- La broma real no se envía al cliente, solo se envía la dirección.
- Bloquea el hilo mientras espera la respuesta de la API.
'''

import json  # Para codificar y decodificar mensajes JSON
import socket  # Para manejo de sockets TCP
import requests  # Para hacer peticiones HTTP a la API de bromas
from threading import Thread  # Para manejar múltiples clientes simultáneamente

def bromita(cliente, dir_cliente):
    """
    Función que maneja cada cliente.
    Parámetros:
    - cliente: socket del cliente
    - dir_cliente: dirección IP y puerto del cliente
    """
    # Hace una petición HTTP a la API de bromas
    datos = requests.get("https://icanhazdadjoke.com/", json=True)
    json_datos = ""  # ERROR: debería decodificar datos.text o usar datos.json()
    if "joke" in json_datos:  # Intenta obtener la broma
        broma = json_datos["joke"]
        print(broma)  # Imprime la broma en el servidor
    else:
        print("Ha habido un error en la petición")  # Mensaje de error si falla

    # Prepara los datos a enviar al cliente
    datos_envio = {
        "direccion_cliente" : dir_cliente  # Envía la dirección del cliente (no la broma)
    }
    json_envio = json.dumps(datos_envio)  # Codifica a JSON
    cliente.send(json_envio.encode())  # Envía los datos al cliente
    cliente.close()  # Cierra la conexión con el cliente

# Configuración del servidor
direccion = ("127.0.0.1", 5000)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea socket TCP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reutilizar la dirección
sock.bind(direccion)  # Asocia el socket con la dirección y puerto
sock.listen()  # Pone el socket en modo escucha
print(f"SERVER BROMITAS ESCUCHANDO EN {direccion}")  # Mensaje de estado

# Bucle principal para aceptar clientes
while True:
    cliente, dir_cliente = sock.accept()  # Espera y acepta conexión de un cliente
    Thread(target=bromita, args=(cliente, dir_cliente)).start()  
    # Crea un hilo para manejar al cliente simultáneamente
