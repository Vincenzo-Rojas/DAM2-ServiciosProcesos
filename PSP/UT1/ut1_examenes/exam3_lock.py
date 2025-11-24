# exam3_lock.py
# Ejercicio 3 — Exclusión mutua: contador compartido protegido por Lock.
# Enunciado:
# - Implementa 'worker_increment(shared, key, n, lock)' que incrementa shared[key] n veces
#   protegiendo la sección crítica con lock.
# - El script lanzará 3 procesos que hagan 200 incrementos cada uno. Valor esperado final = 600.
#
# Autoevaluación:
# - Si el contador final es 600, imprime 'RESULTADO: OK'.

from multiprocessing import Process, Manager, Lock
import os
import sys
import time

def worker_increment(shared, key, n, lock):
    # Realiza n incrementos protegiendo con lock.
    for _ in range(n):
        # Sección crítica: lectura y escritura de shared[key]
        with lock:
            shared[key] += 1
        # Pequeña espera para aumentar posibilidad de intercalado
        time.sleep(0.0005)

def main():
    mgr = Manager()
    shared = mgr.dict()
    shared['contador'] = 0
    lock = Lock()
    procesos = []
    n_procesos = 3
    n_incrementos = 200
    # Crear y arrancar procesos
    for _ in range(n_procesos):
        p = Process(target=worker_increment, args=(shared, 'contador', n_incrementos, lock))
        procesos.append(p)
        p.start()
    # Esperar a que terminen
    for p in procesos:
        p.join()
    # Comprobación automática
    esperado = n_procesos * n_incrementos
    obtenido = shared['contador']
    print('Valor obtenido del contador:', obtenido)
    if obtenido == esperado:
        print('RESULTADO: OK')
        sys.exit(0)
    else:
        print('RESULTADO: FAIL')
        sys.exit(4)

if __name__ == '__main__':
    main()
