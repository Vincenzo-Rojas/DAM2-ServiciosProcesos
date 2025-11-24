from threading import Thread, Lock
import time

lock_1 = Lock()
lock_2 = Lock()

lock_2.acquire()

def ping(lock_1, lock_2):
    while True:
        lock_1.acquire()
        print("PING")
        time.sleep(0.05)
        lock_2.release()
        
def pong(lock_1, lock_2):
    while True:
        lock_2.acquire()
        print("\t\tPONG")
        time.sleep(0.05)
        lock_1.release()

hilo_ping = Thread(target=ping, args=(lock_1, lock_2))
hilo_pong = Thread(target=pong, args=(lock_1, lock_2))

hilo_ping.start()
hilo_pong.start()
