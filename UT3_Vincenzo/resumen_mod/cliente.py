import socket
import json
import struct
import time
import os

# ==========================================================
# CLIENTE MULTISERVICIO
# Incluye chat UDP, streaming de grupo, ejecución de comandos,
# envío de archivos, sistema de votos, streaming continuo,
# envío de JSON y consulta de hora NTP.
# ==========================================================

# ==========================================================
# CHAT UDP
# Envía mensajes a un servidor UDP y muestra respuestas
# ==========================================================
def chat_udp():
    """
    Función que permite enviar y recibir mensajes via UDP.
    Conecta al servidor en el puerto 5001.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        msg = input("Mensaje: ").encode()  # Captura mensaje del usuario
        sock.sendto(msg, ("127.0.0.1", 5001))  # Enviar mensaje
        data, _ = sock.recvfrom(4096)  # Recibir respuesta
        print("Respuesta:", data.decode())

# ==========================================================
# STREAM DE GRUPO
# Escucha mensajes de grupo vía UDP
# ==========================================================
def chat_stream_grupo():
    """
    Función que se une a un stream de grupo.
    Envía mensaje JOIN y luego imprime todo lo recibido.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b"JOIN", ("127.0.0.1", 5002))  # Solicita unión al grupo
    while True:
        data, _ = sock.recvfrom(4096)
        print("STREAM >", data.decode())

# ==========================================================
# EJECUCIÓN DE COMANDOS LINUX
# ==========================================================
def ejecutar_comando(cmd):
    """
    Envía un comando a un servidor TCP que ejecuta comandos permitidos.
    - cmd: string con el comando a ejecutar
    Imprime la salida recibida.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 6000))
    sock.send(b"cmd")  # Indica tipo de solicitud
    time.sleep(0.1)
    sock.send(cmd.encode())  # Envia comando
    print(sock.recv(4096).decode())
    sock.close()

# ==========================================================
# ENVÍO DE ARCHIVOS
# ==========================================================
def enviar_archivo(nombre):
    """
    Envía un archivo completo al servidor TCP.
    - nombre: ruta del archivo a enviar
    Envía primero tipo de solicitud, luego nombre|tamaño, y finalmente el contenido.
    """
    tam = os.path.getsize(nombre)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 6000))
    sock.send(b"file")  # Tipo de solicitud
    time.sleep(0.1)
    sock.send(f"{nombre}|{tam}".encode())  # Enviar metadata
    with open(nombre, "rb") as f:
        sock.sendall(f.read())  # Enviar contenido
    print(sock.recv(4096).decode())  # Recibir confirmación
    sock.close()

# ==========================================================
# SISTEMA DE VOTOS
# ==========================================================
def votar(opcion):
    """
    Envía un voto al servidor.
    - opcion: cadena con la opción seleccionada (A/B/C)
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 6000))
    sock.send(b"voto")  # Tipo de solicitud
    time.sleep(0.1)
    msg = json.dumps({"cmd": "votar", "opcion": opcion})
    sock.send(msg.encode())
    print(sock.recv(4096).decode())
    sock.close()

def ver_resultado():
    """
    Solicita resultados de votación al servidor y los imprime.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 6000))
    sock.send(b"voto")  # Tipo de solicitud
    time.sleep(0.1)
    sock.send(json.dumps({"cmd": "resultado"}).encode())
    print(sock.recv(4096).decode())
    sock.close()

# ==========================================================
# STREAMING
# ==========================================================
def stream():
    """
    Envía datos de forma continua a un servidor TCP de streaming.
    Imprime eco de cada envío recibido.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 6000))
    sock.send(b"stream")
    time.sleep(0.1)
    while True:
        data = input("Dato a stream: ").encode()
        sock.send(data)
        eco = sock.recv(4096)
        print("Eco:", eco.decode())

# ==========================================================
# ENVÍO DE OBJETOS JSON
# ==========================================================
def enviar_json(msg):
    """
    Envía un objeto JSON al servidor y muestra la respuesta.
    - msg: diccionario a enviar
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 6000))
    sock.send(b"json")
    time.sleep(0.1)
    sock.send(json.dumps(msg).encode())
    print(sock.recv(4096).decode())
    sock.close()

# ==========================================================
# CONSULTA NTP
# ==========================================================
def ntp():
    """
    Solicita la hora a un servidor NTP vía UDP.
    Decodifica la respuesta y la imprime en formato humano.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    paquete = b'\x1b' + 47 * b'\0'  # Mensaje NTP estándar
    sock.sendto(paquete, ("127.0.0.1", 12345))
    data, _ = sock.recvfrom(1024)
    unpacked = struct.unpack("!12I", data)
    t = unpacked[10] - 2208988800  # Convertir NTP a Unix time
    print("Hora NTP :", time.ctime(t))

# ==========================================================
# MENÚ PRINCIPAL
# ==========================================================
def menu():
    """
    Muestra un menú de opciones para el usuario
    y llama a la función correspondiente según elección.
    """
    while True:
        print("\nMENU:")
        print("1. Chat UDP")
        print("2. Stream Grupo")
        print("3. Ejecutar comando")
        print("4. Enviar archivo")
        print("5. Votar")
        print("6. Ver resultados")
        print("7. Stream")
        print("8. Enviar JSON")
        print("9. Cliente NTP")
        op = input("> ")

        if op == "1": chat_udp()
        elif op == "2": chat_stream_grupo()
        elif op == "3": ejecutar_comando(input("cmd: "))
        elif op == "4": enviar_archivo(input("archivo: "))
        elif op == "5": votar(input("A/B/C: "))
        elif op == "6": ver_resultado()
        elif op == "7": stream()
        elif op == "8": enviar_json({"msg":"hola"})
        elif op == "9": ntp()

if __name__ == "__main__":
    menu()
