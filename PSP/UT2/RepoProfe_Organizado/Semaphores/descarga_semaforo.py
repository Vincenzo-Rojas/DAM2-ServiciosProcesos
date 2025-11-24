import threading
import time


semaforo = threading.Semaphore(3)

def descarga(num):
    global semaforo
    semaforo.acquire()
    time.sleep(3)
    print(f"descarga {num} terminada!")
    semaforo.release()

hilos = []

for i in range(100):
    hilo = threading.Thread(target=descarga, args=(i,))
    hilos.append(hilo)
    hilo.start()

for h in hilos:
    h.join()

print("Descargas completadas")