import time
import os

def usar_semaforo(semaforo, nombre_proceso):
    # Obtener el ID del proceso
    # Cada proceso tiene su propio contexto de ejecución
    pid = os.getpid()
    print(f"{nombre_proceso} (PID: {pid}) solicitando acceso al recurso")
    
    # Adquirir el semáforo (operación de espera)
    # Si el semáforo está en 0, el proceso se bloquea hasta que esté disponible
    semaforo.acquire()
    print(f"{nombre_proceso} (PID: {pid}) ha adquirido el recurso")
    
    # Simular uso del recurso compartido
    # Durante este tiempo, otros procesos están bloqueados si el semáforo es binario
    print(f"{nombre_proceso} (PID: {pid}) usando el recurso compartido...")
    time.sleep(2)
    
    # Liberar el semáforo (operación de señalización)
    # Esto permite que otro proceso pueda adquirir el recurso
    semaforo.release()
    print(f"{nombre_proceso} (PID: {pid}) ha liberado el recurso")
    
    # El semáforo es un mecanismo de sincronización que evita condiciones de carrera
    # y asegura la exclusión mutua en regiones críticas
