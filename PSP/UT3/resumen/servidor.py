import socket
import threading
import subprocess
import json
import os
import struct
import time

def servidor_chat(udp_port=5001):
    clientes_chat = []
    lock_clientes = threading.Lock()
    avisos_espera = {}  # Para enviar aviso de espera solo 1 vez por cliente

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", udp_port))
    print("[SERVIDOR] Listo en puerto", udp_port)

    while True:
        data, addr = s.recvfrom(4096)
        mensaje = data.decode()
        #print(f"[RECIBIDO] {addr}: {mensaje}")

        with lock_clientes:

            # Comando de desconexión
            if mensaje == "SALIR":
                if addr in clientes_chat:
                    clientes_chat.remove(addr)
                    avisos_espera.pop(addr, None)
                    print(f"[SERVIDOR] {addr} se ha desconectado.")
                    for c in clientes_chat:
                        s.sendto(f"{addr} ha salido del chat.".encode(), c)

            # Comando para listar
            if mensaje == "listar":
                print(f"[SERVIDOR] Clientes conectados: {len(clientes_chat)}")

            # Registrar cliente si no existe
            if addr not in clientes_chat:
                clientes_chat.append(addr)
                avisos_espera[addr] = False
                print(f"[SERVIDOR] Nuevo cliente conectado: {addr}")

            # Comprobación de número de clientes
            if len(clientes_chat) < 2:
                # Enviar aviso de espera solo 1 vez
                if not avisos_espera.get(addr, False):
                    s.sendto("WAIT: Esperando a otro cliente para iniciar el chat...".encode(), addr)
                    avisos_espera[addr] = True
            else:
                # Hay suficientes clientes: enviar mensaje de inicio a todos que puedan escribir
                for c in clientes_chat:
                    if not avisos_espera.get(c, False):
                        s.sendto("START: Ya puedes escribir.".encode(), c)
                        avisos_espera[c] = True

                # Retransmitir mensajes normales (excepto JOIN)
                if "JOIN" not in mensaje:
                    for c in clientes_chat:
                        if c != addr:
                            s.sendto(f"{addr}: {mensaje}".encode(), c)

def servidor_comandos(tcp_port=5002):
    COMANDOS_PERMITIDOS = ["ls", "pwd", "whoami", "date", "hostname"]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", tcp_port))
    s.listen(5)
    print(f"[SERVIDOR COMANDOS] Escuchando en puerto {tcp_port}")

    while True:
        conn, addr = s.accept()
        try:
            data = conn.recv(4096)
            if not data:
                respuesta = {"res": "", "status": "ERROR"}
            else:
                try:
                    recibido = json.loads(data.decode())
                    comando = recibido['comando']

                    # Validación comando permitido
                    comando_base = comando.split()[0]
                    if comando_base not in COMANDOS_PERMITIDOS:
                        respuesta = {"res": "", "status": "ERROR"}
                    else:
                        try:
                            salida = subprocess.check_output(
                                comando,
                                shell=True,
                                text=True,
                                timeout=5
                            )
                            respuesta = {"res": salida, "status": "OK"}
                        except Exception:
                            respuesta = {"res": "", "status": "ERROR"}
                except Exception:
                    respuesta = {"res": "", "status": "ERROR"}
        except Exception:
            respuesta = {"res": "", "status": "ERROR"}

        # Enviar respuesta JSON
        try:
            conn.send(json.dumps(respuesta).encode())
        except:
            pass

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
