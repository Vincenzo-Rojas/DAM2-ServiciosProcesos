from abuela import Abuela
from mesa import Mesa
from nieto import Nieto
from threading import Thread


mesa = Mesa(100)
abuela = Abuela("Andrea", mesa, 1, 10)
nietos = [Nieto(f"Nieto-{i}", mesa, 1/3, 10, 3) for i in range(3)]

# creamos los hilos de cada uno
hilo_abuela = Thread(target=abuela.hacer_galletas)
hilos_nietos = [Thread(target=nieto.comer_galletas) for nieto in nietos]

# iniciamos los hilos
hilo_abuela.start()
for hilo_nieto in hilos_nietos:
    hilo_nieto.start()


