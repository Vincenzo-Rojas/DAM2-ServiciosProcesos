from threading import Thread, Semaphore
import time


inventario_max = 10

semaforo_piezas = Semaphore(inventario_max)
semaforo_producto_final = Semaphore(0)

productos_terminados = 0


def hacer_pieza(s_piezas, s_productos):
    global inventario_max
    while True:
        s_piezas.acquire() # entramos a producir piezas
        print("Inicio producción pieza")
        time.sleep(2)
        print(f"Pieza producida, hay: {inventario_max - s_piezas._value}")
        s_productos.release() # permitir la producción de un producto final

def consumir_pieza(s_piezas, s_productos):
    global productos_terminados
    while True:
        s_productos.acquire()
        print("Inicio producción final")
        time.sleep(3)
        productos_terminados += 1
        print(f"Producto final terminado, en total hay {productos_terminados}")
        s_piezas.release()

productor = Thread(target=hacer_pieza, args=(semaforo_piezas, semaforo_producto_final))
consumidor = Thread(target=consumir_pieza, args=(semaforo_piezas, semaforo_producto_final))

productor.start()
consumidor.start()