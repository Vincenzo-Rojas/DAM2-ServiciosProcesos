from threading import Semaphore
import time

class RecursoCocina:
    def __init__(self,nombre, huecos):
        self.nombre = nombre
        self.huecos = self.limpiar_huecos(huecos)
        self.semaforo = Semaphore(huecos)

    def limpiar_huecos(self, huecos:int):
        if isinstance(huecos, int):
            return huecos
        elif isinstance(huecos, str) and huecos.isnumeric():
            return int(huecos)
        else:
            return 1

    def preparar_item(self, item):
        with self.semaforo:
            print(f"Preparando item: {item.nombre}, del pedido de {item.pedido.cliente.upper()}")
            time.sleep(item.tiempo_prep)
            item.terminar_item()