from threading import Condition, Thread
import time

condition = Condition()
turno = True

def ping():
    global turno
    while True:
        with condition:
            if not turno:
                condition.wait()
            print("PING ...")
            time.sleep(0.05)
            turno = not turno
            condition.notify()

def pong():
    global turno
    while True:
        with condition:
            if turno:
                condition.wait()
            print("\t\t\tPONG")
            time.sleep(0.05)
            turno = not turno
            condition.notify()
                
h_ping = Thread(target=ping)
h_pong = Thread(target=pong)

h_ping.start()
h_pong.start()