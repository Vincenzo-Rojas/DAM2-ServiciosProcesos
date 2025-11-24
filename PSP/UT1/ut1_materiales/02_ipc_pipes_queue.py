# Ejemplos de Pipe y Queue para IPC.

# 02_ipc_pipes_queue.py
# Este programa muestra ejemplos de IPC (Inter-Process Communication) usando Pipe y Queue.
# Pipe: comunicación directa entre padre e hijo.
# Queue: comunicación segura entre productor y consumidor.

from multiprocessing import Process, Pipe, Queue  # Para procesos y mecanismos de IPC
import os  # Para obtener PID
import sys  # Para leer argumentos del programa

# Función del proceso hijo que usa Pipe
def worker_pipe(conn):
    try:
        msg = conn.recv()  # Recibir mensaje del padre
    except EOFError:
        print('Hijo: conexion cerrada')
        return
    print(f'Hijo (PID {os.getpid()}): recibido -> {msg}')
    conteo = sum(1 for c in msg if c.isalpha())  # Contar letras
    conn.send(conteo)  # Enviar resultado al padre
    conn.close()

# Ejemplo de Pipe
def ejemplo_pipe():
    parent_conn, child_conn = Pipe()  # Crear Pipe bidireccional
    p = Process(target=worker_pipe, args=(child_conn,))
    p.start()
    texto = 'Hola Mundo' if len(sys.argv) <= 1 else sys.argv[1]  # Texto a enviar
    parent_conn.send(texto)  # Enviar al hijo
    res = parent_conn.recv()  # Recibir resultado del hijo
    print(f'Padre: el hijo contó {res} letras')
    p.join()  # Esperar a que termine el hijo

# Función del productor que pone items en la Queue
def productor(q, items):
    for it in items:
        q.put(it)
    q.put(None)  # Señal de fin

# Función del consumidor que lee items de la Queue
def consumidor(q):
    total = 0
    while True:
        item = q.get()
        if item is None:  # Detecta fin
            break
        total += sum(1 for c in item if c.isalpha())  # Contar letras
    print(f'Consumidor (PID {os.getpid()}): total={total}')

# Ejemplo de Queue
def ejemplo_queue():
    q = Queue()
    datos = ['hola', 'prueba', 'multiproceso']
    p_prod = Process(target=productor, args=(q, datos))
    p_cons = Process(target=consumidor, args=(q,))
    p_prod.start(); p_cons.start()
    p_prod.join(); p_cons.join()

# Función principal que ejecuta ambos ejemplos
def main():
    ejemplo_pipe()
    ejemplo_queue()

if __name__ == '__main__':
    main()
