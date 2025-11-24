import threading
import time
import random

mesa = [] # maximo 100
condition = threading.Condition()
MAX = 100


def Abuela():
    with condition: 
        while len(mesa) >= MAX: 
                condition.wait()
        if not len(mesa) >= MAX:
            mesa.append(10)
            print("add 10 galletas") 
            condition.notify() # alertar a consumidor 
        time.sleep(1)

def Nieto():
    pass






p = threading.Thread(target=Abuela)
c = threading.Thread(target=Nieto, daemon=True)

p.start()
c.start()
p.join()

































