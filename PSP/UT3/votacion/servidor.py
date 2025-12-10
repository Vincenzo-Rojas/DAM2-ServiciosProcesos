import pprint
import socket
import json
from threading import Thread, Lock

comms = ["candidatos", "votar", "comandos"]
candidatos = {'PA': 0,'PR': 0,'PV': 0,'PM': 0,'PN': 0}
direccion_voto = {"IPs": []}
lock = Lock()

dir_server = ("127.0.0.1", 5000)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(dir_server)
sock.listen(5)

def listar_candidatos():
    global candidatos
    with lock:
        resultado = {"res": "Partidos: \n"}
        for partido, votos in candidatos.items():
            resultado['res'] += partido + "\n"
    return resultado


def votar(clave, direccion):
    global candidatos, direccion_voto

    if clave not in candidatos:
        return {"res": "Error", "Error": f"Partido {clave} no existe"}

    with lock:
        if direccion[0] not in direccion_voto["IPs"]:
            candidatos[clave] += 1    # Suma 1 al valor asociado a clave
            direccion_voto["IPs"].append(direccion[0]) #solo IP
            pprint(candidatos)
            return  {"res": "Ha votado correctamente", "Error": ""}
        else:
            return {"res": "Error", "Error": "Ya has votado, no puedes volver a votar"} 
    


def petition_handler(cliente, direccion):
    respuesta_json = {"res": "", "Error": ""}
    mensaje_comando = cliente.recv(1024)
    
    if mensaje_comando:
        try:
            comando_json = json.loads(mensaje_comando)
        except json.JSONDecodeError:
            cliente.send(json.dumps({"res": "Error", "Error": "JSON inválido"}).encode())
            cliente.close()
            return
        
        if comando_json["comm"] not in comms:
            respuesta_json["Error"] = f"No existe el comando [{comando_json['comm']}]"
            respuesta_texto = json.dumps(respuesta_json)
            cliente.send(respuesta_texto.encode())
        
        else:

            match comando_json["comm"]:
                case "comandos":
                    respuesta_json["res"]=comms
                case "candidatos":
                    respuesta_json = listar_candidatos()
                case "votar":
                    respuesta_json = votar(comando_json["partido"], direccion)
                case _:
                    respuesta_json = {"res": "Error", "Error": "Error desconocido"}

            cliente.send(json.dumps(respuesta_json).encode())

    cliente.close()

while True:
    cliente, direccion = sock.accept()
    Thread(target=petition_handler, args=(cliente, direccion)).start()