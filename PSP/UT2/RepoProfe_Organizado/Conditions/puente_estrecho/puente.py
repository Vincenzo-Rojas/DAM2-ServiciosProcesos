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