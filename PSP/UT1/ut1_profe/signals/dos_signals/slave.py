# Este programa recibe señales del sistema y ejecuta funciones según la señal.
# SIGUSR1 ejecuta ping() e imprime "ping".
# SIGUSR2 ejecuta pong() e imprime "pong".
# Se queda en pausa esperando señales.

import signal  # Para manejar señales del sistema
import os      # Para obtener el PID del proceso

# Funciones que se ejecutan al recibir las señales
def ping(signum, frame):
    print("ping")  # Se ejecuta al recibir SIGUSR1

def pong(signum, frame):
    print("pong")  # Se ejecuta al recibir SIGUSR2

# Asociar señales con funciones
signal.signal(signal.SIGUSR1, ping)
signal.signal(signal.SIGUSR2, pong)

print(os.getpid())  # Mostrar el PID del proceso para poder enviarle señales

while True:
    signal.pause()  # Espera a que llegue una señal
