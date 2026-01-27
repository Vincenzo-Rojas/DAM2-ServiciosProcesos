import pprint                     # Permite imprimir estructuras complejas de forma legible
import socket                     # Librería estándar para crear sockets TCP/UDP
import json                       # Para codificar y decodificar mensajes en formato JSON
from threading import Thread, Lock  # Para gestionar concurrencia con hilos y un bloqueo seguro

# Lista de comandos válidos que el cliente puede solicitar
comms = ["candidatos", "votar", "comandos"]

# Diccionario donde cada clave es un partido político y su valor es el número de votos
candidatos = {'PA': 0,'PR': 0,'PV': 0,'PM': 0,'PN': 0}

# Estructura para almacenar las IPs que ya han votado, evitando votos repetidos
direccion_voto = {"IPs": []}

# Lock para evitar condiciones de carrera cuando varios hilos modifican candidatos o IPs
lock = Lock()

# Dirección y puerto donde el servidor escuchará conexiones entrantes
dir_server = ("127.0.0.1", 5000)

# Creación del socket del servidor (IPv4 + TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Permite reutilizar el puerto si el servidor se reinicia
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Asocia el socket a la dirección indicada
sock.bind(dir_server)

# Pone el socket en modo escucha con una cola de hasta 5 conexiones simultáneas
sock.listen(5)


def listar_candidatos():
    """Devuelve una lista en texto con los partidos existentes."""
    global candidatos
    with lock:  # Bloqueo para evitar lecturas concurrentes inconsistentes
        resultado = {"res": "Partidos: \n"}
        # Recorre todos los partidos y los concatena en una cadena
        for partido, votos in candidatos.items():
            resultado['res'] += partido + "\n"
    return resultado


def votar(clave, direccion):
    """Gestiona el voto de un cliente según su IP."""
    global candidatos, direccion_voto

    # Verifica si el partido existe
    if clave not in candidatos:
        return {"res": "Error", "Error": f"Partido {clave} no existe"}

    with lock:  # Bloqueo: asegura que la escritura sea atómica y segura
        # Se verifica si la IP ya votó
        if direccion[0] not in direccion_voto["IPs"]:
            candidatos[clave] += 1                 # Incrementa el contador de votos
            direccion_voto["IPs"].append(direccion[0])  # Guarda solo la IP que votó
            pprint.pprint(candidatos)             # Muestra por consola el estado del recuento
            return  {"res": "Ha votado correctamente", "Error": ""}
        else:
            # Si ya ha votado, se notifica error
            return {"res": "Error", "Error": "Ya has votado, no puedes volver a votar"} 


def petition_handler(cliente, direccion):
    """Atiende la petición de cada cliente de forma concurrente."""
    respuesta_json = {"res": "", "Error": ""}
    
    # Recibe hasta 1024 bytes del cliente (se espera un mensaje JSON)
    mensaje_comando = cliente.recv(1024)
    
    if mensaje_comando:
        try:
            # Intenta decodificar el mensaje a JSON
            comando_json = json.loads(mensaje_comando)
        except json.JSONDecodeError:
            # Si no es JSON válido, responde con error y cierra
            cliente.send(json.dumps({"res": "Error", "Error": "JSON inválido"}).encode())
            cliente.close()
            return
        
        # Verifica si el comando recibido es válido
        if comando_json["comm"] not in comms:
            respuesta_json["Error"] = f"No existe el comando [{comando_json['comm']}]"
            respuesta_texto = json.dumps(respuesta_json)
            cliente.send(respuesta_texto.encode())
        
        else:
            # Según el comando se ejecuta una acción diferente
            match comando_json["comm"]:
                case "comandos":
                    respuesta_json["res"] = comms   # Devuelve la lista de comandos disponibles
                case "candidatos":
                    respuesta_json = listar_candidatos()  # Devuelve lista de candidatos
                case "votar":
                    respuesta_json = votar(comando_json["partido"], direccion)  # Ejecuta la votación
                case _:
                    respuesta_json = {"res": "Error", "Error": "Error desconocido"}

            # Envía al cliente el resultado en formato JSON
            cliente.send(json.dumps(respuesta_json).encode())

    # Cierra la conexión con el cliente
    cliente.close()


# Bucle principal del servidor: acepta clientes de manera indefinida
while True:
    cliente, direccion = sock.accept()  # Acepta nueva conexión
    # Lanza un hilo para atender al cliente sin bloquear el servidor
    Thread(target=petition_handler, args=(cliente, direccion)).start()
