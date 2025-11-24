""" Ejercicio 1: Multiprocesos y fork

Enunciado:
Escribe un programa que cree un proceso hijo usando os.fork(). El proceso padre debe ejecutar un comando del sistema (ls en Linux o dir en Windows) 
usando subprocess.run y enviar la salida a un fichero. El hijo debe contar el número de líneas del mismo fichero y mostrarlo.

Pregunta: ¿Qué sucede si el padre termina antes de que el hijo lea el fichero? ¿Se garantiza que el hijo tenga todas las líneas?

Respuesta correcta:

Si el padre termina antes de que el hijo lea el fichero, no hay problema porque el fichero ya ha sido escrito en el disco (subprocess.run bloquea hasta terminar).

Se garantiza que el hijo lea todas las líneas, siempre que espere a que el fichero se cierre.

Código clave:
        """

pid = os.fork()
if pid != 0:  # padre
    subprocess.run(['ls','-la'], stdout=open('salida.txt','w'))
else:  # hijo
    with open('salida.txt') as f:
        print(len(f.readlines()))

        
""" Ejercicio 2: Race condition y locks

Enunciado:
Se tienen 4 procesos que incrementan una variable compartida 1000 veces cada uno. Si no se usa Lock, el valor final es menor que el esperado.

Pregunta:

¿Por qué ocurre esto?

Implementa la versión correcta usando multiprocessing.Value y Lock para garantizar el valor esperado.

Respuesta correcta:

Ocurre porque varios procesos acceden al mismo valor simultáneamente (race condition).

Código con lock:
"""
from multiprocessing import Process, Value, Lock

valor = Value('i', 0)
lock = Lock()

def incrementar(valor):
    for _ in range(1000):
        with lock:
            valor.value += 1

procesos = [Process(target=incrementar, args=(valor,)) for _ in range(4)]
for p in procesos: p.start()
for p in procesos: p.join()

print(valor.value)  # Debe imprimir 4000
        
"""Ejercicio 3: Pipes y Queue

Enunciado:
Crea un programa donde un proceso padre genere números del 1 al 100 y los envíe a un hijo por Pipe. El hijo debe calcular la suma de los pares y enviarla de vuelta al padre.

Pregunta: ¿Qué ventaja tendría usar Queue en vez de Pipe para este mismo ejercicio si queremos más de un hijo procesando diferentes rangos simultáneamente?

Respuesta correcta:

Queue permite varios consumidores leyendo de manera segura sin necesidad de locks explícitos.

Con Pipe, se necesitaría crear una tubería por cada hijo y sincronizar cuidadosamente.

        """
""" Ejercicio 4: Signals y control de procesos

Enunciado:
Se quiere simular una carrera de dromedarios controlada por señales. Cada dromedario avanza cuando el usuario pulsa Enter, enviando SIGUSR1 o SIGUSR2 al gestor.

Pregunta:

¿Qué ocurre si ambos dromedarios reciben la señal exactamente al mismo tiempo?

¿Cómo evitar que la posición de los dromedarios se corrompa si se ejecuta simultáneamente la función que incrementa posiciones?

Respuesta correcta:

Puede ocurrir condición de carrera, mostrando posiciones incorrectas.

Se puede usar multiprocessing.Lock o threading.Lock para proteger la sección donde se actualiza posiciones_dromedarios.

        """
"""Ejercicio 5: Subprocess y fork combinados

Enunciado:
Escribe un programa que haga os.fork(). El padre ejecuta un comando ls -la usando subprocess.run y lo guarda en un fichero. 
El hijo espera a que el padre termine usando os.wait() y luego imprime solo los ficheros .py del listado usando grep como subproceso.

Pregunta: ¿Qué pasa si no se usa os.wait() en el hijo?

Respuesta correcta:

Si no se usa os.wait(), el hijo puede intentar leer el fichero antes de que el padre lo haya escrito completo, generando resultados incompletos.

Con os.wait(), se garantiza que el padre terminó antes de que el hijo lea.

        """
"""Ejercicio 6: Continuación de conteo con signals

Enunciado:
Se tiene un contador controlado por señales: SIGUSR1 para empezar desde 0, SIGUSR2 para parar, y SIGINT para continuar.

Pregunta:

Explica por qué el contador puede bloquearse si la función de SIGUSR1 entra en un bucle while contando:.

¿Cómo se puede mejorar para que las señales puedan interrumpir el bucle inmediatamente?

Respuesta correcta:

Bloqueo ocurre porque Python no interrumpe un bucle largo por señales hasta que la función retorna o hace operaciones bloqueables.

Solución: usar loops cortos con time.sleep(0.01) y chequear contando en cada iteración, o usar multiprocessing.Process en vez de bucles infinitos en la señal.
"""

"""Ejercicio 7: Fork + Lock + Variable compartida

Enunciado:
Se crea un proceso padre que inicializa un multiprocessing.Value con 0 y un Lock. Luego hace os.fork() para crear un hijo. 
Tanto padre como hijo incrementan la variable 500 veces usando el lock.

Pregunta:

¿Cuál es el valor final esperado de la variable si ambos usan correctamente el lock?

¿Qué pasaría si se eliminara el lock?

Respuesta correcta:

Valor final esperado: 1000 (500 del padre + 500 del hijo).

Sin lock, ocurre race condition y el valor puede ser menor que 1000.

Código:
"""
from multiprocessing import Value, Lock  # Para variable compartida y exclusión mutua
import os  # Para fork y wait

