from threading import Thread, Lock
import time

# PING PONG con hilos y exclusión mutua
def ping(lock):
    while True:
        with lock:         
            print("PING")
            time.sleep(0.5)

def pong(lock):
    while True:
        with lock:
            print("\t\tPONG")
            time.sleep(0.5)

hilo_ping = Thread(target=ping)
hilo_pong = Thread(target=pong)

hilo_ping.start()
hilo_pong.start()
