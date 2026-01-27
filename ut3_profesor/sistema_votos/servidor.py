'''
Servidor TCP para sistema de votaciones.
Funcionalidad:
- Escucha conexiones TCP en 127.0.0.1:5000.
- Atiende múltiples clientes simultáneamente con hilos.
- Comandos soportados: 
    - "CANDIDATOS": devuelve la lista de candidatos disponibles.
    - "VOTAR": permite votar por un candidato si no se ha votado antes.
    - "FIN": finaliza la sesión del cliente.
- Registra votos en un diccionario por dirección del cliente.

Posibles fallos:
- La identificación del cliente se hace por dirección IP y puerto, lo que puede no ser fiable si el cliente se reconecta.
- No hay límite en el número de clientes concurrentes.
- No hay persistencia de votos; si el servidor se reinicia, se pierden todos los votos.
- El tamaño máximo de mensajes está limitado a 1024 bytes.
'''

import socket  # Para conexiones TCP
import json  # Para codificar y decodificar mensajes JSON
import threading  # Para manejar múltiples clientes simultáneamente
from pprint import pprint  # Para imprimir estructuras de datos de forma legible

# Configuración del servidor y datos iniciales
dir_server = ("127.0.0.1", 5000)  # Dirección y puerto del servidor
lista_candidatos = ["A", "B", "C", "D"]  # Lista de candidatos disponibles
dicc_votos = {}  # Diccionario que almacena los votos por dirección del cliente
lock = threading.Lock()  # Lock para sincronización de acceso al diccionario de votos

def enviar_mensaje(sock, mensaje):
    """Envía un mensaje al cliente a través del socket"""
    try:
        sock.send(mensaje.encode())  # Convierte el mensaje a bytes y envía
    except Exception as e:
        print("Error al enviar el mensaje:",e)  # Captura errores de envío

def recibir_mensaje(sock):
    """Recibe un mensaje JSON del cliente y lo decodifica"""
    try:
        mensaje = sock.recv(1024)  # Recibe hasta 1024 bytes
        mensaje_json = json.loads(mensaje)  # Decodifica JSON
        return mensaje_json
    except Exception as e:
        print("Error al recibir el mensaje:",e)  # Captura errores de recepción o JSON

def manejar_cliente(sock, direccion_cliente):
    """
    Función que gestiona la comunicación con un cliente.
    Parámetros:
    - sock: socket conectado al cliente
    - direccion_cliente: dirección IP y puerto del cliente
    """
    global dicc_votos  # Acceso global al diccionario de votos
    fin = False  # Controla el bucle de comunicación
    while not fin:
        mensaje = recibir_mensaje(sock)  # Recibe mensaje del cliente
        if mensaje is None:  # Si hubo error de conexión
            break
        try:
            comando = mensaje.get("comando")  # Obtiene el comando del JSON
            match comando:
                case "FIN":  # Cliente quiere finalizar sesión
                    fin = True
                    continue
                case "CANDIDATOS":  # Cliente solicita lista de candidatos
                    json_envio = {
                        "res" : "OK",
                        "datos" : lista_candidatos
                    }
                case "VOTAR":  # Cliente desea votar
                    with lock:  # Bloque crítico para acceso seguro a dicc_votos
                        if direccion_cliente in dicc_votos:  # Ya ha votado
                            json_envio = {
                                "res": "error",
                                "error": "Ya se ha votado anteriormente"
                            }
                        else:  # Todavía no ha votado
                            opcion = mensaje.get("candidato")  # Candidato elegido
                            if opcion not in lista_candidatos:  # Validación del candidato
                                json_envio = {
                                    "res": "error",
                                    "error": "Candidato inexistente, comprueba la lista"
                                }
                            else:  # Registro del voto
                                dicc_votos[direccion_cliente] = opcion
                                pprint(dicc_votos)  # Muestra votos actuales
                                json_envio = {
                                    "res" : "OK"
                                }
            enviar_mensaje(sock, json.dumps(json_envio))  # Envía respuesta al cliente
        except Exception as e:
            print("Error al desempaquetar el json:", e)  # Captura errores de procesamiento

    sock.close()  # Cierra la conexión con el cliente al finalizar

# Configuración del socket del servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea socket TCP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reutilizar la dirección
sock.bind(dir_server)  # Asocia el socket con la dirección y puerto
sock.listen()  # Pone el socket en modo escucha

while True:  # Bucle principal para aceptar conexiones
    cliente, dir_cliente = sock.accept()  # Espera y acepta la conexión de un cliente
    threading.Thread(target=manejar_cliente, args=(cliente, dir_cliente)).start()  
    # Crea un hilo para atender al cliente simultáneamente
