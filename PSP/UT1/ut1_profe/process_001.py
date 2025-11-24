# Este programa crea un nuevo proceso usando multiprocessing.
# El proceso hijo ejecuta la función saludo() y el proceso padre espera a que termine.

from multiprocessing import Process  # Para crear procesos en Python
import os  # Para obtener el PID del proceso actual

def saludo():
    print("Hola")  # Función que imprime un saludo

# Crear un proceso nuevo que ejecuta la función saludo
proceso_nuevo = Process(target=saludo)

print("Proceso nuevo", proceso_nuevo.pid)  # Imprime el PID del proceso antes de iniciarlo (None)

proceso_nuevo.start()  # Inicia el proceso hijo
proceso_nuevo.join()   # Espera a que el proceso hijo termine

print("Proceso lanzador", os.getpid())  # Imprime el PID del proceso padre
