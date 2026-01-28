import socket
import json

# Configuracion del cliente
HOST = '127.0.0.1'  # direccion del servidor
PORT = 5000        # puerto del servidor

def jugar_adivina_numero():
    """
    Cliente que se conecta al servidor y juega al juego 'Adivina el numero. '.
    """
    nick = input("Tienes maximo 10 intentos. Introduce tu nick: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Enviar nick al servidor
        s.send(json.dumps({"nick": nick}).encode())

        while True:
            try:
                intento = int(input("Introduce un numero (0-100): "))
            except ValueError:
                print("Debes introducir un numero entero")
                continue

            # Validar que el numero este en el rango 0-100
            if intento >= 0 and intento <= 100:
                # Enviar intento al servidor
                s.send(json.dumps({"num": intento}).encode())

                # Recibir respuesta del servidor
                data = s.recv(1024).decode()
                if not data:
                    print("Conexion cerrada por el servidor")
                    break

                respuesta = json.loads(data)
                res = respuesta.get("res")
                datos = respuesta.get("datos")

                if res == "ok":
                    print(f"Felicidades! Numero adivinado en {datos['intentos']} intentos")
                    print("Ultimos 10 jugadores:")
                    for jugador in datos["ultimos"]:
                        print(f"{jugador['nick']} - {jugador['intentos']} intentos")
                    break
                else:
                    print(f"Intentos usados: {datos['intentos']}, pista: {datos['pista']}")

if __name__ == "__main__":
    jugar_adivina_numero()