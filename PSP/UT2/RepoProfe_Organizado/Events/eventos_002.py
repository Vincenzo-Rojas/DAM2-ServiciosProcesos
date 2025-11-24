from threading import Event, Thread
import time


evento = Event()

def counting():
    i = 0
    evento.wait()
    inicio = time.time()
    while time.time() - inicio < 10:    
        print(i)
        i = i + 1
        
hilo = Thread(target=counting, daemon=True)
hilo.start()

time.sleep(1)
evento.set()
hilo.join()