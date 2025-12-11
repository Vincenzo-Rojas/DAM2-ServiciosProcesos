# Servidor TCP para jugar "Piedra, Papel o Tijera" entre pares de clientes.
# Qué hace:
# - Espera dos clientes conectados en 127.0.0.1:5000, los empareja y lanza una partida en un hilo.
# - Cada partida solicita jugadas a ambos clientes hasta que uno alcance 3 puntos.
# - Envía mensajes de control y resultados a los clientes (texto plano).
# Posibles fallos / riesgos:
# - No hay timeouts por turno: un cliente inactivo bloquea la partida.
# - No hay manejo robusto de desconexiones (se envían mensajes tras desconexión).
# - No hay validación extra de datos recibidos (si llegan bytes inesperados puede fallar).
# - Identificación de jugadores por socket/tupla de dirección, no autenticación.
# - No hay logging ni persistencia de resultados; el servidor sigue con hilos sin límite.

import socket  # módulo para sockets TCP/IP
import threading  # módulo para hilos
import time  # importado pero no usado activamente (se mantiene por compatibilidad)

def juego(cli_1,dir_cli_1,cli_2,dir_cli_2):
    # Función que gestiona una partida entre dos clientes.
    # Parámetros:
    # - cli_1, cli_2: sockets conectados a los clientes
    # - dir_cli_1, dir_cli_2: tuplas (ip, puerto) de los clientes

    # Opciones permitidas (solo estas cadenas son válidas)
    jugadas_validas =  ["piedra", "papel", "tijera"]

    # Diccionario que indica qué jugada vence a cuál para evaluar rondas
    victorias = {
        "piedra": "tijera",   # piedra vence a tijera
        "tijera": "papel",    # tijera vence a papel
        "papel": "piedra"     # papel vence a piedra
    }

    # Diccionario de puntuación inicial
    puntos = {
        'jug_1': 0,
        'jug_2': 0
    }

    # Envío de mensaje inicial a ambos clientes informando que la partida empieza
    try:
        cli_1.send(f"El juego ha comenzado,eres el jugador 1, juegas contra {dir_cli_2}".encode())
        cli_2.send(f"El juego ha comenzado,eres el jugador 2, juegas contra {dir_cli_1}".encode())
    except:
        # Si se produce cualquier excepción al enviar (cliente desconectado, por ejemplo),
        # se registra en consola y se continúa; la función no intenta reconectar.
        print("Error al inicio")

    # Bucle principal de la partida: se ejecuta hasta que un jugador llegue a 3 puntos
    while puntos['jug_1'] != 3 and puntos['jug_2'] != 3:
        # Pedir jugada a ambos jugadores intentando notificar primero
        try:
            cli_1.send(f"Envia tu jugada".encode())  # solicita jugada al jugador 1
            cli_2.send(f"Envia tu jugada".encode())  # solicita jugada al jugador 2
        except:
            # Si falla el envío (cliente desconectado), se registra el error
            print("Error durante - 'envio de jugada'")
        
        # Bloqueante: espera las jugadas desde cada socket
        jugada_1 = cli_1.recv(1024)  # recibe bytes del jugador 1
        jugada_2 = cli_2.recv(1024)  # recibe bytes del jugador 2

        # Si alguno no envía datos (b'' o None), se considera jugada inválida
        if not jugada_1 or not jugada_2:
            # Notificar a ambos que la jugada fue incorrecta y repetir el turno
            cli_1.send("Jugada incorrecta, todos deben enviar de nuevo".encode())
            cli_2.send("Jugada incorrecta, todos deben enviar de nuevo".encode())
            continue  # vuelve a pedir jugadas a ambos

        # Decodificar y normalizar las jugadas (minúsculas y sin espacios)
        jugada_1_limpia = jugada_1.decode().strip().lower()
        jugada_2_limpia = jugada_2.decode().strip().lower()
        
        # Validar que ambas jugadas estén dentro de las permitidas
        if jugada_1_limpia not in jugadas_validas or jugada_2_limpia not in jugadas_validas:
            # Si alguna no es válida, informar y repetir turno
            cli_1.send("Jugada incorrecta, todos deben enviar de nuevo".encode())
            cli_2.send("Jugada incorrecta, todos deben enviar de nuevo".encode())
            continue  # vuelve a pedir jugadas a ambos
        
        # Evaluación de la ronda: empate, gana jugador 1 o gana jugador 2
        resultado = ""  # variable temporal para el resultado de la ronda
        if jugada_1_limpia == jugada_2_limpia:
            resultado = "Empate!"
        elif victorias[jugada_1_limpia] == jugada_2_limpia:
            # Si la jugada de jugador 1 vence a la jugada de jugador 2
            resultado = f"{dir_cli_1} gana la ronda (jugador 1) !"
            puntos['jug_1'] += 1  # sumar punto a jugador 1
        else:
            # En cualquier otro caso (y habiendo validado jugadas válidas), gana jugador 2
            resultado = f"{dir_cli_2} gana la ronda (jugador 2) !"
            puntos['jug_2'] += 1  # sumar punto a jugador 2

        # Debug / logging simple en consola antes de enviar a clientes
        print(f"Pre envio clientes {resultado}")

        # Envío del resultado de la ronda a ambos clientes (texto plano)
        cli_1.send(resultado.encode())
        cli_2.send(resultado.encode())

        # Debug / logging tras el envío
        print(f"Post envio clientes {resultado}")

        # Limpiar la variable resultado para reutilizarla
        resultado = ""

        # Comprobar si algún jugador ha alcanzado 3 puntos para declarar ganador
        if puntos['jug_1'] == 3:
            resultado = f"El jugador 1 ha ganado la partida"
        elif puntos['jug_2'] == 3:
            resultado = f"El jugador 2 ha ganado la partida"
        
        # Si hay un ganador, informar a ambos clientes
        if resultado != "":
            print(f"resultado de la partida: {resultado}")
            cli_1.send(resultado.encode())
            cli_2.send(resultado.encode())
        
    # Al salir del bucle (alguien llegó a 3 puntos), notificar a clientes que finaliza la partida
    cli_1.send("FIN".encode())
    cli_2.send("FIN".encode())


# Dirección y puerto donde el servidor escuchará conexiones entrantes
dir_server = ("127.0.0.1", 5000)

# Crear socket TCP IPv4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Permitir reutilizar la dirección/puerto inmediatamente tras cerrar el socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Asociar socket a la dirección especificada
sock.bind(dir_server)

# Poner socket en modo escucha; la cola de espera se limita a 2 conexiones pendientes
sock.listen(2)

# Bucle principal del servidor: aceptar pares de clientes y lanzar partidas
while True:
    # Espera y acepta la primera conexión (bloqueante)
    cliente_1,dir_cli_1 = sock.accept()
    # Espera y acepta la segunda conexión (bloqueante)
    cliente_2,dir_cli_2 = sock.accept()

    # Lanzar la función 'juego' en un hilo para permitir concurrencia de partidas
    threading.Thread(target=juego,args=(cliente_1,dir_cli_1, cliente_2,dir_cli_2)).start()
