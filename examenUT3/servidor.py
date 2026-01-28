# diccionario de 5 preguntas

import socket
import threading
import json
import random
from collections import deque

import unicodedata

# Configuracion del servidor
HOST = '127.0.0.1'  # localhost
PORT = 60005        # puerto de escucha

#Json
PREGUNTAS = [
    {
        "enunciado": "¿Qué continente se descubrió en 1492?",
        "opciones": {
            "A": "América",
            "B": "Europa",
            "C": "Asia",
            "D": "África"
        },
        "correcta": "A"
    },
    {
        "enunciado": "¿Quién fue el presidente estadounidense que ordenó el lanzamiento de las bombas atómicas sobre Japón?",
        "opciones": {
            "A": "George Washington",
            "B": "Theodore Roosevelt",
            "C": "Richard Nixon",
            "D": "Harry S. Truman"
        },
        "correcta": "D"
    },
    {
        "enunciado": "¿Cuál es la aceleración provocada por la gravedad de la Tierra?",
        "opciones":{
            "A": "3m/s²",
            "B": "9.8m/s²",
            "C": "20.4m/s²",
            "D": "6.7m/²"
        },
        "correcta":"B"
    },
    {
        "enunciado": "¿Qué piloto español busca conseguir la triple corona del automovilismo?",
        "opciones": {
            "A": "Carlos Sainz",
            "B": "Juan Pablo Montoya",
            "C": "Fernando Alonso",
            "D": "Cristina Gutiérrez"
        },
        "correcta": "C"
    },
    {
        "enunciado": "¿Qué significa LSTM en redes de neuronas?",
        "opciones": {
            "A": "Long Short-Term Memory",
            "B": "Linear System Training Model",
            "C": "Local State Transfer Machine",
            "D": "Large Scale Training Method"
        },
        "correcta": "A"
    }
]

#REFERENCIA:
"""

Cliente:
    {"respuesta":"B"}

Servidor: 
    {
    "numero_pregunta": 1-5
    "correcto": true/false
    "mensaje": "Fallaste, la respuesta correcta era la {respuesta_correcta}" / "Correcto!"
    "pregunta_siguiente": 
        {"enunciado": lista[1]["enunciado"], "opciones": lista[1]["opciones"]} / null(ultima)
    "puntuacion_actual": 0-5
    "final": true/false
        if true
    "puntuacion_final": f"{puntuacion}/5"
    "mensaje_final": f"!Partida terminada! Has acertado {puntuacion} de 5 preguntas"

    }
"""
# Recibir respuesta del cliente
def recibir_json(conn_cliente):
    """
    Recibe un mensaje JSON desde el cliente y lo convierte en diccionario.
    Devuelve None si la conexion se ha cerrado.
    """
    data = conn_cliente.recv(1024).decode()

    if not data:
        return None

    return json.loads(data)

# Enviar respuesta del cliente
def enviar_json(conn_cliente, datos):
    conn_cliente.sendall(json.dumps(datos).encode())

def manejar_cliente(conn, addr):
    """
    Funcion que maneja la conexion con cada cliente.
    Recibe mensajes en JSON y envia respuestas en JSON.
    """
    print(f"Conexion establecida con {addr}")
    #Guardar acierto del jugador
    acierto = 0
    numero_pregunta = 0
    control = 0

    try:
        #Enviar pregunta
        enviar_json(conn, {"enunciado":PREGUNTAS[control]["enunciado"], "opciones":PREGUNTAS[control]["opciones"], "final": False })
        
        while True:
            #Recibe respuesta
            mensaje = recibir_json(conn)
            if mensaje is None:
                print(f"Error con el cliente {addr}, respuesta invalida")
            respuesta = mensaje.get("respuesta").upper()
            #VALIDAR - RESPUESTAS (A,B,C,D)
            if respuesta not in ["A", "B", "C", "D"]:
                print("5")
                enviar_json(conn, {"error": "Vuelve a intentarlo letra no valida"})
                
            else:
                #Si acierta
                mensaje=""
                numero_pregunta += 1

                if control == 4:
                    mensaje = {
                            "numero_pregunta": numero_pregunta,
                            "correcto": False,
                            "mensaje": "Fallaste, la respuesta correcta era la {PREGUNTAS[control]['correcta']}",
                            "pregunta_siguiente": None,
                            "puntuacion_actual": acierto,
                            "final": True,
                            "puntuacion_final": f"{acierto}/5",
                            "mensaje_final": f"!Partida terminada! Has acertado {acierto} de 5 preguntas"
                            }
                elif respuesta == PREGUNTAS[control]["correcta"]:
                    acierto += 1
                    mensaje = {
                            "numero_pregunta": numero_pregunta,
                            "correcto": True,
                            "mensaje": "Correcto!",
                            "pregunta_siguiente": 
                                {"enunciado": PREGUNTAS[control+1]["enunciado"], "opciones": PREGUNTAS[control+1]["opciones"]},
                            "puntuacion_actual": acierto,
                            "final": False
                        }
                    
                elif respuesta != PREGUNTAS[control]["correcta"]:
                    mensaje = {
                            "numero_pregunta": numero_pregunta,
                            "correcto": False,
                            "mensaje": f"Fallaste, la respuesta correcta era la {PREGUNTAS[control]['correcta']}",
                            "pregunta_siguiente": 
                                {"enunciado": PREGUNTAS[control+1]["enunciado"], "opciones": PREGUNTAS[control+1]["opciones"]},
                            "puntuacion_actual": acierto,
                            "final": False
                        }

                enviar_json(conn, mensaje)
                control += 1


        
    except Exception as e:
        print(f"Error con el cliente {addr}: {e}")
    finally:
        conn.close()
        print(f"Conexion cerrada con {addr}")

def iniciar_servidor():
    """
    Inicia el servidor TCP y espera conexiones de clientes.
    Crea un hilo por cada cliente.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
            hilo.start()

if __name__ == "__main__":
    iniciar_servidor()