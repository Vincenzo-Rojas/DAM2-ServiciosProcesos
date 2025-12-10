import socket
import json

DIR_SERVER = ("127.0.0.1", 5000)

def enviar_comando(comando, datos=None):
    """
    Envía un comando al servidor en formato JSON y devuelve la respuesta en formato JSON.
    `datos` es un diccionario opcional con información adicional ({'partido': 'PA'}).
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(DIR_SERVER)

        paquete = {"comm": comando}
        if datos:
            paquete.update(datos)

        sock.send(json.dumps(paquete).encode())

        respuesta = sock.recv(1024)
        if respuesta:
            return json.loads(respuesta)
        else:
            return {"res": "", "Error": "Sin respuesta del servidor"}

    except ConnectionRefusedError:
        return {"res": "", "Error": "No se pudo conectar al servidor"}
    finally:
        sock.close()

def menu():
    while True:
        print("\n--- CLIENTE DE VOTACIÓN ---")
        print("1. Listar candidatos")
        print("2. Listar comandos disponibles")
        print("3. Votar")
        print("4. Salir")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            respuesta = enviar_comando("candidatos")
            print("\nLista de candidatos:")
            print(respuesta.get("res", ""))
            if respuesta.get("Error"):
                print(respuesta["Error"])

        elif opcion == "2":
            respuesta = enviar_comando("comandos")
            print("\nComandos disponibles:")
            print(respuesta.get("res", ""))
            if respuesta.get("Error"):
                print(respuesta["Error"])

        elif opcion == "3":
            partido = input("Ingresa el código del partido: ").strip().upper()
            respuesta = enviar_comando("votar", {"partido": partido})
            print("\n" + respuesta.get("res", ""))
            if respuesta.get("Error"):
                print(respuesta["Error"])

        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    menu()
