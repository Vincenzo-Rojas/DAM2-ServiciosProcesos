# Demostracion de race condition y uso de Lock para exclusión mutua.

# 03_sincronizacion_lock.py
# Este programa demuestra race conditions y cómo usar Lock para exclusión mutua.
# Varios procesos incrementan un contador compartido de manera segura usando un lock.

from multiprocessing import Process, Lock, Manager  # Para procesos, locks y variables compartidas
import time  # Para pausas pequeñas y simular trabajo
import os    # Para obtener PID de cada proceso

# Función que incrementa una variable compartida
def incrementar(shared, key, vueltas, lock):
    pid = os.getpid()  # PID del proceso
    for _ in range(vueltas):
        with lock:  # Exclusión mutua para evitar race condition
            shared[key] += 1
        time.sleep(0.001)  # Pausa pequeña para simular tiempo de ejecución
    print(f'Proceso {pid} finalizado')  # Indicar que el proceso terminó

# Ejemplo de uso de lock con varios procesos
def ejemplo_con_lock(vueltas=200, n=3):
    mgr = Manager()  # Manager para variables compartidas
    shared = mgr.dict()  # Diccionario compartido
    shared['contador'] = 0
    lock = Lock()  # Lock para exclusión mutua
    ps = []  # Lista de procesos
    # Crear y lanzar procesos
    for _ in range(n):
        p = Process(target=incrementar, args=(shared, 'contador', vueltas, lock))
        ps.append(p)
        p.start()
    # Esperar a que terminen todos los procesos
    for p in ps:
        p.join()
    print('Valor final (con lock):', shared['contador'])  # Mostrar resultado final

# Función principal
def main():
    ejemplo_con_lock()

if __name__=='__main__':
    main()
