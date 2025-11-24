# Este programa crea una cadena de procesos: padre → hijo → nieto → bisnieto.
# Cada proceso imprime su PID y el bisnieto cambia una variable compartida para indicar el final.
# El proceso padre espera activamente hasta que la variable compartida cambie.

import os
from multiprocessing import Value  # Para crear variable compartida entre procesos

espera = Value("b", True)  # Variable booleana compartida para sincronización

print("Inicio")  # Mensaje inicial

print(f"hola, soy el padre, con PID {os.getpid()}")
pid_hijo = os.fork()  # Crear proceso hijo

if pid_hijo == 0:  # Código del hijo
    print(f"Hola, soy el hijo, con PID {os.getpid()}")
    pid_nieto = os.fork()  # Crear proceso nieto
    if pid_nieto == 0:  # Código del nieto
        print(f"Hola, soy el nieto, con PID {os.getpid()}")
        pid_bisnieto = os.fork()  # Crear proceso bisnieto
        if pid_bisnieto == 0:  # Código del bisnieto
            print(f"Hola, soy el bisnieto, con PID {os.getpid()}")
            espera.value = False  # Cambia la variable compartida para que el padre termine
            os._exit(0)  # Termina el bisnieto
        else:  # Código del nieto
            os._exit(0)  # Termina el nieto
    else:  # Código del hijo
        os._exit(0)  # Termina el hijo

# Proceso padre espera activamente hasta que bisnieto cambie la variable
while espera.value:
    pass

print("Final")  # Mensaje final del proceso padre
