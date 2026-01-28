import pprint
import socket
import json

# Configuracion del cliente
HOST = '127.0.0.1'  # direccion del servidor
PORT = 60005        # puerto del servidor

#REFERENCIA:
"""

Cliente:
    {"respuesta":"B"}

Servidor: 
    {
    "numero_pregunta": 1-5
    "correcto": true/false
    "mensaje": "Fallaste, la respuesta correcta era la {respuesta_correcta}" / "Correcto!"
    "pregunta_siguiente": 
        {"enunciado": lista[1]["enunciado"], "opciones": lista[1]["opciones"]} / null(ultima)
    "puntuacion_actual": 0-5
    "final": true/false
        if true
    "puntuacion_final": f"{puntuacion}/5"
    "mensaje_final": f"!Partida terminada! Has acertado {puntuacion} de 5 preguntas"

    }
"""

# Recibir respuesta del servidor
def recibir_json(socket_servidor):
    """
    Recibe un mensaje JSON desde el servidor y lo convierte en diccionario.
    Devuelve None si la conexion se ha cerrado.
    """
    data = socket_servidor.recv(1024).decode()

    if not data:
        print("Conexion cerrada por el servidor")
        return None

    return json.loads(data)

# Enviar respuesta del servidor
def enviar_json(socket_servidor, datos):
    socket_servidor.sendall(json.dumps(datos).encode())

def jugar():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        #Recibe la pregunta
        respuesta = recibir_json(s)
        if respuesta is None:
            return
        enunciado = respuesta.get("enunciado")
        opciones = respuesta.get("opciones")
        final = respuesta.get("final")

        print("BIENVENIDO A 'QUIZZ'")   
        print(enunciado)
        print(opciones)
        print(final)

        while final == False:
            mensaje = input(f"Introduce tu respuesta: ")
            # Enviar al servidor
            enviar_json(s,{"respuesta": mensaje})
            
            #Recibe respuesta
            respuesta = recibir_json(s)
            if respuesta is None:
                return
            
            pprint.pprint(respuesta)

            final = respuesta.get("final")


if __name__ == "__main__":
    jugar()