import time

class Abuela:
    def __init__(self,galletas_bandeja, tiempo_cocinado, mesa):
        self.galletas_bandeja = galletas_bandeja
        self.tiempo_cocinado = tiempo_cocinado
        self.mesa = mesa

    def hacer_galletas(self):
        while True:
            with self.mesa.condition:
                while (self.mesa.galletas + self.galletas_bandeja) > self.mesa.huecos_max:
                    self.mesa.condition.wait()
                self.mesa.condition.notify_all()
            print(f"Abuela va a preparar galletas")
            time.sleep(self.tiempo_cocinado)
            print(f"Abuela ha prerado las galletas")
            with self.mesa.condition:
                self.mesa.ayadir_bandeja(self.galletas_bandeja)
                print(f"Abuela deja la bandeja en la mesa, hay {self.mesa.galletas} en la mesa")