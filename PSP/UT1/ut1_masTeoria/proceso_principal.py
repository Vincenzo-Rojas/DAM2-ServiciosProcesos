import multiprocessing as mp
import time
from procesos_hijos import calcular_cuadrado, calcular_cubo
from sincronizacion import usar_semaforo
from comunicacion import usar_cola, usar_pipe

def main():
    # Crear un proceso principal que coordina múltiples tareas
    # Esto simula el proceso padre que crea procesos hijos
    print("Iniciando proceso principal")
    
    # Crear una cola para comunicación entre procesos
    # Las colas permiten enviar y recibir mensajes de forma asíncrona
    cola = mp.Queue()
    
    # Crear un pipe (tubería) para comunicación bidireccional
    # Los pipes son mecanismos de comunicación basados en buffers temporales
    extremo_padre, extremo_hijo = mp.Pipe()
    
    # Crear un semáforo para controlar el acceso a recursos compartidos
    # Los semáforos gestionan el acceso a recursos mediante operaciones de espera y señalización
    semaforo = mp.Semaphore(2)  # Permite hasta 2 procesos simultáneos
    
    # Crear procesos hijos para ejecutar tareas en paralelo
    # Cada proceso es una instancia independiente del programa
    p1 = mp.Process(target=calcular_cuadrado, args=(5,))
    p2 = mp.Process(target=calcular_cubo, args=(3,))
    p3 = mp.Process(target=usar_semaforo, args=(semaforo, "Proceso 3"))
    p4 = mp.Process(target=usar_semaforo, args=(semaforo, "Proceso 4"))
    p5 = mp.Process(target=usar_cola, args=(cola, "Mensaje desde proceso 5"))
    p6 = mp.Process(target=usar_pipe, args=(extremo_hijo, "Datos desde proceso 6"))
    
    # Iniciar todos los procesos hijos
    # Al iniciar un proceso, el sistema operativo crea una nueva instancia
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    
    # Enviar un mensaje a través del pipe desde el proceso principal
    # Esto demuestra la comunicación bidireccional entre procesos
    extremo_padre.send("Hola desde el proceso principal")
    
    # Esperar a que todos los procesos hijos terminen
    # La terminación de procesos puede hacerse con sys.exit() o os._exit()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    
    # Recibir respuesta del pipe
    # Las tuberías permiten comunicación entre procesos relacionados (padre-hijo)
    if extremo_padre.poll():
        respuesta = extremo_padre.recv()
        print(f"Respuesta recibida en proceso principal: {respuesta}")
    
    # Recibir mensajes de la cola
    # Las colas de mensajes son útiles cuando no se quiere compartir memoria
    while not cola.empty():
        mensaje = cola.get()
        print(f"Mensaje recibido en proceso principal: {mensaje}")
    
    print("Proceso principal finalizado")

if __name__ == "__main__":
    main()
