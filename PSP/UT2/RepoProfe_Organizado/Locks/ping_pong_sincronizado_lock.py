import threading

lock_ping = threading.Lock()
lock_pong = threading.Lock()

lock_pong.acquire()

def ping():
    global lock_ping, lock_pong
    while True:
        lock_ping.acquire()
        try:
            print("ping")
        except Exception as e:
            print(e)
        finally:
            lock_pong.release()


def pong():
    global lock_ping, lock_pong
    while True:
        lock_pong.acquire()
        try:
            print("\tpong")
        except Exception as e:
            print(e)
        finally:
            lock_ping.release()

hilo_ping = threading.Thread(target=ping)
hilo_pong = threading.Thread(target=pong)


hilo_ping.start()
hilo_pong.start()


