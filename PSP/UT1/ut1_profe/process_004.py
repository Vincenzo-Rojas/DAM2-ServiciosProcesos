# Este programa crea dos procesos que se comunican de forma sincronizada.
# Uno imprime "ping" y otro "pong" de manera alterna usando locks.

import time
from multiprocessing import Process, Lock  # Para crear procesos y sincronizarlos

lock_1 = Lock()  # Lock para el proceso ping
lock_2 = Lock()  # Lock para el proceso pong

lock_2.acquire()  # Bloquea pong al inicio para que ping empiece primero

def ping(lock_1, lock_2):
    while True:
        lock_1.acquire()  # Espera a que ping pueda ejecutarse
        print("ping")  # Imprime "ping"
        time.sleep(0.2)  # Pausa para ver el efecto
        lock_2.release()  # Desbloquea pong

def pong(lock_1, lock_2):
    while True:
        lock_2.acquire()  # Espera a que pong pueda ejecutarse
        print("\t\tpong")  # Imprime "pong" con tabulación
        time.sleep(0.2)  # Pausa para ver el efecto
        lock_1.release()  # Desbloquea ping

# Crear y lanzar procesos ping y pong
Process(target=ping, args=(lock_1, lock_2)).start()
Process(target=pong, args=(lock_1, lock_2)).start()
