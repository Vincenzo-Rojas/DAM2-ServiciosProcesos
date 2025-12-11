# Importamos pprint para mostrar estructuras de datos de manera legible
from pprint import pprint
# Importamos socket para trabajar con conexiones TCP y UDP
import socket
# Importamos json para serializar y deserializar datos
import json
# Importamos os para operaciones de archivos y rutas
import os
# Importamos struct para empaquetar y desempaquetar datos binarios
import struct
# Importamos threading para ejecutar funciones en paralelo (hilos)
import threading
# Importamos time para pausas y temporizadores
import time

# Indicador global para permitir enviar mensajes en el chat
puede_escribir = False
# Indicador global para mantener el programa activo o terminarlo
activo = True  # Permite "salir" sin cerrar el programa

# --------------------------------------------------------------------------------
# Función que escucha mensajes del servidor UDP (chat)
# Recibe datos, los decodifica y los muestra por pantalla
# Cambia el estado 'puede_escribir' si se recibe un mensaje distinto a "WAIT"
# --------------------------------------------------------------------------------
def escuchar(sock):
    global puede_escribir, activo
    while activo:
        try:
            data, _ = sock.recvfrom(4096)  # Espera mensaje UDP de hasta 4096 bytes
            if data:
                mensaje = data.decode()  # Decodifica bytes a string
                print(mensaje)
                # Activar escritura si el mensaje no es de espera
                if "WAIT" not in mensaje:
                    puede_escribir = True
        except Exception as e:
            # Solo imprime error y continúa escuchando
            print(f"[ERROR] en escuchar: {e}")

# --------------------------------------------------------------------------------
# Función para enviar mensajes al servidor UDP (chat)
# Permite salir con "salir" y envía mensajes si puede_escribir es True
# --------------------------------------------------------------------------------
def enviar(sock):
    global puede_escribir, activo
    while activo:
        msg = input("")  # Solicita mensaje al usuario
        if msg.lower() == "salir":
            # Enviar señal de salida al servidor y terminar hilos
            sock.sendto("SALIR".encode(), ("127.0.0.1", 5001))
            activo = False
            print("Te has desconectado del chat.")
        elif puede_escribir:
            # Enviar mensaje al servidor UDP
            sock.sendto(msg.encode(), ("127.0.0.1", 5001))
        else:
            # Mensaje de espera si no hay suficientes clientes conectados
            print("Aún no hay dos clientes conectados. Espera un momento.")

# --------------------------------------------------------------------------------
# Función que inicia el cliente de chat
# Crea un socket UDP, envía JOIN al servidor y lanza hilos de escucha y envío
# --------------------------------------------------------------------------------
def cliente_chat():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Avisar al servidor que se une al chat
    sock.sendto("JOIN".encode(), ("127.0.0.1", 5001))
    # Hilo que escucha mensajes entrantes
    hilo_escucha = threading.Thread(target=escuchar, args=(sock,), daemon=True)
    hilo_escucha.start()
    # Hilo que permite enviar mensajes
    hilo_envio = threading.Thread(target=enviar, args=(sock,))
    hilo_envio.start()

# --------------------------------------------------------------------------------
# Función para ejecutar comandos remotos vía TCP
# Envía un JSON con el comando y recibe respuesta
# --------------------------------------------------------------------------------
def ejecutar_comando(cmd, host="127.0.0.1", port=5002):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))  # Conecta con el servidor TCP
    # Envia comando en formato JSON
    s.send(json.dumps({'comando': cmd}).encode())
    # Recibe respuesta (máx 999999 bytes)
    data = s.recv(999999)
    s.close()
    recibido = json.loads(data.decode())  # Decodifica JSON
    # Imprime la salida si el estado es OK
    if recibido['status'] == 'OK':
        print(recibido['res'])
    return recibido

