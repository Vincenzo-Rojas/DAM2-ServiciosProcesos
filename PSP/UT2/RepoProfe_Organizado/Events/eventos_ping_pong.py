from threading import Event, Thread
import time


evento = Event()

def ping():
    while True:
        if not evento.is_set():
            print("PING...")
            time.sleep(0.05)
            evento.set()

def pong():
    while True:
        if evento.is_set():
            print("\t\t\tPONG")
            time.sleep(0.05)
            evento.clear()

h_ping = Thread(target=ping)
h_pong = Thread(target=pong)

h_ping.start()
h_pong.start()
