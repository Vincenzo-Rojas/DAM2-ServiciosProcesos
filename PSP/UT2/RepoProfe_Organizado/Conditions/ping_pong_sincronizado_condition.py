import threading

lock = threading.Condition()
turno = True

def ping():
    global lock, turno
    with lock:
        while True:
            while turno:
                lock.wait()
            print("ping")
            turno = not turno
            lock.notify()


def pong():
    global lock, turno
    with lock:
        while True:
            while not turno:
                lock.wait()
            print("\tpong")
            turno = not turno
            lock.notify()

hilo_ping = threading.Thread(target=ping)
hilo_pong = threading.Thread(target=pong)


hilo_ping.start()
hilo_pong.start()


