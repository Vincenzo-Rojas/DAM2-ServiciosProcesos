import socket 
import threading

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

def juego(cli_1,dir_cli_1,cli_2,dir_cli_2):
    # inicio juego
    cli_1.send(f"El juego ha comenzado,eres el jugador 1, juegas contra {dir_cli_2}, envia tu jugada".encode())
    cli_2.send(f"El juego ha comenzado,eres el jugador 2, juegas contra {dir_cli_1}, envia tu jugada".encode())

    while puntos['jug_1'] != 3 or puntos['jug_1'] != 3:
        jugada_1 = cli_1.recv(1024)
        jugada_2 = cli_2.recv(1024)

        if not jugada_1 or not jugada_2:
            raise Exception("No he recibido jugada/s correctas")
        
        jugada_1_limpia = jugada_1.decode().strip().lower()
        jugada_2_limpia = jugada_2.decode().strip().lower()
        
        if (jugada_1_limpia not in jugadas_validas) or (jugada_2_limpia not in jugadas_validas):
            raise Exception("La jugada en incorrecta")
        
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

        cli_1.send(resultado.encode())
        cli_2.send(resultado.encode())
        resultado = ""

        # Resultado partida
        if puntos['jug_1'] == 3:
            resultado = f"El jugador 1 ha ganado la partida"
        elif puntos['jug_2'] == 3:
            resultado = f"El jugador 2 ha ganado la partida"
        
        if resultado != "":
            cli_1.send(resultado.encode())
            cli_2.send(resultado.encode())


dir_server = ("127.0.0.1", 5000)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(dir_server)

sock.listen()

while True:
    cliente_1,dir_cli_1 = sock.accept()

    threading.Thread(tarjet=juego,args=(cliente_1, cliente_2)).start()