import time
from threading import Thread
from puente import Puente
from coche import Coche
import random

def main():
    puente = Puente()
    
    # Crear coches con diferentes sentidos
    coches = []
    for i in range(15):
        sentido = random.choice(["NORTE", "SUR"])
        coche = Coche(sentido, puente)
        coches.append(coche)
    
    hilos = []
    for coche in coches:
        hilo = Thread(target=coche.intentar_cruzar, daemon=True)
        hilos.append(hilo)
    
    # Iniciar los hilos con esperas cortas para que no entren de golpe
    for hilo in hilos:
        hilo.start()
        time.sleep(random.uniform(0.1, 0.5))  # llegadas aleatorias
    
    for hilo in hilos:
        hilo.join()
    
    print("Todos los coches han cruzado el puente")

if __name__ == "__main__":
    main()