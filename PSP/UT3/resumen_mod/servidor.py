import socket
import threading
import json
import subprocess
import os
import time
import struct

# ==========================================================
# CHAT UDP BÁSICO (carpeta chat)
# ==========================================================
def servidor_chat_udp():
    """
    Servidor UDP que recibe mensajes de clientes y envía confirmación.
    - Puerto: 5001
    - Protocolo: UDP
    - Comportamiento: imprime mensajes recibidos y envía eco simple
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 5001))  # escucha en todas las interfaces
    print("[CHAT-UDP] Servidor listo en puerto 5001")

    while True:
        data, addr = sock.recvfrom(4096)  # recibe mensaje
        print("[CHAT-UDP] Mensaje de", addr, ">", data.decode())
        sock.sendto(b"Mensaje recibido", addr)  # confirma recepción

# ==========================================================
# STREAM CHAT EN GRUPO (carpeta chat_stream_grupo)
# ==========================================================
clientes_stream = []

def servidor_stream_grupo():
    """
    Servidor UDP que retransmite mensajes a todos los clientes conectados.
    - Puerto: 5002
    - Protocolo: UDP
    - Comportamiento: mantiene lista de clientes y reenvía todos los mensajes recibidos
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 5002))
    print("[STREAM-GRUPO] Servidor listo en puerto 5002")

    while True:
        data, addr = sock.recvfrom(4096)

        if addr not in clientes_stream:
            clientes_stream.append(addr)

        # reenviar mensaje a todos los clientes
        for c in clientes_stream:
            try:
                sock.sendto(data, c)
            except Exception as e:
                print(f"Error: {e}")

# ==========================================================
# EJECUCIÓN DE COMANDOS LINUX (carpeta comandos_linux)
# ==========================================================
def procesar_comando(cmd):
    """
    Ejecuta un comando en shell y devuelve stdout + stderr.
    """
    try:
        result = subprocess.run(cmd.split(),
                                capture_output=True,
                                text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

def servidor_comandos(conn):
    """
    Servidor TCP que recibe un comando desde un cliente, lo ejecuta y devuelve la salida.
    - Protocolo: TCP
    - Comportamiento: recibe texto del comando, lo ejecuta y devuelve resultado
    """
    data = conn.recv(4096)
    cmd = data.decode()
    salida = procesar_comando(cmd)
    conn.send(salida.encode())

# ==========================================================
# TRANSFERENCIA DE ARCHIVOS (carpeta ppt)
# ==========================================================
def servidor_archivos(conn):
    """
    Servidor TCP que recibe archivos completos de clientes.
    - Formato recibido: "nombre|tamaño"
    - Envía confirmación al finalizar
    """
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
votos = {"A": 0, "B": 0, "C": 0}
lock_votos = threading.Lock()

def servidor_votos(conn):
    """
    Servidor TCP para sistema de votación.
    - Comandos posibles: "votar" (incrementa contador), "resultado" (envía totales)
    - Recibe JSON del cliente y responde JSON
    """
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
    """
    Servidor TCP de streaming de datos continuo.
    - Recibe datos y los devuelve como eco
    """
    while True:
        data = conn.recv(4096)
        if not data:
            break
        conn.send(data)

# ==========================================================
# HILOS + JSON (carpeta stream_hilos_envio_json)
# ==========================================================
def servidor_json_hilos(conn):
    """
    Servidor TCP que recibe objetos JSON, añade timestamp y los devuelve.
    - Maneja errores de decodificación JSON
    """
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
NTP_DELTA = 2208988800  # diferencia entre epochs NTP y Unix

def servidor_ntp(sock):
    """
    Servidor UDP que responde a solicitudes NTP.
    - Recibe 48 bytes, responde con tiempo NTP empaquetado
    """
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
# SERVIDOR TCP PRINCIPAL (multiprotocolo)
# ==========================================================
def manejar_cliente(conn, addr):
    """
    Selecciona el servicio según el "modo" enviado por el cliente.
    - modulación de servicios: cmd, file, voto, stream, json
    """
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
    """
    Servidor TCP principal que atiende múltiples clientes usando hilos.
    - Puerto: 6000
    - Cada conexión nueva se maneja en un hilo independiente
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", 6000))
    sock.listen(10)
    print("[TCP] Servidor esperando clientes en puerto 6000")

    while True:
        conn, addr = sock.accept()
        threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True).start()

# ==========================================================
# ARRANQUE GENERAL DEL SERVIDOR
# ==========================================================
if __name__ == "__main__":
    # Hilos para servicios UDP
    threading.Thread(target=servidor_chat_udp, daemon=True).start()
    threading.Thread(target=servidor_stream_grupo, daemon=True).start()

    # Servidor NTP UDP
    ntp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ntp_sock.bind(("0.0.0.0", 12345))
    threading.Thread(target=servidor_ntp, args=(ntp_sock,), daemon=True).start()

    # Servidor TCP principal (multiprotocolo)
    servidor_tcp()
