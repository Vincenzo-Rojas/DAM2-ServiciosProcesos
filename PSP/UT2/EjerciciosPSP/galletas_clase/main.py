from abuela import Abuela
from mesa import Mesa
from nieto import Nieto
from threading import Thread

#Crea objetos Abuela, 3 nietos, y la mesa
i_mesa = Mesa(huecos=100)
i_abuela = Abuela(galletas_bandeja=5,tiempo_cocinado=1,mesa=i_mesa)
i_nietos = [
    Nieto(tiempo_galleta=1/3,limite_hambre=10,tiempo_descanso=3, mesa=i_mesa) 
    for i in range (3)]

#Crea los hilos
h_abuela = Thread(target=i_abuela.hacer_galletas)
h_nietos = []
for nieto in i_nietos:
    h_nietos.append(Thread(target=nieto.comer_galleta))

#iniciar los hilos
h_abuela.start()
for nieto in h_nietos:
    nieto.start()