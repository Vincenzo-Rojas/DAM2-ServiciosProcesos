# Este programa envía señales a otro proceso (esclavo) cuyo PID se pasa como argumento.
# Permite al usuario escribir "ping" o "pong" para enviar SIGUSR1 o SIGUSR2 respectivamente.
# Se ejecuta en bucle hasta que se cierre el programa manualmente.

import signal  # Para usar señales del sistema
import os      # Para enviar señales con os.kill
import sys     # Para acceder a los argumentos del programa

print(sys.argv)  # Muestra los argumentos con los que se llamó el programa

# Comprobar que se ha pasado un PID como argumento
if len(sys.argv) != 2:
    sys.exit(-1)  # Salir si no se proporciona exactamente un argumento

pid_esclavo = int(sys.argv[1])  # Convertir argumento a entero (PID del proceso esclavo)

while True:  # Bucle infinito
    comando = input("Ingrese comando:")  # Pedir comando al usuario
    match comando.lower().strip():  # Normalizar el comando
        case "ping":
            os.kill(pid_esclavo, signal.SIGUSR1)  # Enviar señal SIGUSR1
        case "pong":
            os.kill(pid_esclavo, signal.SIGUSR2)  # Enviar señal SIGUSR2
        case _:  # Comando inválido
            print("oye, pon un comando válido (ping|pong)")
            continue  # Volver a pedir comando
