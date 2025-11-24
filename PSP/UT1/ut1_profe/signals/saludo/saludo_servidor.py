# Este programa actúa como un servidor que espera señales SIGUSR1.
# Al recibir SIGUSR1, ejecuta la función saludo() e imprime un mensaje.
# Se queda en espera de señales de manera indefinida.

import signal  # Para manejar señales del sistema
import os      # Para obtener el PID del proceso

print(f"Hola, el pid del servidor es: {os.getpid()}")  # Mostrar PID para enviar señales

# Función que se ejecuta al recibir SIGUSR1
def saludo(signum, frame):
    print("se ha recibido la señal de saludo")  # Mensaje al recibir la señal

signal.signal(signal.SIGUSR1, saludo)  # Asociar SIGUSR1 con la función saludo

while True:
    signal.pause()  # Espera a que llegue una señal
