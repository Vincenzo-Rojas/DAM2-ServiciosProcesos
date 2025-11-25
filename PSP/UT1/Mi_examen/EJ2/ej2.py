'''
30 pasos
animal 1: tortuga - 0.5 seg
animal 2: liebre - o.3 seg - 15% dormir 1seg

1 process por animal

quien gana
posiciones de ambosç

impirmir al mover sus posiciones
imprimir si se duerme la liebre
'''


import signal  # Para manejar señales del sistema
import os      # Para obtener el PID del proceso
import random  # Para calcular tropiezos aleatorios
from multiprocessing import Process, Lock
import time


posiciones = [0, 0]  # Posición inicial de los dos animales
meta = 30  # Posición final (meta)
dormir = 0.15  # Probabilidad de tropiezo al avanzar

lock_1 = Lock()  # Lock para el proceso tortuga
lock_2 = Lock()  # Lock para el proceso liebre

lock_2.acquire()  # Bloquea pong al inicio para que ping empiece primero

# Función que hace avanzar a un dromedario
def avanzar_tortuga():
    global posiciones
    while True:
        posiciones[animal] += 1
        time.sleep(0.5)

def avanzar_liebre():
    global dormir, posiciones
    while True:
        if random.random() > dormir:  # Probabilidad de dormir   
            posiciones[animal] += 1
            time.sleep(0.3)
        else:
            print("La liebre se ha dormido")


def mostrar_animales_victoria():
    while True:        
        # Mostrar posiciones de los dromedarios en la pista
        print((posiciones[0] - 1) * "_" + "T" + (meta - posiciones[0] - 1) * "_" + "|")
        print((posiciones[1] - 1) * "_" + "L" + (meta - posiciones[1] - 1) * "_" + "|")
        time.sleep(0.1)

        print(posiciones)
        
        # Comprobar si algún animal ha llegado a la meta
        for i in range(len(posiciones)):
            if posiciones[i] == meta and i == 0:
                print(f"Ha ganado la tortuga")
            if posiciones[i] == meta and i == 1:
                print(f"Ha ganado la liebre")

# Crear 3 procesos con diferentes argumentos
proceso_1 = Process(target=avanzar_tortuga,)
proceso_2 = Process(target=avanzar_liebre, )
proceso_3 = Process(target=mostrar_animales_victoria)

# Iniciar procesos
proceso_3.start()
proceso_1.start()
proceso_2.start()

