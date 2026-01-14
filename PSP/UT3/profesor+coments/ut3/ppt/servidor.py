# Este script implementa un servidor TCP para jugar “Piedra, Papel o Tijera” entre dos clientes.
# Funcionalidad:
# - Escucha en 127.0.0.1:5000.
# - Empareja dos clientes para jugar una partida.
# - Gestiona turnos y puntajes hasta que un jugador llegue a 3 puntos.
# - Envía mensajes sobre el estado del juego y resultado de cada turno.
# Posibles fallos:
# 1. No hay manejo de errores en caso de desconexión de un cliente durante la partida.
# 2. Cada partida ocupa un hilo; sin límites, muchas conexiones pueden saturar el servidor.
# 3. El tamaño máximo de mensaje es de 1024 bytes.
# 4. No hay autenticación; cualquier cliente puede conectarse.
# 5. No hay control de tiempo de respuesta; un jugador lento bloquea al otro.

import socket  # Para crear y manejar sockets TCP
import threading  # Para manejar múltiples partidas simultáneas

jugadas_validas = ["piedra", "papel", "tijera"]  
# Lista de jugadas permitidas

def calcular_ganador_turno(jug_1, jug_2):
    # Determina el ganador de un turno
    resultado_turno = 0  # 0 = empate, -1 = gana jugador 1, 1 = gana jugador 2
    if jug_1 == "piedra" and jug_2 == "papel":
        resultado_turno = 1
    elif jug_1 == "piedra" and jug_2 == "tijera":
        resultado_turno = -1
    elif jug_1 == "tijera" and jug_2 == "piedra":
        resultado_turno = 1
    elif jug_1 == "tijera" and jug_2 == "papel":
        resultado_turno = -1
    elif jug_1 == "papel" and jug_2 == "tijera":
        resultado_turno = 1
    elif jug_1 == "papel" and jug_2 == "piedra":
        resultado_turno = -1
    return resultado_turno  # Retorna el resultado del turno

def juego(cli_1, dir_cli_1, cli_2, dir_cli_2):
    # Gestiona una partida entre dos clientes
    puntos = {"jug_1": 0, "jug_2": 0}  
    # Puntajes iniciales
    fin_juego = False  
    # Variable para controlar el bucle del juego
    ganador = ""  
    # Almacena el ganador final

    cli_1.send(f"El juego ha comenzado, estás jugando contra {dir_cli_2}, envía tu jugada".encode())
    cli_2.send(f"El juego ha comenzado, estás jugando contra {dir_cli_1}, envía tu jugada".encode())
    # Informa a ambos jugadores que la partida comenzó

    while not fin_juego:
        jugada_1 = cli_1.recv(1024)  
        jugada_2 = cli_2.recv(1024)  
        # Recibe la jugada de cada cliente

        if not jugada_1 or not jugada_2:
            raise Exception("No he recibido jugada/s")  
            # Si algún cliente desconecta, lanza excepción

        jug_1_limpia = jugada_1.decode().strip().lower()  
        jug_2_limpia = jugada_2.decode().strip().lower()  
        # Normaliza las jugadas

        if(jug_1_limpia not in jugadas_validas) or (jug_2_limpia not in jugadas_validas):
            raise Exception("La jugada recibida no es válida")  
            # Valida que las jugadas sean correctas

        resultado_turno = calcular_ganador_turno(jug_1_limpia, jug_2_limpia)  
        # Calcula el resultado del turno

        if resultado_turno == -1:  
            puntos["jug_1"] += 1
            if puntos["jug_1"] == 3:
                ganador = "Jugador_1"
        elif resultado_turno == 1:
            puntos["jug_2"] += 1
            if puntos["jug_2"] == 3:
                ganador = "Jugador_2"

        if ganador != "":
            # Fin de la partida
            fin_juego = True
            if ganador == "Jugador_1":
                cli_1.send(f"El rival ha jugado:{jug_2_limpia}.\nHas ganado la partida!".encode())
                cli_1.close()
                cli_2.send(f"El rival ha jugado:{jug_1_limpia}.\nHas perdido la partida!".encode())
                cli_2.close()
            else:
                cli_2.send(f"El rival ha jugado:{jug_1_limpia}.\nHas ganado la partida!".encode())
                cli_2.close()
                cli_1.send(f"El rival ha jugado:{jug_2_limpia}.\nHas perdido la partida!".encode())
                cli_1.close()
        else:
            # La partida continúa
            if resultado_turno == 0:  
                # Empate
                cli_1.send("Habéis jugado lo mismo, se sigue jugando!".encode())
                cli_2.send("Habéis jugado lo mismo, se sigue jugando!".encode())
            elif resultado_turno == -1:  
                # Gana jugador 1
                cli_1.send(f"El rival ha jugado:{jug_2_limpia}.\nHas ganado el turno! Vais {puntos['jug_1']}-{puntos['jug_2']}".encode())
                cli_2.send(f"El rival ha jugado:{jug_1_limpia}.\nHas perdido el turno! Vais {puntos['jug_1']}-{puntos['jug_2']}".encode())
            else:  
                # Gana jugador 2
                cli_1.send(f"El rival ha jugado:{jug_2_limpia}.\nHas perdido el turno! Vais {puntos['jug_1']}-{puntos['jug_2']}".encode())
                cli_2.send(f"El rival ha jugado:{jug_1_limpia}.\nHas ganado el turno! Vais {puntos['jug_1']}-{puntos['jug_2']}".encode())

dir_server = ("127.0.0.1", 5000)  
# Dirección IP y puerto donde el servidor escuchará

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
# Permite reutilizar la dirección inmediatamente

sock.bind(dir_server)  
# Asocia el socket a la dirección

sock.listen()  
# Escucha conexiones entrantes

while True:
    cliente_1, dir_cli_1 = sock.accept()  
    cliente_2, dir_cli_2 = sock.accept()  
    # Espera a que se conecten dos clientes para iniciar una partida

    threading.Thread(target=juego, args=(cliente_1, dir_cli_1, cliente_2, dir_cli_2)).start()  
    # Crea un hilo para manejar la partida de manera concurrente
