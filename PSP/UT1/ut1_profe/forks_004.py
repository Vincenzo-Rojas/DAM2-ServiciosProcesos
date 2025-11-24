# Este programa demuestra la creación de un proceso hijo con fork
# y la sincronización con wait() para que el padre espere al hijo.
# Cada proceso imprime su PID y el PID del padre.

import os   # Módulo para funciones del sistema operativo
import sys  # Módulo para finalizar el proceso de manera segura

print("INICIO")  # Mensaje inicial

pid = os.fork()  # Crea un proceso hijo

if pid != 0:  # Código del proceso padre
    os.wait()  # Espera a que termine el proceso hijo
    print(f"Hola, soy el padre, con PID {os.getpid()}")
else:  # Código del proceso hijo
    print(f"Hola, soy el proceso hijo, con PID {os.getpid()}, mi padre es {os.getppid()}")
    sys.exit(0)  # Termina el proceso hijo de forma segura

print("FINAL")  # Mensaje final de cada proceso
