'''
Servidor TCP para gestión de archivos.
Funcionalidad:
- Acepta conexiones de múltiples clientes simultáneamente (hilos).
- Recibe comandos JSON del cliente: listar directorios, descargar archivos, finalizar sesión.
- Envía respuestas en JSON para listar o estado de descarga, y envía bytes para archivos.
Posibles fallos:
- No hay validación de seguridad de rutas; un cliente podría intentar acceder a archivos sensibles.
- Los archivos grandes podrían saturar la memoria si no se leen en bloques correctamente.
- La desconexión inesperada de un cliente no siempre se maneja de forma robusta.
- No hay límite en el número de clientes concurrentes.
'''

import json  # Para codificar y decodificar mensajes JSON
import socket  # Para manejo de sockets TCP
import threading  # Para permitir múltiples clientes simultáneamente
import os  # Para manejo de archivos y directorios
from pprint import pprint  # Para imprimir estructuras de datos de forma legible (depuración)

def gestionar_cliente(cliente, dir_cliente):
    fin = False  # Variable de control del bucle principal del cliente
    while not fin:  # Mientras no se reciba comando 'fin'
        try:
            mensaje = cliente.recv(1024)  # Recibe hasta 1024 bytes del cliente
            mensaje_json = json.loads(mensaje)  # Decodifica el JSON recibido
            comando = mensaje_json.get("comm")  # Extrae el comando
            datos = mensaje_json.get("data")  # Extrae los datos asociados al comando
            pprint(mensaje_json)  # Muestra el mensaje recibido para depuración

            match comando:  # Evalúa el comando recibido
                case "listar":
                    lista = listar(datos)  # Llama a la función listar con la ruta solicitada
                    print(lista)  # Imprime el resultado del listado
                    json_envio = {
                        "res": "OK" if len(lista) > 0 else "ERROR",  # Estado: OK si hay archivos, ERROR si vacío
                        "data": lista  # Datos: lista de archivos/directorios
                    }
                    cliente.send(json.dumps(json_envio).encode())  # Envía respuesta JSON al cliente

                case "descargar":
                    descargar(cliente, datos)  # Llama a la función descargar con la ruta del archivo

                case "fin":
                    fin = True  # Marca fin como True para cerrar el bucle y la conexión
        except Exception as e:
            print(f"Ha habido un error al leer el comando del cliente, {e}")  # Captura errores de comunicación
    
    cliente.close()  # Cierra la conexión con el cliente al terminar

def listar(ruta):
    print(ruta)  # Imprime la ruta solicitada
    resultado = []  # Inicializa la lista de resultados
    if os.path.exists(ruta) and os.path.isdir(ruta):  # Comprueba que la ruta existe y es un directorio
        resultado = os.listdir(ruta)  # Lista los archivos y directorios contenidos
    return resultado  # Retorna la lista de contenidos

def descargar(cliente, ruta):
    if os.path.exists(ruta) and not os.path.isdir(ruta):  # Verifica que el archivo exista y no sea un directorio
        json_respuesta = {
            "res": "OK",  # Estado OK
            "data": os.path.getsize(ruta)  # Tamaño del archivo en bytes
        }
        cliente.send(json.dumps(json_respuesta).encode())  # Envía estado y tamaño del archivo

        with open(ruta, "rb") as file:  # Abre el archivo en modo binario
            while True:
                chunk = file.read(1024)  # Lee el archivo en bloques de 1024 bytes
                if not chunk:  # Si no hay más datos, termina el bucle
                    break
                cliente.send(chunk)  # Envía el bloque al cliente
    else:
        # Archivo no encontrado, envía mensaje de error
        json_respuesta = {
            "res": "ERROR",
            "data": "Archivo no encontrado"
        }
        cliente.send(json.dumps(json_respuesta).encode())

dir_server = ("127.0.0.1", 5000)  # Dirección y puerto del servidor

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea socket TCP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reutilizar la dirección

sock.bind(dir_server)  # Asocia socket con dirección y puerto
sock.listen()  # Pone el socket en modo escucha

while True:  # Bucle principal para aceptar clientes
    try:
        cliente, dir_cliente = sock.accept()  # Espera y acepta la conexión de un cliente
        threading.Thread(target=gestionar_cliente, args=(cliente, dir_cliente)).start()  
        # Crea un hilo para gestionar la comunicación con este cliente
    except Exception as e:
        print("Servidor de descarga cerrado")  # Mensaje si ocurre un error en accept
        os._exit(0)  # Cierra el servidor de manera inmediata
