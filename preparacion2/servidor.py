import socket
import threading
import json
import random
from collections import deque

import unicodedata

# Configuracion del servidor
HOST = '127.0.0.1'  # localhost
PORT = 60000        # puerto de escucha

# Cola para almacenar los ultimos 5 jugadores (FIFO)
ultimos_jugadores = deque(maxlen=5)

# Lock para sincronizar el acceso a la lista de ultimos jugadores
lock = threading.Lock()

# Maximos intentos
MAX_INTENTOS = 8

# Lista de palabras

# Lista de palabras para el juego
palabras = [
    "acierto","programa","python","socket","cliente","servidor","ventana",
    "concurrencia","variable","funcion","algoritmo","cadena","numero",
    "ahorcado","intentos","examen","ordenador","teclado","monitor","archivo"
]

#Longitud de las palabras de la lista
LONGITUD = [4, 12]

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

# Quita solo las tildes
def quitar_tildes(texto):
    resultado = ""
    for c in texto:
        if c in "áéíóúÁÉÍÓÚ":
            resultado += unicodedata.normalize('NFD', c)[0]
        else:
            resultado += c
    return resultado

#Validar la palabra del jugador, devuelve true si solo hay letras
def palabra_valida(palabra:str):
    palabra = quitar_tildes(palabra)

    return palabra.lower().strip().isalpha()
        
def generar_pista(p_secreta: str, p_jugador: str, pista_anterior: str) -> str:
    """
    Genera una pista acumulativa.
    
    - p_secreta: palabra a adivinar
    - p_jugador: intento del jugador
    - pista_anterior: pista obtenida en intentos anteriores

    Devuelve una nueva pista donde:
    - Las letras acertadas en cualquier posicion se muestran
    - Las letras ya descubiertas se mantienen
    - Las letras no descubiertas se muestran como '*'
    """
    # Aseguramos que la pista anterior tenga la longitud de la palabra secreta
    if not pista_anterior or len(pista_anterior) != len(p_secreta):
        pista_anterior = "*" * len(p_secreta)

    nueva_pista = ""

    for i, letra_secreta in enumerate(p_secreta):
        # Letra ya descubierta en intentos anteriores
        if pista_anterior[i] != "*":
            nueva_pista += pista_anterior[i]
        # Letra del jugador coincide con alguna letra de la palabra secreta
        elif letra_secreta in p_jugador:
            nueva_pista += letra_secreta
        else:
            nueva_pista += "*"

    return nueva_pista


def manejar_cliente(conn, addr):
    """
    Funcion que maneja la conexion con cada cliente.
    Recibe mensajes en JSON y envia respuestas en JSON.
    """
    print(f"Conexion establecida con {addr}")

    try:
        #Enviar intentos maximos
        respuesta = {"MAX_INTENTOS": MAX_INTENTOS, "longitud": LONGITUD}
        enviar_json(conn, respuesta)

        #Recibe el nick del jugador
        mensaje = recibir_json(conn)
        if mensaje is None:
            #enviar_json(conn,{"res": "error", "datos": "No se recibio nick"})
            return
        nick = mensaje.get("nick")

        intentos_restantes = MAX_INTENTOS
        palabra_secreta = random.choice(palabras)
        letras_acertadas = ""

        while intentos_restantes > 0:

            #Recibir intento del jugador
            mensaje = recibir_json(conn)
            if mensaje is None:
                return
            palabra_jugador = mensaje.get("intento")
            
            # Resta intento, si es valida o no
            intentos_restantes -= 1

            #Si no es valido
            if len(palabra_jugador) < LONGITUD[0]:
                enviar_json(conn, {"res": "error", "datos": { "intentos_restantes": intentos_restantes, "pista": f"La palabra mas corta es de {LONGITUD[0]} caracteres" }})
            elif len(palabra_jugador) > LONGITUD[1]:
                enviar_json(conn, {"res": "error", "datos": { "intentos_restantes": intentos_restantes, "pista": f"La palabra mas larga es de {LONGITUD[0]} caracteres" }})
            elif palabra_valida(palabra_jugador) is False:
                enviar_json(conn, {"res": "error", "datos": { "intentos_restantes": intentos_restantes, "pista": "entrada invalida" }})           
            else:
                #Si acierta
                if palabra_jugador == palabra_secreta:
                    with lock:
                        ultimos_jugadores.append({"nick": nick, "intentos_restantes": intentos_restantes})
                        ultimos = list(ultimos_jugadores)
                    enviar_json(conn, {"res": "GANADOR","datos": {"intentos_restantes": intentos_restantes,"ultimos": ultimos}})
                    return
                #Si falla o acierta letras
                else:
                    letras_acertadas = generar_pista(palabra_secreta, palabra_jugador, letras_acertadas)
                    enviar_json(conn,{"res": "error", "datos": { "intentos_restantes": intentos_restantes, "pista": letras_acertadas}})
        #Muestra los ultimos 5 ganadores, si no hay mas intentos
        if intentos_restantes == 0:
            enviar_json(conn, {"res": "ok","datos": {"intentos_restantes": intentos_restantes,"ultimos": ultimos_jugadores}})
        
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