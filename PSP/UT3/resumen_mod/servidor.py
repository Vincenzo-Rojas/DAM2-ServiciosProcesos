import socket
import threading
import json
import subprocess
import os
import time
import struct

# ==========================================================
#  CHAT UDP BÁSICO (carpeta chat)
# ==========================================================

def servidor_chat_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 5001))
    print("[CHAT-UDP] Servidor listo en puerto 5001")

    while True:
        data, addr = sock.recvfrom(4096)
        print("[CHAT-UDP] Mensaje de", addr, ">", data.decode())
        sock.sendto(b"Mensaje recibido", addr)

# ==========================================================
#  STREAM CHAT EN GRUPO (carpeta chat_stream_grupo)
# ==========================================================

clientes_stream = []

def servidor_stream_grupo():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 5002))
    print("[STREAM-GRUPO] Servidor listo en puerto 5002")

    while True:
        data, addr = sock.recvfrom(4096)

        if addr not in clientes_stream:
            clientes_stream.append(addr)

        # reenviar a todos
        for c in clientes_stream:
            try:
                sock.sendto(data, c)
            except Exception as e:
                print(f"Error: {e}")

# ==========================================================
#  EJECUCIÓN DE COMANDOS LINUX (carpeta comandos_linux)
# ==========================================================

def procesar_comando(cmd):
    try:
        result = subprocess.run(cmd.split(),
                                capture_output=True,
                                text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

def servidor_comandos(conn):
    data = conn.recv(4096)
    cmd = data.decode()
    salida = procesar_comando(cmd)
    conn.send(salida.encode())

# ==========================================================
# TRANSFERENCIA DE ARCHIVOS (carpeta ppt)
# ==========================================================

def servidor_archivos(conn):
    meta = conn.recv(1024).decode()
    nombre, tam = meta.split("|")
    tam = int(tam)

    with open(nombre, "wb") as f:
        recibido = 0
        while recibido < tam:
            chunk = conn.recv(4096)
            f.write(chunk)
            recibido += len(chunk)

    conn.send(b"Archivo recibido")

# ==========================================================
# SISTEMA DE VOTOS (carpeta sistema_votos)
# ==========================================================

votos = {
    "A": 0,
    "B": 0,
    "C": 0
}

lock_votos = threading.Lock()

def servidor_votos(conn):
    data = conn.recv(2048)
    msg = json.loads(data.decode())

    if msg["cmd"] == "votar":
        opcion = msg["opcion"]

        with lock_votos:
            if opcion in votos:
                votos[opcion] += 1

        conn.send(json.dumps({"ok": True}).encode())

    elif msg["cmd"] == "resultado":
        conn.send(json.dumps(votos).encode())

# ==========================================================
# STREAMING DE DATOS (carpetas stream y prueba_stream)
# ==========================================================

def servidor_streaming(conn):
    while True:
        data = conn.recv(4096)
        if not data:
            break
        # eco
        conn.send(data)

# ==========================================================
# HILOS + JSON (carpeta stream_hilos_envio_json)
# ==========================================================

def servidor_json_hilos(conn):
    while True:
        data = conn.recv(4096)
        if not data:
            break
        try:
            msg = json.loads(data.decode())
            msg["servidor_timestamp"] = time.time()
            conn.send(json.dumps(msg).encode())
        except:
            conn.send(b"JSON invalido")

# ==========================================================
# SERVIDOR NTP (carpeta stream_hilos_ntp)
# ==========================================================

NTP_DELTA = 2208988800  # diferencia epochs

def servidor_ntp(sock):
    while True:
        data, addr = sock.recvfrom(48)

        t = time.time() + NTP_DELTA
        respuesta = struct.pack("!12I",
            0x1C, 0, 0, 0,
            0, 0, 0, 0,
            int(t), int((t - int(t)) * 2**32),
            int(t), int((t - int(t)) * 2**32)
        )

        sock.sendto(respuesta, addr)

# ==========================================================
# SERVIDOR TCP PRINCIPAL
# ==========================================================

def manejar_cliente(conn, addr):
    try:
        modo = conn.recv(128).decode()

        if modo == "cmd":
            servidor_comandos(conn)
        elif modo == "file":
            servidor_archivos(conn)
        elif modo == "voto":
            servidor_votos(conn)
        elif modo == "stream":
            servidor_streaming(conn)
        elif modo == "json":
            servidor_json_hilos(conn)
        else:
            conn.send(b"Modo desconocido")

    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

def servidor_tcp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", 6000))
    sock.listen(10)
    print("[TCP] Servidor esperando clientes en puerto 6000")

    while True:
        conn, addr = sock.accept()
        threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True).start()

# ==========================================================
# ARRANQUE GENERAL
# ==========================================================

if __name__ == "__main__":

    threading.Thread(target=servidor_chat_udp, daemon=True).start()
    threading.Thread(target=servidor_stream_grupo, daemon=True).start()

    ntp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ntp_sock.bind(("0.0.0.0", 12345))
    threading.Thread(target=servidor_ntp, args=(ntp_sock,), daemon=True).start()

    servidor_tcp()
