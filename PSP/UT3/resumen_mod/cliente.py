import socket
import json
import struct
import time
import os

# ==========================================================
# CHAT UDP
# ==========================================================

def chat_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        msg = input("Mensaje: ").encode()
        sock.sendto(msg, ("127.0.0.1", 5001))
        data, _ = sock.recvfrom(4096)
        print("Respuesta:", data.decode())

# ==========================================================
# STREAM GRUPO
# ==========================================================

def chat_stream_grupo():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b"JOIN", ("127.0.0.1", 5002))
    while True:
        data, _ = sock.recvfrom(4096)
        print("STREAM >", data.decode())

# ==========================================================
# COMANDOS LINUX
# ==========================================================

def ejecutar_comando(cmd):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 6000))
    sock.send(b"cmd")
    time.sleep(0.1)
    sock.send(cmd.encode())
    print(sock.recv(4096).decode())
    sock.close()

# ==========================================================
# ENVÍO ARCHIVOS
# ==========================================================

def enviar_archivo(nombre):
    tam = os.path.getsize(nombre)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 6000))
    sock.send(b"file")
    time.sleep(0.1)

    sock.send(f"{nombre}|{tam}".encode())

    with open(nombre, "rb") as f:
        sock.sendall(f.read())

    print(sock.recv(4096).decode())
    sock.close()

# ==========================================================
# SISTEMA VOTOS
# ==========================================================

def votar(opcion):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 6000))
    sock.send(b"voto")
    time.sleep(0.1)
    msg = json.dumps({"cmd": "votar", "opcion": opcion})
    sock.send(msg.encode())
    print(sock.recv(4096))
    sock.close()

def ver_resultado():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 6000))
    sock.send(b"voto")
    time.sleep(0.1)
    sock.send(json.dumps({"cmd": "resultado"}).encode())
    print(sock.recv(4096).decode())
    sock.close()

# ==========================================================
# STREAMING
# ==========================================================

def stream():
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
# JSON + HILOS
# ==========================================================

def enviar_json(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 6000))
    sock.send(b"json")
    time.sleep(0.1)
    sock.send(json.dumps(msg).encode())
    print(sock.recv(4096).decode())
    sock.close()

# ==========================================================
# NTP
# ==========================================================

def ntp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    paquete = b'\x1b' + 47 * b'\0'
    sock.sendto(paquete, ("127.0.0.1", 12345))

    data, _ = sock.recvfrom(1024)
    unpacked = struct.unpack("!12I", data)
    t = unpacked[10] - 2208988800
    print("Hora NTP :", time.ctime(t))

# ==========================================================
# MENU
# ==========================================================

def menu():
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
