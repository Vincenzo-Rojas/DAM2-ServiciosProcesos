import socket
import json
import os
import struct
import time
from datetime import datetime

DIR_SERVER = ("127.0.0.1", 5000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(DIR_SERVER)

def enviar(json_envio):
    sock.send.json.dumps(json_envio).encode()

def recibir(cliente:socket):
    data = cliente.recv(1024)

    if data:
        try:
            obj = json.loads(data.decode())
            enviar({"res": "OK", "Error": ""})
            return obj
        except json.JSONDecodeError:
            enviar({"res": "Error", "Error": "Al recibir Json"})
            return


def enviar_datos(socket:socket, tipo, valor):
    json_envio = {
        "sensor_id": {
            "ip": socket.getsockname()[0],
            "puerto": socket.getsockname()[1],
            "fd": socket.fileno()
        },
        "fecha": datetime.now().isoformat(),
        "tipo": tipo,
        "valor": valor
    }
    enviar(json_envio)

def gestion_cliente(socket:socket):

if __name__ == "__main__":
    pass
