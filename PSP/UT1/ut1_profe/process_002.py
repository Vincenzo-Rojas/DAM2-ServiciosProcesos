# Este programa crea dos procesos usando multiprocessing.
# Cada proceso ejecuta la función saludo() con diferentes argumentos.
# El proceso principal espera a que ambos terminen antes de continuar.

from multiprocessing import Process  # Para crear procesos en Python
import os  # Para obtener información del sistema (no usado en prints aquí)

def saludo(persona, edad):
    print(f"Hola {persona}, {edad}")  # Imprime saludo con nombre y edad

# Crear dos procesos con diferentes argumentos
proceso_1 = Process(target=saludo, args=("Pedro", 56))
proceso_2 = Process(target=saludo, args=("Salma", 22))

# Iniciar ambos procesos
proceso_1.start()
proceso_2.start()

# Esperar a que ambos procesos terminen
proceso_1.join()
proceso_2.join()

print("adios desde el principal")  # Mensaje final del proceso principal
