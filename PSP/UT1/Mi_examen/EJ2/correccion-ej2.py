import random
import time
from multiprocessing import Process, Value

meta = 30

def avanzar_tortuga(pos_tortuga):
    while pos_tortuga.value < meta:
        pos_tortuga.value += 1
        time.sleep(0.5)

def avanzar_liebre(pos_liebre):
    while pos_liebre.value < meta:
        if random.random() > 0.15:  # 85% de avanzar
            pos_liebre.value += 1
            time.sleep(0.3)
        else:
            print("La liebre se ha dormido")
            time.sleep(1)

def mostrar_animales_victoria(pos_tortuga, pos_liebre):
    while pos_tortuga.value < meta and pos_liebre.value < meta:
        pista_t = "_" * (pos_tortuga.value) + "T" + "_" * (meta - pos_tortuga.value - 1) + "|"
        pista_l = "_" * (pos_liebre.value) + "L" + "_" * (meta - pos_liebre.value - 1) + "|"
        print(pista_t)
        print(pista_l)
        print(f"Posiciones: Tortuga={pos_tortuga.value} Liebre={pos_liebre.value}\n")
        time.sleep(0.2)

    # Declarar ganador
    if pos_tortuga.value >= meta and pos_liebre.value >= meta:
        print("Empate!")
    elif pos_tortuga.value >= meta:
        print("Ha ganado la tortuga!")
    else:
        print("Ha ganado la liebre!")

if __name__ == "__main__":
    # Variables compartidas entre procesos
    pos_tortuga = Value('i', 0)
    pos_liebre = Value('i', 0)

    # Crear procesos
    p_tortuga = Process(target=avanzar_tortuga, args=(pos_tortuga,))
    p_liebre = Process(target=avanzar_liebre, args=(pos_liebre,))
    p_mostrar = Process(target=mostrar_animales_victoria, args=(pos_tortuga, pos_liebre))

    # Iniciar procesos
    p_tortuga.start()
    p_liebre.start()
    p_mostrar.start()

    # Esperar a que terminen
    p_tortuga.join()
    p_liebre.join()
    p_mostrar.join()
