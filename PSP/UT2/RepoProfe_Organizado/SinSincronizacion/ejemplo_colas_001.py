import threading
import queue
import time
import random

cola = queue.Queue()

def producir():
    global cola
    while True:
        num = random.randint(1,100)
        cola.put(num)
        print(f"\tel productor ha producido el valor {num}")
        time.sleep(0.5)

def consumir():
    global cola
    while True:
        try:
            num = cola.get()
            print(f"el consumidor ha consumido el valor {num}")
            time.sleep(2)
        except queue.Empty:
            print("La cola está vacía")
        except Exception as e:
            print(e)
    




hilo_productor = threading.Thread(target=producir)
hilo_consumidor = threading.Thread(target=consumir)

hilo_productor.start()
hilo_consumidor.start()