# --------------------------------------------------------------------------------
# Función para enviar un archivo a un servidor TCP
# Envía nombre, tamaño y contenido del archivo en chunks de 4096 bytes
# --------------------------------------------------------------------------------
def enviar_archivo(path, host="127.0.0.1", port=5003):
    tamaño = os.path.getsize(path)  # Obtiene tamaño del archivo
    nombre = os.path.basename(path)  # Obtiene nombre del archivo
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    # Enviar nombre del archivo
    s.send(nombre.encode())
    time.sleep(0.1)  # Pequeña espera para sincronización
    # Enviar tamaño del archivo
    s.send(str(tamaño).encode())
    time.sleep(0.1)
    # Abrir archivo en modo binario y enviar contenido en chunks
    f = open(path, "rb")
    chunk = f.read(4096)
    while chunk:
        s.send(chunk)
        chunk = f.read(4096)
    f.close()
    s.close()

# --------------------------------------------------------------------------------
# Función para enviar un stream simulado de frames a un servidor TCP
# Envía 50 frames separados por 0.05 segundos
# --------------------------------------------------------------------------------
def enviar_stream(host="127.0.0.1", port=5004):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    for i in range(50):
        s.send(b"FRAME_" + bytes(str(i), "utf8"))  # Envía frame
        time.sleep(0.05)  # Pequeña pausa entre frames
    s.close()

# --------------------------------------------------------------------------------
# Función para enviar un objeto JSON a un servidor TCP y recibir respuesta
# --------------------------------------------------------------------------------
def enviar_json(obj, host="127.0.0.1", port=5005):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(json.dumps(obj).encode())
    data = s.recv(4096)
    s.close()
    return json.loads(data.decode())  # Devuelve JSON decodificado

# --------------------------------------------------------------------------------
# Función que pide la hora a un servidor NTP
# Recibe datos binarios UDP, desempaqueta 12 enteros y calcula tiempo UNIX
# --------------------------------------------------------------------------------
def pedir_ntp(host="127.0.0.1", port=5006):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(b"REQ", (host, port))
    data, _ = s.recvfrom(1024)  # Recibe respuesta NTP
    campos = struct.unpack("!12I", data)  # Desempaqueta 12 enteros (big-endian)
    ntp_time = campos[10]  # Tomamos el campo de segundos
    unix_time = ntp_time - 2208988800  # Convertimos a tiempo UNIX
    return unix_time

# --------------------------------------------------------------------------------
# Función para descargar un archivo desde un servidor TCP
# Recibe nombre, tamaño y contenido, lo guarda como "descargado_<nombre>"
# --------------------------------------------------------------------------------
def descargar_archivo(nombre, host="127.0.0.1", port=5007):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(nombre.encode())  # Envía nombre del archivo
    tamaño = int(s.recv(4096).decode())  # Recibe tamaño
    if tamaño == -1:
        print("El archivo no existe en el servidor.")
        s.close()
        return
    s.send(b"OK")  # Confirmación simple de sincronización
    # Abrir archivo local en modo escritura binaria
    f = open("descargado_" + nombre, "wb")
    recibido = 0
    while recibido < tamaño:
        data = s.recv(4096)
        if not data:
            break
        f.write(data)  # Escribe chunk en archivo
        recibido += len(data)
    f.close()
    s.close()
    print(f"Archivo descargado como descargado_{nombre}")

# --------------------------------------------------------------------------------
# BLOQUE PRINCIPAL: menú para seleccionar operación
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    print("1) Enviar chat")
    print("2) Ejecutar comando")
    print("3) Enviar archivo")
    print("4) Streaming")
    print("5) JSON")
    print("6) NTP")
    print("7) Descargar archivo")

    op = input("Seleccione: ")

    # Ejecuta la función correspondiente según opción del usuario
    if op == "1":
        cliente_chat()
    elif op == "2":
        ejecutar_comando(input("Comando: "))
    elif op == "3":
        enviar_archivo(input("Ruta del archivo: "))
    elif op == "4":
        enviar_stream()
    elif op == "5":
        print(enviar_json({"msg": "hola", "valor": 123}))
    elif op == "6":
        print("Hora UNIX: ", pedir_ntp())
    elif op == "7":
        descargar_archivo(input("Nombre del archivo a descargar: "))
