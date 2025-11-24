import time
import logging


class Coche:
    contador = 0
    
    def __init__(self, parking, tiempo_aparcado, tiempo_entrar_salir):
        Coche.contador += 1
        self.id = Coche.contador
        self.parking = parking
        self.tiempo_aparcado = tiempo_aparcado
        self.tiempo_entrar_salir = tiempo_entrar_salir
    
    def __str__(self):
        return f"Coche-{self.id}"

    #Ciclo de vida en el parking
    def intentar_aparcar(self):
        self.parking.annadir_cola(self)
        
        # aquí esperamos que nos toque
        self.parking.entrar_parking(self)
        
        #Tiempo que pasa aparcado
        time.sleep(self.tiempo_aparcado)

        #El coche sale del parking
        self.parking.salir_parking(self)