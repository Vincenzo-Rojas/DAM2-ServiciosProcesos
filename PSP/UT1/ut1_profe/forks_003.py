# Este programa demuestra la creación de procesos usando dos forks.
# Genera cuatro procesos en total: padre, dos hijos y un nieto.
# Cada proceso imprime su PID y el PID de su padre para mostrar la relación.

import os  # Módulo para funciones del sistema operativo

print("INICIO")  # Mensaje inicial

pid = os.fork()  # Primer fork: crea un hijo
pid_2 = os.fork()  # Segundo fork: crea otro proceso desde cada proceso actual

if pid != 0 and pid_2 != 0:  # Proceso padre original
    print(f"Hola desde el padre, mi PID es: {os.getpid()}")
elif pid != 0 and pid_2 == 0:  # Segundo hijo del padre
    print(f"Hola desde el segundo hijo: {os.getpid()}, mi padre es el: {os.getppid()}")
elif pid == 0 and pid_2 != 0:  # Primer hijo del padre
    print(f"Hola desde el primer hijo: {os.getpid()}, mi padre es el: {os.getppid()}")
else:  # Nieto (hijo del primer hijo)
    print(f"Hola desde el nieto: {os.getpid()}, mi padre es el: {os.getppid()}")

print("FINAL")  # Mensaje final de cada proceso
