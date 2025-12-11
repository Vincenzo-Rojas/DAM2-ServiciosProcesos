# Este script implementa un servidor TCP para un chat, capaz de manejar múltiples clientes simultáneamente usando hilos.
# Funcionalidad:
# - Acepta conexiones entrantes de clientes en 127.0.0.1:5000.
# - Cada cliente se gestiona en un hilo independiente.
# - Los mensajes de un cliente se envían a todos los demás conectados (broadcast).
# Posibles fallos:
# 1. No hay manejo de errores al aceptar conexiones; fallos en sockets pueden cerrar el servidor.
# 2. No hay límite de tamaño de mensajes ni de número de clientes.
# 3. Si un cliente envía datos corruptos o desconecta inesperadamente, puede haber excepciones.
# 4. El broadcast no distingue entre mensajes de sistema y mensajes de chat; podría mezclarse.
# 5. No hay mecanismo de cierre ordenado del servidor.

import socket  # Para crear y manejar sockets
import threading  # Para manejar hilos y concurrencia

dir_server = ("127.0.0.1", 5000)  
# Dirección IP y puerto donde el servidor escuchará

clientes_conectados = []  
# Lista global para mantener referencias a los sockets de los clientes conectados

lock = threading.Lock()  
# Lock para proteger operaciones críticas sobre la lista de clientes compartida

def broadcast(mensaje, emisor):
    # Envía el mensaje a todos los clientes excepto al emisor
    with lock:  
        # Asegura acceso exclusivo a la lista de clientes
        for sock in clientes_conectados:
            if sock != emisor:  # Evita enviar el mensaje de vuelta al remitente
                try:
                    sock.send(mensaje.encode())  # Envía el mensaje codificado
                except Exception as e:
                    print("Cliente desconectado")  
                    # Si hay error, se asume que el cliente se desconectó
                    clientes_conectados.remove(sock)  
                    # Se elimina el cliente de la lista

def manejar_comunicacion(cliente, direccion_cliente):
    # Gestiona la comunicación con un cliente específico
    broadcast(f"[{direccion_cliente}] nueva conexión", cliente)  
    # Informa a los demás que un nuevo cliente se ha conectado

    with lock:
        num_clientes_conectados = len(clientes_conectados)  
    broadcast(f"Hay un total de {num_clientes_conectados} clientes conectados al chat", None)  
    # Informa el número total de clientes conectados

    while True:
        try:
            mensaje = cliente.recv(1024)  
            # Recibe hasta 1024 bytes del cliente
            if mensaje:
                broadcast(mensaje.decode(), cliente)  
                # Reenvía el mensaje a todos los demás clientes
            else:
                cliente.close()  # Cierra el socket si no hay mensaje (cliente desconectado)
                broadcast(f"[{direccion_cliente}] se ha desconectado", None)
                break
        except Exception as e:
            print(f"Ha habido un error: {e}")  
            break

    # Al salir del bucle, el cliente se ha desconectado
    with lock:
        if cliente in clientes_conectados:
            clientes_conectados.remove(cliente)  # Lo eliminamos de la lista
        num_clientes_conectados = len(clientes_conectados)
    broadcast(f"[{direccion_cliente}] se ha desconectado del chat, quedan {num_clientes_conectados} conectados", None)

# Configuración del socket del servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# Socket TCP usando IPv4

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
# Permite reutilizar la dirección inmediatamente después de cerrar el servidor

sock.bind(dir_server)  
# Asocia el socket a la dirección definida

sock.listen()  
# Pone el socket en modo escucha para aceptar conexiones entrantes

while True:
    conn, dir_cliente = sock.accept()  
    # Espera una nueva conexión; devuelve el socket y la dirección del cliente

    clientes_conectados.append(conn)  
    # Añade el cliente a la lista de clientes conectados

    hilo_cliente = threading.Thread(target=manejar_comunicacion, args=(conn, dir_cliente))  
    # Crea un hilo para manejar la comunicación con este cliente

    hilo_cliente.start()  
    # Inicia el hilo
