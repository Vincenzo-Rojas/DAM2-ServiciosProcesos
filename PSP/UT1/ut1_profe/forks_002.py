import os  # Módulo para funciones del sistema operativo

print("INICIO")  # Mensaje inicial

pid = os.fork()  # Crea un proceso hijo

if pid != 0:  # Código del proceso padre
    print("hola, soy el padre", os.getpid(), "mi hijo tiene pid:", pid)
else:  # Código del proceso hijo
    print("hola, soy el hijo", os.getpid(), "mi padre tiene pid:", os.getppid())

print("FINAL")  # Mensaje final de cada proceso
