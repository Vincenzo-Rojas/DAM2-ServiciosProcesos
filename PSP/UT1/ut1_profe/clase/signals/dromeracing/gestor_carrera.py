# Este programa simula una carrera de dromedarios controlada por señales.
# Cada usuario conectado inicia un dromedario. SIGUSR1 y SIGUSR2 hacen avanzar a cada dromedario.
# SIGINT simula la conexión de un usuario. La carrera termina cuando un dromedario llega a la meta.

import signal  # Para manejar señales del sistema
import os      # Para obtener el PID del proceso
import random  # Para calcular tropiezos aleatorios

print(os.getpid())  # Mostrar PID del proceso para enviar señales

num_usuarios = 0  # Contador de usuarios conectados
posiciones_dromedarios = [0, 0]  # Posición inicial de los dos dromedarios
meta = 20  # Posición final (meta)
prob_tropiezo = 0.2  # Probabilidad de tropiezo al avanzar

# Función que hace avanzar a un dromedario
def avanzar_dromedario(signum, frame, num_drom):
    global prob_tropiezo, posiciones_dromedarios
    if random.random() > prob_tropiezo:  # No hay tropiezo
        posiciones_dromedarios[num_drom] += 1
    # Mostrar posiciones de los dromedarios en la pista
    print((posiciones_dromedarios[0] - 1) * "_" + "🐪" + (meta - posiciones_dromedarios[0] - 1) * "_" + "|")
    print((posiciones_dromedarios[1] - 1) * "_" + "🐪" + (meta - posiciones_dromedarios[1] - 1) * "_" + "|")
    # Comprobar si algún dromedario ha llegado a la meta
    for i in range(len(posiciones_dromedarios)):
        if posiciones_dromedarios[i] == meta:
            print(f"Ha ganado el dromedario {i}")

# Función que inicia la carrera asignando señales a los dromedarios
def empezar():
    print("La carrera ha empezado")
    signal.signal(signal.SIGUSR1, lambda signum, frame: avanzar_dromedario(signum, frame, 0))
    signal.signal(signal.SIGUSR2, lambda signum, frame: avanzar_dromedario(signum, frame, 1))

# Función que simula la conexión de un usuario mediante SIGINT
def usuario_conectado(signum, frame):
    global num_usuarios
    print("Se ha conectado un usuario")
    num_usuarios += 1
    if num_usuarios == 2:  # Si hay dos usuarios, empieza la carrera
        empezar()

# Asociar SIGINT con la función de conexión de usuario
signal.signal(signal.SIGINT, usuario_conectado)

# Bucle infinito esperando señales
while True:
    signal.pause()
