import socket 
import threading
import time


def juego(cli_1,dir_cli_1,cli_2,dir_cli_2):

    # Opciones
    jugadas_validas =  ["piedra", "papel", "tijera"]

    # Diccionario que indica qué vence a qué
    victorias = {
        "piedra": "tijera",
        "tijera": "papel",
        "papel": "piedra"
    }

    # Diccionario de puntuacion
    puntos = {
        'jug_1': 0,
        'jug_2': 0
    }

    # inicio juego
    try:
        cli_1.send(f"El juego ha comenzado,eres el jugador 1, juegas contra {dir_cli_2}".encode())
        cli_2.send(f"El juego ha comenzado,eres el jugador 2, juegas contra {dir_cli_1}".encode())
    except:
        print("Error al inicio")

    while puntos['jug_1'] != 3 and puntos['jug_2'] != 3:
        # enviar jugada
        try:
            cli_1.send(f"Envia tu jugada".encode())
            cli_2.send(f"Envia tu jugada".encode())
        except:
            print("Error durante - 'envio de jugada'")
        
        jugada_1 = cli_1.recv(1024)
        jugada_2 = cli_2.recv(1024)

        if not jugada_1 or not jugada_2:
            cli_1.send("Jugada incorrecta, todos deben enviar de nuevo".encode())
            cli_2.send("Jugada incorrecta, todos deben enviar de nuevo".encode())
            continue  # vuelve a pedir jugadas a ambos

        
        jugada_1_limpia = jugada_1.decode().strip().lower()
        jugada_2_limpia = jugada_2.decode().strip().lower()
        
        # comprobar validez
        if jugada_1_limpia not in jugadas_validas or jugada_2_limpia not in jugadas_validas:
            cli_1.send("Jugada incorrecta, todos deben enviar de nuevo".encode())
            cli_2.send("Jugada incorrecta, todos deben enviar de nuevo".encode())
            continue  # vuelve a pedir jugadas a ambos
        
        # Comprobación piedra, papel, tijera + sumar puntos
        resultado = ""
        if jugada_1_limpia == jugada_2_limpia:
            resultado = "Empate!"
        elif victorias[jugada_1_limpia] == jugada_2_limpia:
            resultado = f"{dir_cli_1} gana la ronda (jugador 1) !"
            puntos['jug_1'] += 1
        else:
            resultado = f"{dir_cli_2} gana la ronda (jugador 2) !"
            puntos['jug_2'] += 1

        print(f"Pre envio clientes {resultado}")
        cli_1.send(resultado.encode())
        cli_2.send(resultado.encode())
        print(f"Post envio clientes {resultado}")
        resultado = ""

        # Resultado partida
        if puntos['jug_1'] == 3:
            resultado = f"El jugador 1 ha ganado la partida"
        elif puntos['jug_2'] == 3:
            resultado = f"El jugador 2 ha ganado la partida"
        
        if resultado != "":
            print(f"resultado de la partida: {resultado}")
            cli_1.send(resultado.encode())
            cli_2.send(resultado.encode())
        

    # fin juego
    cli_1.send("FIN".encode())
    cli_2.send("FIN".encode())


dir_server = ("127.0.0.1", 5000)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(dir_server)
sock.listen(2)


while True:
    cliente_1,dir_cli_1 = sock.accept()
    cliente_2,dir_cli_2 = sock.accept()

    threading.Thread(target=juego,args=(cliente_1,dir_cli_1, cliente_2,dir_cli_2)).start()