import socket
import threading
import subprocess
import json
import os
import struct
import time

clientes_chat = []
lock_clientes = threading.Lock()

def servidor_descargas(tcp_port=5007):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", tcp_port))
    s.listen(5)

    while True:
        conn, addr = s.accept()

        nombre = conn.recv(4096).decode()  # nombre solicitado
        ruta = os.path.join("descargas", nombre)

        if not os.path.exists(ruta):
            conn.send(str(-1).encode())  # archivo NO encontrado
            conn.close()
        else:
            tamaño = os.path.getsize(ruta)
            conn.send(str(tamaño).encode())  # tamaño del archivo
            ack = conn.recv(4)  # no se usa, solo sincroniza

            f = open(ruta, "rb")
            chunk = f.read(4096)
            while chunk:
                conn.send(chunk)
                chunk = f.read(4096)
            f.close()
            conn.close()


def servidor_chat(udp_port=5001):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", udp_port))
    while True:
        data, addr = s.recvfrom(4096)
        mensaje = data.decode()
        with lock_clientes:
            if addr not in clientes_chat:
                clientes_chat.append(addr)
            for c in clientes_chat:
                s.sendto(f"{addr}: {mensaje}".encode(), c)


def servidor_comandos(tcp_port=5002):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", tcp_port))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        cmd = conn.recv(4096).decode()
        salida = subprocess.getoutput(cmd)  # salida:str
        conn.send(salida.encode())
        conn.close()


def servidor_archivos(tcp_port=5003):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", tcp_port))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        nombre = conn.recv(1024).decode()
        tamaño = int(conn.recv(1024).decode())
        f = open(nombre, "wb")
        recibidos = 0
        while recibidos < tamaño:
            chunk = conn.recv(4096)
            f.write(chunk)
            recibidos += len(chunk)
        f.close()
        conn.close()


def servidor_stream(tcp_port=5004):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", tcp_port))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        while True:
            frame = conn.recv(4096)
            if not frame:
                break
            # simplemente descartamos el “frame”
        conn.close()


def servidor_json(tcp_port=5005):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", tcp_port))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        data = conn.recv(4096)
        obj = json.loads(data.decode())  
        respuesta = {"recibido": obj, "timestamp": time.time()}
        conn.send(json.dumps(respuesta).encode())
        conn.close()


def servidor_ntp(udp_port=5006):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", udp_port))
    while True:
        data, addr = s.recvfrom(1024)
        t = time.time() + 2208988800  
        paquete = struct.pack("!12I", *( [0]*10 + [int(t), 0] ))
        s.sendto(paquete, addr)


if __name__ == "__main__":
    threading.Thread(target=servidor_chat, daemon=True).start()
    threading.Thread(target=servidor_comandos, daemon=True).start()
    threading.Thread(target=servidor_archivos, daemon=True).start()
    threading.Thread(target=servidor_stream, daemon=True).start()
    threading.Thread(target=servidor_json, daemon=True).start()
    threading.Thread(target=servidor_ntp, daemon=True).start()
    threading.Thread(target=servidor_descargas, daemon=True).start()

    print("Servidor multisericio ejecutándose...")
    while True:
        time.sleep(1)
