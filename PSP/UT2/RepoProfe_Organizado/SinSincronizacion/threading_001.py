import threading

contador = 0
iteraciones = 100000  # Suficientes iteraciones para hacer probable la condición de carrera

def incrementar():
    global contador
    for _ in range(iteraciones):
        # Esta operación NO ES ATÓMICA: leer + modificar + escribir
        contador += 1
def restar():
    global contador
    for _ in range(iteraciones):
        # Esta operación NO ES ATÓMICA: leer + modificar + escribir
        contador -= 1

# Crear y ejecutar hilos
hilo1 = threading.Thread(target=incrementar)
hilo2 = threading.Thread(target=incrementar)
hilo3 = threading.Thread(target=restar)

hilo1.start()
hilo2.start()
hilo3.start()

hilo1.join()
hilo2.join()
hilo3.join()

print(contador)