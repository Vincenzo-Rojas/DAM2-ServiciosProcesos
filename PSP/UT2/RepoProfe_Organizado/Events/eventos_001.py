from threading import Event, Thread
import time

evento = Event()

def counting():
    i = 0
    while not evento.is_set():
        print(i)
        i = i + 1

hilo = Thread(target=counting)
hilo.start()

time.sleep(5)
evento.set()


