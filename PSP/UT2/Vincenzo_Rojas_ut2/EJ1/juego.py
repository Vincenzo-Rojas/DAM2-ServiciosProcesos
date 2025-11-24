# imports
from threading import Lock, Thread
import time

#variables
cantidad_oro = 0
nivel_pico = 1
lock = Lock()
acabar = False

def generar_oro():
    global cantidad_oro, nivel_pico, lock, acabar
    while True:
        if acabar == False:
            time.sleep(0.2)
            with lock:
                cantidad_oro += nivel_pico*2
        else:
            return

def principal():
    global cantidad_oro, nivel_pico, lock, acabar
    oro_X_nivel = 0
    
    while True:
        with lock:
            oro_X_nivel = 100*nivel_pico
            print(f"Cantidad de oro: {cantidad_oro}")
            print(f"Nivel del pico: {nivel_pico}")

            print(f""" Enter: vuelta al bucle, mostrar oro y nivel
            'm': intenta mejorar el pico, cuesta  {oro_X_nivel}
            'q': Salir del juego """)
        
        opcion = input()

        if opcion == 'm':
            #mejorar pico, revisar oro antes
            with lock:
                if(cantidad_oro >= oro_X_nivel):
                    cantidad_oro -= oro_X_nivel
                    nivel_pico+=1
                    print(f"Nivel del pico {nivel_pico}")
                else:
                    print("Oro insuficiente")

        if opcion == 'q':
            print("finalizando el juego")
            acabar = True
            return
    

# creamos los hilos de cada uno
hilo_oro = Thread(target=generar_oro)
hilo_principal = Thread(target=principal)

hilo_oro.start()
hilo_principal.start()