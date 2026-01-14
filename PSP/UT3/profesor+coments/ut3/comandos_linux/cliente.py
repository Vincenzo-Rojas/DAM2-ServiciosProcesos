# Este script implementa un cliente TCP que envía un comando al servidor en 127.0.0.1:5000 usando JSON.
# Funcionalidad:
# - El comando se pasa como argumento al ejecutar el script.
# - Se conecta al servidor, envía el comando y espera una respuesta.
# - Imprime la respuesta decodificada o un mensaje de error si ocurre.
# Posibles fallos:
# 1. No hay manejo de reconexión si el servidor no está disponible.
# 2. Solo envía un comando y termina; no soporta interacción continua.
# 3. No hay validación del contenido del comando más allá de su existencia.
# 4. El tamaño de la respuesta está limitado a 1024 bytes; respuestas más grandes se truncarán.

import socket  # Para crear y manejar sockets TCP
import json  # Para codificar y decodificar datos en formato JSON
import sys  # Para acceder a los argumentos de la línea de comandos

if len(sys.argv) < 2:
    # Verifica que se haya pasado un argumento al script
    print("Hace falta especificar el comando a ejecutar")  
    sys.exit(-1)  
    # Sale del programa con código de error -1 si no se proporcionó comando

dir_server = ("127.0.0.1", 5000)  
# Dirección IP y puerto del servidor al que se conectará

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# Crea un socket TCP usando IPv4

sock.connect(dir_server)  
# Conecta el socket al servidor definido

print("Conexión establecida")  
# Mensaje indicando que la conexión fue exitosa

paquete = json.dumps({"comm" : sys.argv[1]})  
# Crea un diccionario con la clave "comm" y el valor del comando pasado como argumento
# Lo convierte a cadena JSON

sock.send(paquete.encode())  
# Envía el paquete codificado en bytes al servidor

print("Paquete enviado")  
# Indica que el mensaje ha sido enviado

respuesta = sock.recv(1024)  
# Espera hasta 1024 bytes de respuesta del servidor

if respuesta:
    # Si se recibe algún dato
    respuesta_dict = json.loads(respuesta)  
    # Decodifica la respuesta de JSON a diccionario
    if "ERROR" in respuesta_dict["status"]:
        # Comprueba si hay un error en la respuesta
        print("Ha habido un error: ", respuesta_dict["error"])
    else:
        print(respuesta_dict["res"])  
        # Muestra la respuesta recibida del servidor
