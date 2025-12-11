# Este script implementa un servidor TCP que recibe comandos JSON de clientes y ejecuta acciones específicas.
# Funcionalidad:
# - Escucha en 127.0.0.1:5000.
# - Soporta comandos validados en la lista valid_comms.
# - Ejecuta el comando "listar" en bash y devuelve la salida al cliente en formato JSON.
# Posibles fallos:
# 1. No hay validación de seguridad: ejecutar comandos con subprocess puede ser peligroso.
# 2. Solo soporta el comando "listar" por ahora; otros generan un error impreso en consola.
# 3. Tamaño máximo de mensaje de 1024 bytes; mensajes más grandes se truncarán.
# 4. No hay manejo de excepciones para errores de conexión o datos corruptos.
# 5. Cada cliente se maneja en un hilo, pero no hay límite de clientes concurrentes.

import socket  # Para crear y manejar sockets TCP
import json  # Para codificar y decodificar datos JSON
import subprocess  # Para ejecutar comandos del sistema
from datetime import datetime  # Importado pero no usado en el script
from threading import Thread  # Para manejar hilos concurrentes
import time  # Importado pero no usado

valid_comms = ["listar", "crear_f"]  
# Lista de comandos válidos que el servidor puede procesar

dir_server = ("127.0.0.1", 5000)  
# Dirección IP y puerto donde el servidor escuchará

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# Crea un socket TCP usando IPv4

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
# Permite reutilizar la dirección inmediatamente después de cerrar el servidor

sock.bind(dir_server)  
# Asocia el socket a la dirección y puerto definidos

sock.listen(5)  
# Pone el socket en modo escucha, con cola de hasta 5 conexiones pendientes

def listar():
    # Ejecuta el comando "ls" en bash y devuelve la salida en un diccionario JSON
    p = subprocess.run(["bash", "-c", "ls"], capture_output=True, text=True)
    # Ejecuta el comando y captura la salida y errores como texto
    print(type(p.stderr), p.stderr)  
    # Muestra el tipo y contenido de stderr (para depuración)
    resultado = {"res": p.stdout, "status": "OK"}  
    # Crea un diccionario con el resultado y estado
    return resultado

def petition_handler(cliente, direccion):
    # Maneja la petición de un cliente
    respuesta_json = {"res": "", "status": ""}  
    # Diccionario de respuesta por defecto
    mensaje_comando = cliente.recv(1024)  
    # Recibe hasta 1024 bytes del cliente
    if mensaje_comando:
        comando_json = json.loads(mensaje_comando)  
        # Decodifica el mensaje JSON a diccionario
        if comando_json["comm"] not in valid_comms:
            # Comando no válido
            respuesta_json["status"] = f"ERROR: No existe el comando [{comando_json['comm']}]"
            respuesta_texto = json.dumps(respuesta_json)  
            # Convierte la respuesta a JSON
            cliente.send(respuesta_texto.encode())  
            # Envía la respuesta al cliente
        else:
            res = ""
            match comando_json["comm"]:
                case "listar":
                    res = listar()  
                    # Ejecuta el comando "listar"
                case _:
                    print("error")  
                    # Mensaje de error en consola si se recibe comando inesperado
            cliente.send(json.dumps(res).encode())  
            # Envía el resultado al cliente
    cliente.close()  
    # Cierra la conexión con el cliente

while True:
    cliente, direccion = sock.accept()  
    # Espera una nueva conexión de cliente
    Thread(target=petition_handler, args=(cliente, direccion)).start()  
    # Crea un hilo para manejar la petición de este cliente
