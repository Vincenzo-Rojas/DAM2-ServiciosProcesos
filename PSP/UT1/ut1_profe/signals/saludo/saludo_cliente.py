# Este programa envía la señal SIGUSR1 a un proceso cuyo PID se pasa como argumento.
# Sirve para notificar o activar acciones en otro proceso que esté escuchando SIGUSR1.

import os      # Para enviar señales con os.kill y salir del programa
import sys     # Para leer los argumentos del programa
import signal  # Para usar señales del sistema

# Comprobar que se ha pasado un único argumento (el PID)
if len(sys.argv) != 2:
    print("Número incorrecto de parámetros, se espera un PID")
    os._exit(-1)  # Salir inmediatamente con código de error

numero = int(sys.argv[1])  # Convertir argumento a entero (PID del proceso receptor)
os.kill(numero, signal.SIGUSR1)  # Enviar señal SIGUSR1 al proceso indicado
