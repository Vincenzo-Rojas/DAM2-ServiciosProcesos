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


from threading import Condition
import logging
import time


class Puente:
    def __init__(self):
        self.cola_sentido_norte = []
        self.cola_sentido_sur = []
        self.condicion = Condition()
        self.sentido = "NORTE"
        self.max_coches_seguidos = 5
        self.coches_seguidos_actuales = 0
        self.coches_cruzando = 0
        self.max_coches_cruzando = 5
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        

    def annadir_cola_norte(self, coche):
        with self.condicion:
            self.logger.info(f"Coche [{coche}] ha llegado al puente, hace cola para ir al NORTE, tiene a {len(self.cola_sentido_norte)} delante")
            self.cola_sentido_norte.append(coche)
            coche.iniciar_espera()
            # Notificar por si el puente está vacío y este coche puede cruzar
            self.condicion.notify_all()
    
    def annadir_cola_sur(self, coche):
        with self.condicion:
            self.logger.info(f"Coche [{coche}] ha llegado al puente, hace cola para ir al SUR, tiene a {len(self.cola_sentido_sur)} delante")
            self.cola_sentido_sur.append(coche)
            coche.iniciar_espera()
            # Notificar por si el puente está vacío y este coche puede cruzar
            self.condicion.notify_all()

    
    def entrar_puente(self, coche, sentido):
        with self.condicion:
            # Esperar hasta que:
            # -Sea el primero de su cola
            # -Pueda cruzar (sentido correcto y no se ha llegado al límite aun)
            # -No se deba cambiar de sentido
            while not self.es_primero_en_cola(coche, sentido) or not self.puede_cruzar(sentido) or self.debe_cambiar_sentido():
                self.condicion.wait()
            
            self.coches_cruzando += 1
            self.coches_seguidos_actuales += 1
            self.sentido = sentido
            
            # quitar el coche de la cola
            if sentido == "NORTE":
                self.cola_sentido_norte.remove(coche)
            else:
                self.cola_sentido_sur.remove(coche)
            
            tiempo_espera = time.time() - coche.tiempo_inicio_espera
            self.logger.info(f"Coche [{coche}] ENTRA al puente hacia {sentido} (esperó {tiempo_espera:.2f}s) - Coches en puente: {self.coches_cruzando}")
            
            # Notificar al siguiente coche de la cola que ahora es su turno
            self.condicion.notify_all()

    def salir_puente(self, coche):
        with self.condicion:
            self.coches_cruzando -= 1
            
            self.logger.info(f"Coche [{coche}] SALE del puente, quedan: {self.coches_cruzando} cruzando")
            
            if self.coches_cruzando == 0:
                if self.debe_cambiar_sentido():
                    self.cambiar_sentido()
                    self.coches_seguidos_actuales = 0
                    self.logger.info(f"Cambio de sentido -> {self.sentido} ")
            
            self.condicion.notify_all()


    def debe_cambiar_sentido(self):
        if self.coches_seguidos_actuales >= self.max_coches_seguidos:
            if self.sentido == "NORTE" and len(self.cola_sentido_sur) > 0:
                return True
            if self.sentido == "SUR" and len(self.cola_sentido_norte) > 0:
                return True
        return False

    def cambiar_sentido(self):
        if self.sentido == "NORTE":
            self.sentido = "SUR"
        else:
            self.sentido = "NORTE"
    
    def es_primero_en_cola(self, coche, sentido):
        if sentido == "NORTE":
            return len(self.cola_sentido_norte) > 0 and self.cola_sentido_norte[0] == coche
        else:
            return len(self.cola_sentido_sur) > 0 and self.cola_sentido_sur[0] == coche
    
    def puede_cruzar(self, sentido):
        # Si no hay nadie cruzando podremos cruzar
        if self.coches_cruzando == 0:
            return True
        
        # Si hay coches del mismo sentido y no se ha alcanzado el límite
        if self.coches_cruzando < self.max_coches_cruzando and sentido == self.sentido:
            return True
        
        return False

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