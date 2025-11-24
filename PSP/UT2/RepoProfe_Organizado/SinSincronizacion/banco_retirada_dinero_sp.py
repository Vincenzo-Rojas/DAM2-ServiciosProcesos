import threading
import time

class Cuenta:
    def __init__(self, saldo):
        self.saldo = saldo

    def retirar(self, cantidad):
        print(f"{threading.current_thread().name} intentando retirar {cantidad}€")
        if self.saldo >= cantidad:
            print(f"{threading.current_thread().name} comprobó que hay suficiente saldo ({self.saldo}€)")
            time.sleep(1)  # Simulamos el tiempo que tarda el cajero
            self.saldo -= cantidad
            print(f"{threading.current_thread().name} retiró {cantidad}€. Saldo restante: {self.saldo}€")
        else:
            print(f"{threading.current_thread().name} no puede retirar {cantidad}€ (saldo: {self.saldo}€)")

cuenta = Cuenta(50)

# Dos hilos que intentan retirar dinero a la vez
t1 = threading.Thread(target=cuenta.retirar, args=(40,), name="Persona-1")
t2 = threading.Thread(target=cuenta.retirar, args=(30,), name="Persona-2")

t1.start()
t2.start()
t1.join()
t2.join()