import time
from threading import Thread
from parking import Parking
from coche import Coche
import random

class Main():
    # al mostrar los coches no supera cantidad_maxima - 1 porque se muestra despues de salir un coche 
    parking = Parking(5, 5) 
    tiempo_entrada_salida = 4/60
    coches_creados = 20

    # Crear 15 coches con tiempo de aparcamiento diferente entre 1 y 8, 
    coches = []
    for i in range(coches_creados):
        tiempo_aparcado = random.randint(1,8) 
        coche = Coche(parking, tiempo_aparcado, tiempo_entrada_salida)
        coches.append(coche)
    
    hilos = []
    for coche in coches:
        hilo = Thread(target=coche.intentar_aparcar, daemon=True)
        hilos.append(hilo)
    
    # Iniciar los hilos con esperas cortas para que no entren de golpe
    for hilo in hilos:
        hilo.start()
        time.sleep(random.uniform(0.1,0.5))  # llegadas aleatorias
    
    for hilo in hilos:
        hilo.join()
    
    print("Todos los coches han aparcado")

if __name__ == "__main__":
    Main()
