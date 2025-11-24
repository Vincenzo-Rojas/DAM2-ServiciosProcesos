# Este programa envía señales a un proceso secundario según el comando del usuario.
# "empezar" → SIGUSR1, "parar" → SIGUSR2, "continuar" → SIGINT.
# Permite controlar el proceso secundario de forma interactiva.

import signal  # Para usar señales del sistema
import os      # Para enviar señales con os.kill
import sys     # Para leer argumentos del programa

# Comprobar que se ha pasado el PID del proceso secundario
if len(sys.argv) != 2:
    print("falta el pid del secundario")
    os._exit(-1)

pid = int(sys.argv[1])  # PID del proceso secundario

# Bucle que pide comandos al usuario y envía la señal correspondiente
while True:
    command = input("Ingrese señal:\t")
    match command:
        case "empezar":
            os.kill(pid, signal.SIGUSR1)  # Enviar señal SIGUSR1
        case "parar":
            os.kill(pid, signal.SIGUSR2)  # Enviar señal SIGUSR2
        case "continuar":
            os.kill(pid, signal.SIGINT)   # Enviar señal SIGINT
        case _:  # Comando inválido
            print("ese comando no existe, ingresa (empezar|parar|continuar)")
