import threading

def ping():
    while True:
        print("ping")

def pong():
    while True:
        print("\tpong")

hilo_ping = threading.Thread(target=ping)
hilo_pong = threading.Thread(target=pong)


hilo_ping.start()
hilo_pong.start()


