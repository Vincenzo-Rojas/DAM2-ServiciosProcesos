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
