import socket   # Módulo para crear y gestionar sockets TCP/IP
import json     # Módulo para codificar y decodificar mensajes en formato JSON

# Dirección del servidor: IP local + puerto donde escucha
DIR_SERVER = ("127.0.0.1", 5000)


def enviar_comando(comando, datos=None):
    """
    Envía un comando al servidor formateado como JSON.
    - `comando`: string con el comando principal a enviar.
    - `datos`: diccionario opcional con parámetros adicionales.
    Devuelve un diccionario JSON recibido desde el servidor.
    """

    try:
        # Crear un socket TCP/IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conectar al servidor definido en DIR_SERVER
        sock.connect(DIR_SERVER)

        # Construir el paquete base con el comando
        paquete = {"comm": comando}

        # Si se pasan datos adicionales, se añaden al diccionario
        if datos:
            paquete.update(datos)

        # Convertir el diccionario a JSON y enviarlo como bytes
        sock.send(json.dumps(paquete).encode())

        # Esperar respuesta del servidor (máximo 1024 bytes)
        respuesta = sock.recv(1024)

        # Si llega algo, se decodifica el JSON y se devuelve como dict
        if respuesta:
            return json.loads(respuesta)
        else:
            # Si no llega nada, se asume un error general en el servidor
            return {"res": "", "Error": "Sin respuesta del servidor"}

    except ConnectionRefusedError:
        # Error típico cuando el servidor no está activo o el puerto no está disponible
        return {"res": "", "Error": "No se pudo conectar al servidor"}

    finally:
        # Cierre del socket; se ejecute lo que se ejecute antes, siempre se cierra
        sock.close()



def menu():
    """
    Menú interactivo del cliente.
    Ejecuta opciones que envían comandos al servidor según la selección del usuario.
    """
    while True:
        # Muestra el menú principal
        print("\n--- CLIENTE DE VOTACIÓN ---")
        print("1. Listar candidatos")
        print("2. Listar comandos disponibles")
        print("3. Votar")
        print("4. Salir")

        # Solicita una opción al usuario
        opcion = input("Selecciona una opción: ").strip()

        # Opción 1: pedir al servidor la lista de candidatos
        if opcion == "1":
            respuesta = enviar_comando("candidatos")
            print("\nLista de candidatos:")
            print(respuesta.get("res", ""))   # Imprime la parte de respuesta
            if respuesta.get("Error"):
                print(respuesta["Error"])

        # Opción 2: pedir al servidor lista de comandos disponibles
        elif opcion == "2":
            respuesta = enviar_comando("comandos")
            print("\nComandos disponibles:")
            print(respuesta.get("res", ""))
            if respuesta.get("Error"):
                print(respuesta["Error"])

        # Opción 3: votar por un partido
        elif opcion == "3":
            # Solicita al usuario el código del partido
            partido = input("Ingresa el código del partido: ").strip().upper()

            # Enviar comando "votar" con los datos del partido en un dict
            respuesta = enviar_comando("votar", {"partido": partido})

            # Imprimir resultado del servidor
            print("\n" + respuesta.get("res", ""))
            if respuesta.get("Error"):
                print(respuesta["Error"])

        # Opción 4: salir del cliente
        elif opcion == "4":
            print("Saliendo...")
            break

        # Cualquier otra entrada no es válida
        else:
            print("Opción no válida")



# Punto de entrada principal: cuando el archivo se ejecuta directamente
if __name__ == "__main__":
    menu()
