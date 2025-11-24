import threading

lock = threading.Condition()
turno = True

def ping():
    global lock, turno    
    while True:
        lock.acquire()
        try:
            while not turno:
                lock.wait()
            print("ping")
            turno = not turno
            lock.notify()
        except Exception as e:
            print(e)
        finally:
            lock.release()


def pong():
    global lock, turno
    while True:
        lock.acquire()
        try:
            while turno:
                lock.wait()
            print("\tpong")
            turno = not turno
            lock.notify()
        except Exception as e:
            print(e)
        finally:
            lock.release()

hilo_ping = threading.Thread(target=ping)
hilo_pong = threading.Thread(target=pong)


hilo_ping.start()
hilo_pong.start()


