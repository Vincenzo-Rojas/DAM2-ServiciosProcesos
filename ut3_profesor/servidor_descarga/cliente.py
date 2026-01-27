# Este script implementa un cliente TCP para interactuar con un servidor de archivos.
# Funcionalidad principal:
# - Conectarse a un servidor TCP en 127.0.0.1:5000
# - Enviar comandos en formato JSON: listar directorios, descargar archivos o finalizar la sesión.
# - Recibir respuestas del servidor en JSON y procesarlas adecuadamente.
# - Guardar archivos descargados en el directorio local elegido por el usuario.
#
# Posibles fallos y riesgos:
# 1. No hay manejo de desconexiones inesperadas del servidor durante cualquier operación.
# 2. Los tamaños máximos de mensajes están limitados (2048 bytes para listar y 1024 bytes por bloque en descarga).
# 3. No hay control sobre permisos de escritura; si el usuario elige un directorio donde no tiene permisos, fallará.
# 4. La descarga sobrescribe archivos con el mismo nombre sin preguntar.
# 5. No hay validación de seguridad en las rutas recibidas del servidor; un servidor malicioso podría intentar sobrescribir archivos locales.
# 6. La interacción es secuencial y bloqueante: mientras se descarga un archivo, no se pueden hacer otras acciones.

import json  # Para codificar y decodificar datos en formato JSON
import socket  # Para crear y manejar conexiones TCP
import os  # Para manejo de rutas y directorios locales
from pprint import pprint  # Para imprimir estructuras de datos de forma legible (opcional, usado en depuración)

comandos_validos = ["listar", "descargar", "fin"]  
# Lista de comandos que el cliente puede enviar al servidor
# "listar" -> obtener contenido de un directorio en el servidor
# "descargar" -> solicitar un archivo para guardarlo localmente
# "fin" -> terminar la sesión

def conseguir_directorio_cliente():
    """
    Solicita al usuario el directorio local donde se guardarán los archivos descargados.
    Validación:
    - Si el usuario no escribe nada, se usa el directorio actual (".").
    - Repite la solicitud hasta que se introduzca un directorio válido existente.
    Retorna:
    - Ruta absoluta o relativa del directorio elegido.
    """
    directorio = ""
    fin = False
    while not fin:
        directorio = input("Ingresa el directorio de descarga del archivo (raíz por defecto):\t")
        directorio = "." if not directorio else directorio  # Usa "." si no hay entrada
        if os.path.exists(directorio):
            fin = True  # Solo acepta directorios existentes
    return directorio

def conseguir_comando():
    """
    Solicita al usuario que ingrese un comando válido.
    Validación:
    - Convierte el comando a minúsculas y elimina espacios al inicio y fin.
    - Repite hasta que el comando sea uno de los válidos.
    Retorna:
    - String con el comando elegido.
    """
    comando = None
    while not comando:
        comando = input("Ingresa el comando:\t").strip().lower()
        if comando not in comandos_validos:
            print(f"COMANDO NO VÁLIDO: solo se admiten los comandos[{comandos_validos}]")
    return comando     

def listar(sock):
    """
    Función para solicitar al servidor la lista de archivos de un directorio.
    Pasos:
    1. Solicita al usuario el directorio en el servidor (por defecto ".").
    2. Envía un JSON con comando 'listar' y el directorio.
    3. Recibe la respuesta del servidor en JSON.
    4. Muestra los elementos si la operación fue exitosa o un mensaje de error si no.
    """
    directorio = input("Ingrese directorio a listar (desde la raíz del servidor) ('directorio raíz por defecto'):\t")
    directorio = "." if not directorio else directorio
    json_envio = {
        "comm" : "listar",
        "data" : directorio
    }
    sock.send(json.dumps(json_envio).encode())  # Envía el comando al servidor en bytes

    try:
        respuesta = sock.recv(2048)  # Recibe hasta 2048 bytes de respuesta
        respuesta_json = json.loads(respuesta)  # Decodifica la respuesta JSON
        respuesta_estado = respuesta_json.get("res")  # Estado de la operación ("OK" o "ERROR")
        respuesta_datos = respuesta_json.get("data")  # Contenido del directorio o mensaje de error
        if respuesta_estado == "ERROR":
            print(f"La carpeta {directorio} no existe o no es un directorio o está vacío")
        else:
            print(f"Los resultados de listar el directorio {directorio} son:")
            for i,item in enumerate(respuesta_datos):
                print(f"{i+1}. {item}")  # Muestra los archivos y subdirectorios enumerados
    except Exception as e:
        print(f"Ha habido un error al listar: {e}")

def descargar(sock):
    """
    Función para descargar un archivo desde el servidor.
    Pasos:
    1. Solicita al usuario el nombre del archivo a descargar.
    2. Solicita el directorio local donde se guardará.
    3. Envía JSON con comando 'descargar' y el nombre del archivo.
    4. Recibe la respuesta inicial con estado y tamaño del archivo.
    5. Si es correcto, recibe el archivo en bloques de 1024 bytes hasta completarlo.
    6. Guarda el archivo en el directorio local elegido.
    """
    archivo = input("Ingrese un archivo a descargar:\t")
    directorio = conseguir_directorio_cliente()
    json_envio = {
        "comm" : "descargar",
        "data" : archivo
    }

    try:
        sock.send(json.dumps(json_envio).encode())  # Envia la petición de descarga al servidor
        
        # Recibe la respuesta inicial que indica si el archivo existe y su tamaño
        mensaje = sock.recv(1024)
        mensaje_json = json.loads(mensaje)
        estado_mensaje = mensaje_json.get("res")  # "OK" o "ERROR"
        datos_mensaje = mensaje_json.get("data")  # Si OK, tamaño en bytes; si ERROR, mensaje
        if estado_mensaje == "ERROR":
            print(f"Ha habido un error con el archivo: {datos_mensaje}")
        else: 
            # Inicio de la descarga en bucle
            with open(f"{os.path.join(directorio,os.path.basename(archivo))}", "wb") as file:
                num_bytes = 0
                while num_bytes < datos_mensaje:
                    chunk_pkg = sock.recv(1024)  # Recibe bloques de 1024 bytes
                    num_bytes += file.write(chunk_pkg)  # Escribe en el archivo local
            print("Archivo guardado!")

    except Exception as e:
        print(f"Ha habido un error en la descarga: {e}")

def envio_fin(sock):
    """
    Envía un comando 'fin' al servidor para indicar que el cliente desea cerrar la sesión.
    """
    json_envio = {
        "comm" : "fin",
        "data" : ""
    }
    sock.send(json.dumps(json_envio).encode())

# Conexión con el servidor
dir_server = ("127.0.0.1", 5000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
sock.connect(dir_server)  # Conexión al servidor
print("Conectado!")

# Bucle principal de interacción con el usuario
fin = False
while not fin:
    comando = conseguir_comando()  # Solicita comando válido
    match comando:
        case "listar":
            listar(sock)  # Ejecuta listado de directorio
        case "descargar":
            descargar(sock)  # Ejecuta descarga de archivo
        case "fin":
            envio_fin(sock)  # Envía fin de sesión
            fin = True  # Sale del bucle y termina el cliente
