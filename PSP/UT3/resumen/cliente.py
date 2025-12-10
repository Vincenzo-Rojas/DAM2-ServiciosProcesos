import socket
import json
import os
import struct
import time

def descargar_archivo(nombre, host="127.0.0.1", port=5007):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    s.send(nombre.encode())  # envío nombre

    tamaño = int(s.recv(4096).decode())
    if tamaño == -1:
        print("El archivo no existe en el servidor.")
        s.close()
        return

    s.send(b"OK")  # sincronización simple

    f = open("descargado_" + nombre, "wb")
    recibido = 0

    while recibido < tamaño:
        data = s.recv(4096)
        if not data:
            break
        f.write(data)
        recibido += len(data)

    f.close()
    s.close()
    print(f"Archivo descargado como descargado_{nombre}")


def chat_enviar(mensaje, host="127.0.0.1", port=5001):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(mensaje.encode(), (host, port))


def ejecutar_comando(cmd, host="127.0.0.1", port=5002):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(cmd.encode())
    data = s.recv(999999)
    s.close()
    return data.decode()


def enviar_archivo(path, host="127.0.0.1", port=5003):
    tamaño = os.path.getsize(path)
    nombre = os.path.basename(path)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    s.send(nombre.encode())
    time.sleep(0.1)
    s.send(str(tamaño).encode())
    time.sleep(0.1)

    f = open(path, "rb")
    chunk = f.read(4096)
    while chunk:
        s.send(chunk)
        chunk = f.read(4096)
    f.close()
    s.close()


def enviar_stream(host="127.0.0.1", port=5004):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    for i in range(50):
        s.send(b"FRAME_" + bytes(str(i), "utf8"))
        time.sleep(0.05)
    s.close()


def enviar_json(obj, host="127.0.0.1", port=5005):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(json.dumps(obj).encode())
    data = s.recv(4096)
    s.close()
    return json.loads(data.decode())


def pedir_ntp(host="127.0.0.1", port=5006):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(b"REQ", (host, port))
    data, _ = s.recvfrom(1024)
    campos = struct.unpack("!12I", data)
    ntp_time = campos[10]
    unix_time = ntp_time - 2208988800
    return unix_time


if __name__ == "__main__":
    print("1) Enviar chat")
    print("2) Ejecutar comando")
    print("3) Enviar archivo")
    print("4) Streaming")
    print("5) JSON")
    print("6) NTP")
    print("7) Descargar archivo")

    op = input("Seleccione: ")

    if op == "1":
        chat_enviar(input("Mensaje: "))
    elif op == "2":
        print(ejecutar_comando(input("Comando: ")))
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
