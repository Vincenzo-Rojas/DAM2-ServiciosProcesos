# Este programa actúa como un contador controlado por señales.
# SIGUSR1 → empezar a contar desde 0.
# SIGUSR2 → parar el contador.
# SIGINT → continuar el conteo desde donde se quedó.

import os      # Para obtener el PID del proceso
import signal  # Para manejar señales del sistema

# Función que inicia el conteo desde 0
def empezar(signum, frame):  # SIGUSR1
    global contando, contador
    contando = True
    contador = 0
    while contando:
        contador += 1
        print(contador)

# Función que detiene el conteo
def parar(signum, frame):  # SIGUSR2
    global contando
    contando = False

# Función que continúa el conteo desde el valor actual
def continuar(signum, frame):  # SIGINT
    global contando, contador
    contando = True
    while contando:
        contador += 1
        print(contador)

contador = 0     # Valor inicial del contador
contando = False # Indicador de si se está contando

print(os.getpid())  # Mostrar PID para enviar señales

# Asociar señales con funciones
signal.signal(signal.SIGUSR1, empezar)
signal.signal(signal.SIGUSR2, parar)
signal.signal(signal.SIGINT, continuar)

# Bucle infinito esperando señales
while True:
    signal.pause()
