from multiprocessing import Process, Value, Lock
import time, random

META = 15

def mov_tortuga(pos, Lock, winner):
    while pos.value < META:
        with Lock:
            if winner.value:    
                return
        time.sleep(0.5)
        with Lock:
            pos.value += 1
            print(f"La tortuga a avanzado a {pos.value}")
            
            
def mov_liebre(pos, lock, winner):
    while pos.value < META:
        with lock:
            if winner.value:    
                return
        time.sleep(0.3)
        if random.random() < 0.15:
            time.sleep(1)
            print("\tLa liebre se durmio")
        with lock:
            pos.value += 1
            print(f"La liebre a avanzado a {pos.value}")
    
    

def main():
    #Variables
    tortuga_pos = Value('i', 0)  # posición compartida de la tortuga
    liebre_pos = Value('i', 0)   # posición compartida de la liebre
    ganador = Value('b', False) # controla al ganador
    lock = Lock()

    #1 proceso por animal
    p_tortuga = Process(target=mov_tortuga, args=(tortuga_pos, lock,ganador))
    p_liebre = Process(target=mov_liebre, args=(liebre_pos, lock,ganador))

    p_tortuga.start()
    p_liebre.start()

    # Impletacion fuera de las funciones
    while not ganador.value:
        with lock:
            if tortuga_pos.value >= META or liebre_pos.value >= META:
                ganador.value = True
            
    p_tortuga.join()
    p_liebre.join()

    if ganador.value:        
        if tortuga_pos.value == META:
            print(f"\tLa tortuga ha llegado a la meta {tortuga_pos.value}")
        else:
            print(f"\tLa tortuga no ha llegado a la meta, se quedo en posicion: {tortuga_pos.value}")
                    
        if liebre_pos.value == META:
            print(f"\tLa liebre ha llegado a la meta {liebre_pos.value}")
        else:
            print(f"\tLa liebre no ha llegado a la meta, se quedo en posicion: {liebre_pos.value}")

    

if __name__ == "__main__":
    main()