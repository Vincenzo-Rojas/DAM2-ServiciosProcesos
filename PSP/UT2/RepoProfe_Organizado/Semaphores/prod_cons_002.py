from threading import Thread, Semaphore, Lock
import threading
import time


inventario_max = 10

semaforo_piezas = Semaphore(inventario_max)
semaforo_producto_final = Semaphore(0)

productos_terminados = 0

lock = Lock()


def hacer_pieza(s_piezas, s_productos):
    global inventario_max
    while True:
        s_piezas.acquire() # entramos a producir piezas
        print(f"[{threading.current_thread().name}]Inicio producción pieza")
        time.sleep(2)
        print(f"[{threading.current_thread().name}]Pieza producida, hay: {inventario_max - s_piezas._value}")
        s_productos.release() # permitir la producción de un producto final

def consumir_pieza(s_piezas, s_productos, bloqueo):
    global productos_terminados
    while True:
        s_productos.acquire()
        print("Inicio producción final")
        time.sleep(3)
        with bloqueo:
            productos_terminados += 1
            print(f"Producto final terminado, en total hay {productos_terminados}")
        s_piezas.release()


productores = []
consumidores = []

for i in range(2):
    p = Thread(target=hacer_pieza,name=f"Productor_{i}" ,args=(semaforo_piezas, semaforo_producto_final))
    productores.append(p)

for j in range(5):
    c = Thread(target=consumir_pieza, args=(semaforo_piezas, semaforo_producto_final, lock))
    consumidores.append(c)

for p in productores:
    p.start()
for c in consumidores:
    c.start()
