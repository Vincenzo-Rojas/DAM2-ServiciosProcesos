'''
Cliente TCP para sistema de votaciones.
Funcionalidad:
- Conecta con un servidor TCP en 127.0.0.1:5000.
- Permite enviar comandos: "CANDIDATOS" para obtener lista de candidatos, "VOTAR" para votar por un candidato, "FIN" para terminar.
- Recibe respuestas en formato JSON y las procesa.
Posibles fallos:
- No maneja desconexiones inesperadas del servidor.
- No valida si la conexión se ha perdido antes de enviar o recibir.
- El tamaño máximo de mensajes está limitado a 1024 bytes.
- No hay validación de los datos de los candidatos recibidos.
'''

import socket  # Para conexiones TCP
import json  # Para codificar y decodificar mensajes en JSON

def enviar_mensaje(sock, mensaje):
    """
    Envía un mensaje al servidor a través del socket.
    Parámetro:
    - sock: socket TCP conectado
    - mensaje: string a enviar
    """
    try:
        sock.send(mensaje.encode())  # Convierte el string a bytes y envía
    except Exception as e:
        print("Error al enviar el mensaje:",e)  # Captura errores de envío

def recibir_mensaje(sock):
    """
    Recibe un mensaje del servidor y lo decodifica como JSON.
    Retorna:
    - Diccionario Python con los datos recibidos
    """
    try:
        mensaje = sock.recv(1024)  # Recibe hasta 1024 bytes
        mensaje_json = json.loads(mensaje)  # Decodifica JSON
        return mensaje_json
    except Exception as e:
        print("Error al recibir el mensaje:",e)  # Captura errores de recepción o JSON

def gestionar_mensaje_recibido(mensaje):
    """
    Procesa el mensaje recibido del servidor.
    - Si hay un error, lo muestra.
    - Si es OK, muestra los datos o confirma que el voto se realizó.
    """
    try:
        resultado = mensaje.get("res")  # Obtiene el estado
        if resultado == "error":  # Si el servidor reporta error
            error = mensaje.get("error")
            print("El error que reporta el servidor es: ", error)
        if resultado == "OK":  # Si todo salió bien
            if "datos" in mensaje:  # Si hay lista de candidatos
                for i,c in enumerate(mensaje["datos"]):  # Recorre cada candidato
                    print(f"{i + 1}.{c}")  # Muestra el número y nombre del candidato
            else:
                print("Voto realizado exitosamente")  # Confirmación de voto
    except Exception as e:
        print("Ha habido un error al intentar leer el json:", e)  # Captura errores al procesar JSON

# Configuración del servidor
dir_server = ("127.0.0.1", 5000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea socket TCP

sock.connect(dir_server)  # Conecta al servidor
print("Conectados con el server!")  # Confirmación de conexión

comando = ""  # Inicializa variable de comando

while comando != "FIN":  # Bucle principal, se ejecuta hasta que el usuario escriba FIN
    comando = input("Ingresa un comando:\t").strip().upper()  # Solicita comando y normaliza a mayúsculas
    match comando:  # Evalúa el comando ingresado
        case "CANDIDATOS":
            # Comando para solicitar lista de candidatos
            json_envio = {
                "comando": comando
            }
        case "VOTAR":
            # Comando para votar por un candidato
            candidato = ""  # Inicializa variable de candidato
            while not candidato:  # Repite hasta que se ingrese un nombre
                candidato = input("Elige un candidato:\t").strip().upper()
            json_envio = {
                "comando": comando,
                "candidato": candidato
            }
        case "FIN":
            # Comando para terminar sesión
            json_envio = {"comando": comando}
        case _:
            # Comando inválido
            print("Por favor, usa un comando válido ('CANDIDATOS', 'VOTAR', 'FIN')")
            continue  # Vuelve al inicio del bucle

    enviar_mensaje(sock, json.dumps(json_envio))  # Envía el comando al servidor en JSON
    if comando != "FIN":  # Solo procesa la respuesta si no es FIN
        mensaje = recibir_mensaje(sock)  # Recibe la respuesta del servidor
        gestionar_mensaje_recibido(mensaje)  # Procesa la respuesta
