import time

class Abuela:
    def __init__(self, nombre, mesa, tiempo_x_bandeja, galletas_x_bandeja):
        self.nombre = nombre
        self.mesa = mesa
        self.tiempo_x_bandeja = tiempo_x_bandeja
        self.galletas_x_bandeja = galletas_x_bandeja
        
    def hacer_galletas(self):
        while True:
            with self.mesa.condicion:
                while (self.mesa.huecos_max - self.mesa.galletas) < 10:
                    self.mesa.condicion.wait()
                    
            print("Abuela está preparando una bandeja de galletas")
            time.sleep(self.tiempo_x_bandeja)

            with self.mesa.condicion:
                self.mesa.annadir_bandeja()
                print(f"Abuela ha sacado una bandeja del horno, ya hay {self.mesa.galletas} galletas en la mesa")
                self.mesa.condicion.notify_all()

class Nieto:
    def __init__(self, nombre, mesa, tiempo_x_galleta, limite, tiempo_hambre):
        self.nombre = nombre
        self.mesa = mesa
        self.tiempo_x_galleta = tiempo_x_galleta
        self.limite = limite
        self.tiempo_hambre = tiempo_hambre
        self.contador_galletas = 0

    def comer_galletas(self):
        while True:
            with self.mesa.condicion:
                print(f"El nieto [{self.nombre}] quiere comer")
                while self.mesa.galletas == 0:
                    self.mesa.condicion.wait()
                self.mesa.comer_galleta()
                self.mesa.condicion.notify_all()
                
            print(f"El nieto [{self.nombre}] coge una galleta, quedan {self.mesa.galletas} galletas en la mesa")
            time.sleep(self.tiempo_x_galleta)
            self.contador_galletas += 1
            print(f"El nieto [{self.nombre}] se ha comido la galleta nº {self.contador_galletas}")
            if self.contador_galletas >= self.limite:
                print(f"El nieto [{self.nombre}] está lleno, espera un poco antes de seguir comiendo")
                time.sleep(self.tiempo_hambre)

from threading import Condition

class Mesa:
    def __init__(self, huecos):
        self.huecos_max = huecos
        self.condicion = Condition()
        self.galletas = 0
    
    def annadir_bandeja(self):
        self.galletas += 10

    def coger_galleta(self):
        self.galletas -= 1

#from abuela import Abuela
#from mesa import Mesa
#from nieto import Nieto
from threading import Thread

mesa = Mesa(100)
abuela = Abuela("Andrea", mesa, 1, 10)
nietos = [Nieto(f"Nieto-{i}", mesa, 1/3, 10, 3) for i in range(3)]

# creamos los hilos de cada uno
hilo_abuela = Thread(target=abuela.hacer_galletas)
hilos_nietos = [Thread(target=nieto.comer_galletas) for nieto in nietos]

# iniciamos los hilos
hilo_abuela.start()
for hilo_nieto in hilos_nietos:
    hilo_nieto.start()
