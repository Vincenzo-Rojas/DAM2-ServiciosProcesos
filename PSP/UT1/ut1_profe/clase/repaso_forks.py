# Este programa crea una cadena de procesos: padre → hijo → nieto → bisnieto.
# Cada proceso imprime su PID y el PID de sus hijos y padre cuando corresponda.
# Se usan os._exit(0) para que los procesos hijos terminen sin ejecutar código adicional.

import os  # Para crear procesos con fork y obtener PID/PPID

print("Inicio")  # Mensaje inicial

pid_hijo = os.fork()  # Crear proceso hijo

if pid_hijo != 0:  # Código del padre
    print(f"hola, soy el padre, con PID {os.getpid()}, mi proceso clon(hijo) tiene PID {pid_hijo}")
else:  # Código del hijo
    pid_nieto = os.fork()  # Crear proceso nieto
    if pid_nieto != 0:  # Código del hijo
        print(f"Hola, soy el hijo, con PID {os.getpid()}, mi hijo tiene PID {pid_nieto}, mi padre es {os.getppid()}")
        os._exit(0)  # Terminar el hijo
    else:  # Código del nieto
        pid_bisnieto = os.fork()  # Crear proceso bisnieto
        if pid_bisnieto != 0:  # Código del nieto
            print(f"Hola, soy el nieto, con PID {os.getpid()}, mi hijo tiene PID {pid_bisnieto}, mi padre es {os.getppid()}")
            os._exit(0)  # Terminar el nieto
        else:  # Código del bisnieto
            print(f"Hola, soy el bisnieto, con PID {os.getpid()}, mi padre es {os.getppid()}")
            os._exit(0)  # Terminar el bisnieto

print("Final")  # Mensaje final que ejecuta el proceso padre
