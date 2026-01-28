import socket
import threading
import json
import random
from collections import deque

# Configuracion del servidor
HOST = '127.0.0.1'  # localhost
PORT = 5000        # puerto de escucha

# Cola para almacenar los ultimos 10 jugadores (FIFO)
ultimos_jugadores = deque(maxlen=10)

# Lock para sincronizar el acceso a la lista de ultimos jugadores
lock = threading.Lock()

def manejar_cliente(conn, addr):
    """
    Funcion que maneja la conexion con cada cliente.
    Recibe mensajes en JSON y envia respuestas en JSON.
    """
    print(f"Conexion establecida con {addr}")

    try:
        # Recibir nick del jugador
        data = conn.recv(1024).decode()
        mensaje = json.loads(data)
        nick = mensaje.get("nick")
        if not nick:
            conn.send(json.dumps({"res": "error", "datos": "No se recibio nick"}).encode())
            conn.close()
            return

        # Generar numero aleatorio a adivinar
        numero_secreto = random.randint(0, 100)
        intentos_max = 10
        intentos_usados = 0

        # Bucle de intentos
        while intentos_usados <= 10:
            data = conn.recv(1024).decode()
            if not data:
                return
            mensaje = json.loads(data)
            intento = mensaje.get("num")

            # Incrementar intentos aunque el numero no sea valido
            intentos_usados += 1

            # Validar que el intento sea un entero
            if intento is None or not isinstance(intento, int):
                respuesta = {"res": "error", "datos": {"intentos": intentos_usados, "pista": "numero invalido"}}
                conn.send(json.dumps(respuesta).encode())
            # Validar que el numero este entre 0 y 100
            elif intento < 0 or intento > 100:
                respuesta = {"res": "error", "datos": {"intentos": intentos_usados, "pista": "numero fuera de rango"}}
                conn.send(json.dumps(respuesta).encode())
            else:
                if intento == numero_secreto:
                    # Acerto el numero
                    with lock:
                        # Guardar en la lista de ultimos jugadores
                        ultimos_jugadores.append({"nick": nick, "intentos": intentos_usados})
                        ultimos = list(ultimos_jugadores)

                    respuesta = {"res": "ok", "datos": {"intentos": intentos_usados, "ultimos": ultimos}}
                    conn.send(json.dumps(respuesta).encode())
                    return
                else:
                    # Dar pista al jugador
                    pista = "mayor" if intento < numero_secreto else "menor"
                    respuesta = {"res": "error", "datos": {"intentos": intentos_usados, "pista": pista}}
                    conn.send(json.dumps(respuesta).encode())
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
