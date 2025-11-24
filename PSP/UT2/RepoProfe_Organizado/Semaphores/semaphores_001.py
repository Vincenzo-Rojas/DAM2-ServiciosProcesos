from threading import Semaphore, Thread
import time
import random

semaforo = Semaphore(10)

def descarga(num):
    semaforo.acquire()
    print(f"Inicia la descarga número :{num}")
    time.sleep(random.randrange(1,5))
    print(f"Termina la descarga número : {num}")
    semaforo.release()

for i in range(20):
    Thread(target=descarga, args=(i,)).start()