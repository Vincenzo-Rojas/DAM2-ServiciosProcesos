# Este programa simula un dromedario controlado por un usuario.
# Cada dromedario envía señales al gestor para avanzar cuando el usuario pulsa Enter.
# Se recibe el número del dromedario y el PID del gestor como argumentos.

import os      # Para enviar señales con os.kill
import signal  # Para usar señales del sistema
import sys     # Para leer argumentos del programa

# Comprobar que se han pasado los dos argumentos necesarios
if len(sys.argv) != 3:
    print("Faltan parámetros:")
    print("dromedario.py [num_dromedario] [pid_gestor]")
    sys.exit(-1)

pid_gestor = int(sys.argv[2])      # PID del proceso gestor
num_dromedario = sys.argv[1]       # Número del dromedario ("1" o "2")

# Notificar al gestor que un usuario se ha conectado
os.kill(pid_gestor, signal.SIGINT)  # Cuando el gestor reciba 2 conexiones, empieza la carrera

# Determinar la señal que controla este dromedario
signal_drom = signal.SIGUSR1 if num_dromedario == "1" else signal.SIGUSR2

# Bucle que avanza el dromedario cada vez que el usuario pulsa Enter
while True:
    input("Pulsa Enter para avanzar")  # Espera acción del usuario
    os.kill(pid_gestor, signal_drom)  # Enviar señal al gestor para mover el dromedario
