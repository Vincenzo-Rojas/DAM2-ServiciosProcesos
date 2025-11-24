import subprocess
import time

proceso_1 = subprocess.run(args=['clear'], capture_output=True, text=True)

def derecha():
    for i in range(20):
        print(proceso_1.stdout)
        print(" "*i, "**")
        time.sleep(0.08)

def izquierda():
    for i in range(20, -1, -1):
        print(proceso_1.stdout)
        print(" "*i, "**")
        time.sleep(0.08)

while True:
    derecha()
    izquierda()

