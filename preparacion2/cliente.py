import socket
import json

# Configuracion del cliente
HOST = '127.0.0.1'  # direccion del servidor
PORT = 60000        # puerto del servidor

# Recibir respuesta del servidor
def recibir_json(socket_servidor):
    """
    Recibe un mensaje JSON desde el servidor y lo convierte en diccionario.
    Devuelve None si la conexion se ha cerrado.
    """
    data = socket_servidor.recv(1024).decode()

    if not data:
        print("Conexion cerrada por el servidor")
        return None

    return json.loads(data)

# Enviar respuesta del servidor
def enviar_json(socket_servidor, datos):
    socket_servidor.sendall(json.dumps(datos).encode())

def jugar_adivina_numero():
    
    '''
    Cliente que se conecta al servidor y juega al juego 'Adivina la palabra. '.
    '''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

            
        #Recibe los intentos maximos
        respuesta = recibir_json(s)
        if respuesta is None:
            return
        intentos_max = respuesta.get("MAX_INTENTOS")
        longitud = respuesta.get("longitud")

        print("BIENVENIDO A 'ADIVINA LA PALABRA'")
        print(f"Las palabras tienen entre {longitud[0]} y {longitud[1]} letras")
        print(f"Tienes maximo {intentos_max} intentos.")
        nick = input(f"Introduce tu nick: ")

        # Enviar nick al servidor
        enviar_json(s,{"nick": nick})

        while True:
            palabra = input("Introduce una palabra: ")

            # Enviar intento al servidor
            enviar_json(s,{"intento": palabra})

            #Recibe respuesta
            respuesta = recibir_json(s)
            if respuesta is None:
                return
            
            res = respuesta.get("res")
            datos = respuesta.get("datos")

            if res == "GANADOR":
                print(f"Felicidades! Palabra adivinadam te quedaban {datos['intentos_restantes']} intentos")
                print("Ultimos 5 jugadores WINNER's:")
                for jugador in datos["ultimos"]:
                    print(f"{jugador['nick']} - {jugador['intentos_restantes']} intentos")
                break
            else:
                print(f"Intentos restantes: {datos['intentos_restantes']}, pista: {datos['pista']}")


if __name__ == "__main__":
    jugar_adivina_numero()