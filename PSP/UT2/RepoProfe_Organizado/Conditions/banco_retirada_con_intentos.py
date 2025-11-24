import threading
import time
import random

class Cuenta:
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)

    def retirar(self, cantidad, intentos=3, timeout=3):
        with self.cond:
            print(f"{threading.current_thread().name} quiere retirar {cantidad}€")

            for intento in range(1, intentos + 1):
                if self.saldo >= cantidad:
                    # Hay suficiente saldo
                    print(f"{threading.current_thread().name} retira {cantidad}€ (saldo actual: {self.saldo}€)")
                    time.sleep(random.uniform(0.5, 1.5))
                    self.saldo -= cantidad
                    print(f"{threading.current_thread().name} retiró {cantidad}€. Saldo restante: {self.saldo}€")
                    return True
                else:
                    # No hay suficiente, esperar un poco
                    print(f"{threading.current_thread().name} (intento {intento}/{intentos}) espera saldo... (actual: {self.saldo}€)")
                    self.cond.wait(timeout=timeout)

            # Si llegó aquí, no ha conseguido sacar el dinero
            print(f"{threading.current_thread().name} se rindió tras {intentos} intentos. No pudo retirar {cantidad}€ (saldo: {self.saldo}€)")
            return False

    def ingresar(self, cantidad):
        with self.cond:
            print(f"🏦 {threading.current_thread().name} ingresa {cantidad}€")
            time.sleep(random.uniform(0.5, 1.5))
            self.saldo += cantidad
            print(f"📈 Nuevo saldo: {self.saldo}€")
            self.cond.notify_all()  # Despierta a los que estaban esperando


# --- Simulación ---
cuenta = Cuenta(50)

# Dos personas que quieren retirar más de lo que hay
t1 = threading.Thread(target=cuenta.retirar, args=(70,), name="Persona-1")
t2 = threading.Thread(target=cuenta.retirar, args=(60,), name="Persona-2")

# Un banco que ingresa dinero más tarde
t3 = threading.Thread(target=cuenta.ingresar, args=(30,), name="Banco")

t1.start()
t2.start()
time.sleep(5)  # El banco ingresa dinero después de un rato
t3.start()

t1.join()
t2.join()
t3.join()

print(f"\n Saldo final en la cuenta: {cuenta.saldo}€")
