import time
import logging

class Coche:
    contador = 0
    
    def __init__(self, sentido, puente):
        Coche.contador += 1
        self.id = Coche.contador
        self.sentido = sentido
        self.puente = puente
        self.tiempo_inicio_espera = None
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def __str__(self):
        return f"Coche-{self.id}-{self.sentido}"
    
    def iniciar_espera(self):
        self.tiempo_inicio_espera = time.time()

    def intentar_cruzar(self):
        if self.sentido == "NORTE":
            self.puente.annadir_cola_norte(self)
        else:
            self.puente.annadir_cola_sur(self)
        
        # aquí esperamos que nos toque
        self.puente.entrar_puente(self, self.sentido)
        self.logger.info(f"Coche [{self}] está cruzando el puente")
        time.sleep(2)

        self.puente.salir_puente(self)
        self.logger.info(f"Coche [{self}] ha terminado de cruzar")        


    
