import time

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
                