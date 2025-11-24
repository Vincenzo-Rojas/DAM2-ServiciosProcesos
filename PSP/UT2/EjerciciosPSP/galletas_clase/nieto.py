import time

class Nieto:
    num_nietos = 1
    def __init__(self, tiempo_galleta,limite_hambre, tiempo_descanso, mesa):
        self.id_nieto = Nieto.num_nietos
        Nieto.num_nietos +=1
        self.tiempo_galleta = tiempo_galleta #tiempo en comer la galleta
        self.limite_hambre = limite_hambre
        self.tiempo_descanso = tiempo_descanso #descanso entre galltas a partir de limite_hambre
        self.mesa = mesa
        self.contador_galletas = 0
    
    def __str__(self):
        return f"NIETO_{self.id_nieto}"

    def comer_galleta(self):
        while True:
            print(f"El nieto {self} quiere comer galletas")
            while self.mesa.condition:
                while self.mesa.galletas <= 0:
                    self.mesa.condition.wait()
                self.mesa.coger_galleta()
                self.contador_galletas += 1
                print(f"El nieto {self} esta comiendo galleta, lleva {self.contador_galletas} galletas, en la mesa quedan {self.mesa.galletas}")
                self.mesa.condition.notify_all()
            time.sleep(self.tiempo_galleta)
            if self.contador_galletas >= self.limite_hambre:
                print(f"El nieto tiene mas de {self.limite_hambre} y esta descansando {self.tiempo_descanso}")
                time.sleep(self.tiempo_descanso)


    def comer_galleta2(self):
        while True:
            print(f"El nieto {self} quiere comer galletas")
            while self.mesa.condition:
                while self.mesa.galletas <= 0:
                    self.mesa.condition.wait()
                self.mesa.coger_galleta()
                print(f"El nieto {self} ha cogido galleta")
                self.contador_galletas += 1
                self.mesa.condition.notify_all()
            
            print(f"El nieto {self} se esta comiendo la galleta, lleva {self.contador_galletas}")
            time.time(self.tiempo_galleta)

            if self.contador_galletas > self.limite_hambre:
                print(f"El nieto tiene mas de {self.limite_hambre} y esta descansando {self.tiempo_descanso}")
                time.time(self.tiempo_descanso)