# Variable compartida entera inicializada a 0
contador = Value('i', 0)

# Lock para evitar race condition
lock = Lock()

# Función que incrementa la variable 500 veces usando lock
def incrementar(v):
    for _ in range(500):
        with lock:  # Solo un proceso puede modificar la variable a la vez
            v.value += 1

# Crear proceso hijo
pid = os.fork()
if pid != 0:  # Padre
    incrementar(contador)  # Incrementa 500 veces
    os.wait()  # Espera a que el hijo termine
    print("Valor final esperado (padre+hijo):", contador.value)  # Debe ser 1000
else:  # Hijo
    incrementar(contador)  # Incrementa 500 veces
    os._exit(0)  # Termina el hijo

"""Ejercicio 8: Pipe + fork con sincronización

Enunciado:
Un proceso padre crea un Pipe() y hace os.fork(). El hijo recibe un mensaje del padre, lo transforma a mayúsculas y lo devuelve por el mismo pipe.

Pregunta:

Si el padre hace pipe.recv() antes de pipe.send(), ¿qué ocurre?

¿Cómo se puede evitar que el padre quede bloqueado indefinidamente?

Respuesta correcta:

El padre queda bloqueado esperando porque el hijo aún no ha enviado el mensaje.

Se puede usar pipe.poll(timeout) para comprobar si hay datos antes de recibir.

Código:

"""
from multiprocessing import Pipe  # Para comunicación entre procesos
import os  # Para fork

# Crear un pipe bidireccional
parent_conn, child_conn = Pipe()

# Crear proceso hijo
pid = os.fork()
if pid != 0:  # Padre
    mensaje = "hola mundo"
    parent_conn.send(mensaje)  # Enviar mensaje al hijo
    # Esperar hasta 5 segundos para recibir respuesta
    if parent_conn.poll(5):  # poll devuelve True si hay datos listos
        respuesta = parent_conn.recv()  # Recibir respuesta del hijo
        print("Padre recibió:", respuesta)
    else:
        print("No llegó respuesta del hijo")
    os.wait()  # Esperar a que el hijo termine
else:  # Hijo
    msg = child_conn.recv()  # Recibir mensaje del padre
    child_conn.send(msg.upper())  # Enviar mensaje en mayúsculas de vuelta
    os._exit(0)  # Termina el hijo


"""Ejercicio 10: Señales + subprocess

Enunciado:
Un script lanza un subproceso que hace un bucle infinito. El script principal captura SIGINT (Ctrl+C) 
y al recibirlo hace os.kill(pid_subproceso, SIGTERM) para terminarlo.

Pregunta:

¿Qué pasa si el subproceso tiene su propio handler para SIGINT?

¿Cómo garantizar que el subproceso muera cuando el padre recibe la señal?

Respuesta correcta:

Si el subproceso captura SIGINT, no termina automáticamente, ignorando la señal de Ctrl+C.

Para garantizar que muera, el padre debe enviar SIGTERM o SIGKILL, o crear un grupo de procesos y mandar la señal al grupo.

Código:
"""
import subprocess  # Para lanzar subprocesos
import signal      # Para manejar señales
import os
import time

# Lanzar subproceso que ejecuta bucle infinito
p = subprocess.Popen(["python3","-c","while True: pass"])

# Función para terminar el subproceso al recibir SIGINT
def terminar_subproceso(signum, frame):
    print("Padre recibe SIGINT, matando subproceso...")
    os.kill(p.pid, signal.SIGTERM)  # Manda SIGTERM al subproceso

# Registrar el handler para SIGINT
signal.signal(signal.SIGINT, terminar_subproceso)

# Esperar a que el subproceso termine
try:
    while p.poll() is None:  # poll() devuelve None si sigue vivo
        time.sleep(0.5)
except KeyboardInterrupt:
    pass


"""Ejercicio 11: Carrera de dromedarios y locks

Enunciado:
Se tiene un programa de carrera de dromedarios donde múltiples usuarios envían señales para avanzar. Cada señal hace que se incremente la posición del dromedario en una variable global.

Pregunta:

¿Por qué podría mostrarse una posición incorrecta si varios usuarios envían señales al mismo tiempo?

Propón una solución usando multiprocessing.

Respuesta correcta:

El problema ocurre por race condition al modificar la variable global simultáneamente.

Solución: usar multiprocessing.Lock() alrededor de la sección crítica donde se actualiza la posición.

Código:

"""
import signal
import multiprocessing
import time
import random

# Lock para proteger la sección crítica
lock = multiprocessing.Lock()

# Posiciones iniciales de los dromedarios
posiciones = multiprocessing.Array('i', [0,0])
meta = 20  # Meta de la carrera

# Función para avanzar un dromedario
def avanzar(num):
    with lock:  # Protección contra race condition
        if random.random() > 0.2:  # Probabilidad de tropiezo
            posiciones[num] += 1
        print(f"Dromedario {num} posición: {posiciones[num]}")

# Handler que asigna señales a cada dromedario
def handler(signum, frame):
    avanzar(0 if signum==signal.SIGUSR1 else 1)

# Registrar handlers
signal.signal(signal.SIGUSR1, handler)
signal.signal(signal.SIGUSR2, handler)

print("PID gestor:", os.getpid())
# Loop principal que espera señales hasta que un dromedario llegue a la meta
while max(posiciones) < meta:
    signal.pause()  # Espera señal sin consumir CPU

print("Carrera finalizada:", list(posiciones))
