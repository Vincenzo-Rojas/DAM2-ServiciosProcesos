import time
import os

def usar_cola(cola, mensaje):
    # Obtener el ID del proceso
    # Cada proceso tiene su propio espacio de memoria independiente
    pid = os.getpid()
    print(f"Proceso usar_cola (PID: {pid}) iniciado")
    
    # Enviar mensaje a la cola
    # Las colas de mensajes permiten comunicación asíncrona entre procesos
    cola.put(f"{mensaje} (desde PID: {pid})")
    print(f"Mensaje enviado a la cola por proceso {pid}")
    
    # Simular trabajo
    # Durante este tiempo, otros procesos pueden acceder a recursos
    time.sleep(0.5)
    
    # Finalizar proceso
    # El proceso pasa al estado terminado y se libera su contexto
    print(f"Proceso usar_cola (PID: {pid}) finalizado")

def usar_pipe(extremo_pipe, datos):
    # Obtener el ID del proceso
    # Cada proceso es una instancia independiente del programa
    pid = os.getpid()
    print(f"Proceso usar_pipe (PID: {pid}) iniciado")
    
    # Enviar datos a través del pipe
    # Las tuberías son mecanismos de comunicación unidireccionales
    extremo_pipe.send(f"{datos} (PID: {pid})")
    print(f"Datos enviados por el pipe desde proceso {pid}")
    
    # Esperar y recibir respuesta
    # Los pipes permiten comunicación bidireccional si se usan dos tuberías
    if extremo_pipe.poll():
        respuesta = extremo_pipe.recv()
        print(f"Respuesta recibida en proceso {pid}: {respuesta}")
    
    # Simular trabajo
    # El proceso puede estar en estado de ejecución o espera
    time.sleep(0.5)
    
    # Finalizar proceso
    # El proceso terminado debe ser recolectado por el proceso padre
    print(f"Proceso usar_pipe (PID: {pid}) finalizado")
