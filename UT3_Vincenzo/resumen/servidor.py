# --------------------------------------------------------------------------------
# Servidor multihilo con múltiples servicios: chat, comandos, archivos, streaming,
# JSON, NTP y descargas de archivos.
# Cada servicio corre en su propio hilo y escucha en su puerto específico.
# --------------------------------------------------------------------------------

import socket
import threading
import subprocess
import json
import os
import struct
import time

# --------------------------------------------------------------------------------
# Servidor de chat UDP
# Gestiona clientes conectados y retransmite mensajes entre ellos
# Espera a que haya al menos 2 clientes antes de permitir escritura
# --------------------------------------------------------------------------------
def servidor_chat(udp_port=5001):
    clientes_chat = []  # Lista de direcciones de clientes conectados
    lock_clientes = threading.Lock()  # Evita condiciones de carrera al modificar clientes
    avisos_espera = {}  # Controla aviso de espera por cliente

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Socket UDP
    s.bind(("0.0.0.0", udp_port))  # Escucha en todas las interfaces
    print("[SERVIDOR] Listo en puerto", udp_port)

    while True:
        data, addr = s.recvfrom(4096)  # Recibe mensaje UDP de cliente
        mensaje = data.decode()  # Decodifica bytes a string

        with lock_clientes:  # Asegura acceso exclusivo a la lista de clientes
            # Cliente se desconecta
            if mensaje == "SALIR":
                if addr in clientes_chat:
                    clientes_chat.remove(addr)
                    avisos_espera.pop(addr, None)
                    print(f"[SERVIDOR] {addr} se ha desconectado.")
                    # Notificar a los demás clientes
                    for c in clientes_chat:
                        s.sendto(f"{addr} ha salido del chat.".encode(), c)

            # Comando para listar clientes conectados
            if mensaje == "listar":
                print(f"[SERVIDOR] Clientes conectados: {len(clientes_chat)}")

            # Registrar cliente nuevo
            if addr not in clientes_chat:
                clientes_chat.append(addr)
                avisos_espera[addr] = False
                print(f"[SERVIDOR] Nuevo cliente conectado: {addr}")

            # Comprobar si hay suficientes clientes
            if len(clientes_chat) < 2:
                # Avisar solo una vez que debe esperar
                if not avisos_espera.get(addr, False):
                    s.sendto("WAIT: Esperando a otro cliente para iniciar el chat...".encode(), addr)
                    avisos_espera[addr] = True
            else:
                # Suficientes clientes: enviar mensaje de inicio a todos
                for c in clientes_chat:
                    if not avisos_espera.get(c, False):
                        s.sendto("START: Ya puedes escribir.".encode(), c)
                        avisos_espera[c] = True

                # Retransmitir mensajes normales a todos menos al remitente
                if "JOIN" not in mensaje:
                    for c in clientes_chat:
                        if c != addr:
                            s.sendto(f"{addr}: {mensaje}".encode(), c)

# --------------------------------------------------------------------------------
# Servidor de comandos TCP
# Permite ejecutar comandos limitados y devuelve salida o error en JSON
# --------------------------------------------------------------------------------
def servidor_comandos(tcp_port=5002):
    COMANDOS_PERMITIDOS = ["ls", "pwd", "whoami", "date", "hostname"]  # Lista blanca

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", tcp_port))
    s.listen(5)
    print(f"[SERVIDOR COMANDOS] Escuchando en puerto {tcp_port}")

    while True:
        conn, addr = s.accept()  # Acepta conexión TCP
        try:
            data = conn.recv(4096)  # Recibe comando
            if not data:
                respuesta = {"res": "", "status": "ERROR"}
            else:
                try:
                    recibido = json.loads(data.decode())
                    comando = recibido['comando']

                    # Validar que el comando esté permitido
                    comando_base = comando.split()[0]
                    if comando_base not in COMANDOS_PERMITIDOS:
                        respuesta = {"res": "", "status": "ERROR"}
                    else:
                        try:
                            # Ejecuta el comando con timeout
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
        conn.close()  # Cerrar conexión TCP

# --------------------------------------------------------------------------------
# Servidor de recepción de archivos TCP
# Recibe nombre y tamaño, luego guarda el archivo recibido
# --------------------------------------------------------------------------------
def servidor_archivos(tcp_port=5003):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", tcp_port))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        nombre = conn.recv(1024).decode()  # Nombre del archivo
        tamaño = int(conn.recv(1024).decode())  # Tamaño en bytes
        f = open(nombre, "wb")  # Abrir archivo en modo binario escritura
        recibidos = 0
        while recibidos < tamaño:
            chunk = conn.recv(4096)  # Leer en bloques
            f.write(chunk)
            recibidos += len(chunk)
        f.close()
        conn.close()

# --------------------------------------------------------------------------------
# Servidor de streaming TCP
# Recibe frames de un cliente y simplemente los descarta
# --------------------------------------------------------------------------------
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
            # Frame recibido, no se procesa
        conn.close()

# --------------------------------------------------------------------------------
# Servidor JSON TCP
# Recibe un objeto JSON y devuelve confirmación con timestamp
# --------------------------------------------------------------------------------
def servidor_json(tcp_port=5005):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", tcp_port))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        data = conn.recv(4096)
        obj = json.loads(data.decode())  # Decodifica objeto
        respuesta = {"recibido": obj, "timestamp": time.time()}
        conn.send(json.dumps(respuesta).encode())
        conn.close()

# --------------------------------------------------------------------------------
# Servidor NTP UDP
# Devuelve la hora en formato NTP (seconds since 1900)
# --------------------------------------------------------------------------------
def servidor_ntp(udp_port=5006):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", udp_port))
    while True:
        data, addr = s.recvfrom(1024)
        t = time.time() + 2208988800  # Convertir a tiempo NTP
        paquete = struct.pack("!12I", *([0]*10 + [int(t), 0]))  # Empaquetar 12 enteros
        s.sendto(paquete, addr)

# --------------------------------------------------------------------------------
# Servidor de descargas TCP
# Permite al cliente solicitar un archivo y recibirlo en chunks
# --------------------------------------------------------------------------------
def servidor_descargas(tcp_port=5007):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", tcp_port))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        nombre = conn.recv(4096).decode()  # Nombre del archivo solicitado
        ruta = os.path.join("descargas", nombre)  # Carpeta 'descargas'

        if not os.path.exists(ruta):
            conn.send(str(-1).encode())  # Archivo no existe
            conn.close()
        else:
            tamaño = os.path.getsize(ruta)
            conn.send(str(tamaño).encode())  # Enviar tamaño
            ack = conn.recv(4)  # Espera sincronización

            f = open(ruta, "rb")
            chunk = f.read(4096)
            while chunk:
                conn.send(chunk)
                chunk = f.read(4096)
            f.close()
            conn.close()

# --------------------------------------------------------------------------------
# BLOQUE PRINCIPAL
# Inicia todos los servicios en hilos daemon
# --------------------------------------------------------------------------------
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
        time.sleep(1)  # Mantener el hilo principal vivo
