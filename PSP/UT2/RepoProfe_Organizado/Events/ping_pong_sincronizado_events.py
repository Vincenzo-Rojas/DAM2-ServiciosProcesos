import threading

def ping():
    global event_ping, event_pong
    while True:
        while not event_ping.is_set():
            event_ping.wait()
        print("ping")
        event_ping.clear()
        event_pong.set()

def pong():
    global event_ping, event_pong
    while True:
        while not event_pong.is_set():
            event_pong.wait()
        print("\tpong")
        event_pong.clear()
        event_ping.set()


event_ping = threading.Event()
event_pong = threading.Event()

event_ping.set()

hilo_ping = threading.Thread(target=ping)
hilo_pong = threading.Thread(target=pong)

hilo_ping.start()
hilo_pong.start()
