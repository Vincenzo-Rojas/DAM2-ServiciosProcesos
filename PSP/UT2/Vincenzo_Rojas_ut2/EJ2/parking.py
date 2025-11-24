from threading import Condition
import logging
import time

class Parking():
    def __init__(self, plazas_maximas, precio):
        self.plazas_maximas = plazas_maximas
        self.coches_aparcados = 0
        self.cola_parking = []
        self.condicion = Condition()
        self.precio = precio
        self.total_acumulado = 0

    def annadir_cola(self, coche):
        with self.condicion:
            print(f"Coche [{coche}] ha llegado a la cola del parking")
            self.cola_parking.append(coche)
            # Notificar por si el parking esta vacio y puede aparcar
            self.condicion.notify_all()
    
    def es_primero_en_cola(self, coche):
            return len(self.cola_parking) > 0 and self.cola_parking[0] == coche
    
    def puede_cruzar(self):
        # Si hay espacio en el parking 
        if self.coches_aparcados < self.plazas_maximas:
            return True
        
        return False
    
    def entrar_parking(self, coche):
        with self.condicion:
            # Esperar hasta que:
            # -Sea el primero de la cola
            # -Pueda aparcar
            while not self.es_primero_en_cola(coche) or not self.puede_cruzar():
                #print(f"{coche} esperando a entrar al parking")
                self.condicion.wait()
            
            print(f"El {coche} esta maniobrando")
            # Simular tiempo en entrar del parking
            time.sleep(coche.tiempo_entrar_salir)

            #Coche aparcado
            self.coches_aparcados += 1
            print(f"\tCoche [{coche}] está aparcado")

            # quitar el coche de la cola
            self.cola_parking.remove(coche)
            
            # Notificar al siguiente coche de la cola que ahora es su turno
            self.condicion.notify_all()

    def salir_parking(self, coche):
        # el tiempo aparcado, por el precio del parking
        total = coche.tiempo_aparcado * self.precio
        
        #Simula que el coche paga
        with self.condicion:
            self.total_acumulado += total
            print(f"Coche [{coche}] ha pagado: {total} $$. El parking tiene un total de ingresos de: {self.total_acumulado} $$.")
            # Que el coche sale
            self.coches_aparcados -= 1
            print(f"\t\t Saliendo [{coche}]")
            self.condicion.notify_all()
            
        # Simular tiempo en salir del parking
        time.sleep(coche.tiempo_entrar_salir)

        #Salio del parking
        print(f"\t\t Salio [{coche}]")

    
    