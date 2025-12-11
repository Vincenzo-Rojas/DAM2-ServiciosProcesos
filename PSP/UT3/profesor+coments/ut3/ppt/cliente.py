# Este script implementa un cliente TCP para jugar “Piedra, Papel o Tijera” con un servidor.
# Funcionalidad:
# - Se conecta al servidor en 127.0.0.1:5000.
# - Espera mensajes del servidor solicitando la jugada.
# - Envía la jugada seleccionada por el usuario.
# - Finaliza cuando el servidor indica que la partida terminó.
# Posibles fallos:
# 1. No hay manejo de reconexión si el servidor cae.
# 2. Solo acepta jugadas válidas exactas; no hay sugerencias ni repetición en caso de errores.
# 3. Tamaño máximo de mensaje de 1024 bytes.
# 4. No hay temporizadores ni control de turnos; el cliente queda bloqueado en recv() hasta recibir mensaje.

import socket  # Para crear y manejar sockets TCP

def pedir_jugada():
    # Función que solicita al usuario ingresar su jugada y valida que sea correcta
    jugada = ""  
    # Inicializa la jugada vacía
    while not jugada:  
        # Repite hasta recibir una jugada válida
        jug_intento = input("Por favor, ingresa tu jugada:\t")  
        # Solicita jugada al usuario
        if jug_intento.strip().lower() in ["piedra", "papel", "tijera"]:  
            # Valida que la jugada sea una de las opciones permitidas
            jugada = jug_intento.strip().lower()  
            # Normaliza la jugada a minúsculas y sin espacios
    return jugada  
    # Retorna la jugada válida

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# Crea un socket TCP usando IPv4

dir_server = ("127.0.0.1", 5000)  
# Dirección IP y puerto del servidor del juego

sock.connect(dir_server)  
# Conecta el cliente al servidor

jugando = True  
# Variable de control del bucle de juego

while jugando:
    # Bucle principal para jugar hasta que termine la partida
    try:
        mensaje = sock.recv(1024)  
        # Espera recibir un mensaje del servidor (máximo 1024 bytes)

        if not mensaje:
            raise Exception("Desconexion")  
            # Si no se recibe mensaje, se considera que el servidor se desconectó
            
        mensaje_dec = mensaje.decode()  
        # Decodifica el mensaje de bytes a string

        print(mensaje_dec)  
        # Muestra el mensaje del servidor

        if "la partida" in mensaje_dec:  
            # Si el mensaje indica fin de partida
            jugando = False  
            # Termina el bucle
            continue
        else:
            # Si el mensaje solicita jugada
            jugada = pedir_jugada()  
            # Solicita al usuario su jugada
            sock.send(jugada.encode())  
            # Envía la jugada codificada al servidor

    except Exception as e:
        print(f"Ha habido un problema:{e}")  
        # Muestra cualquier error ocurrido durante la comunicación
