from concurrent.futures import ThreadPoolExecutor
import threading
from threading import Lock

lock = Lock()
i = 1

def saludo():
    global i
    with lock:
        print(f"hola desde el hilo: {threading.current_thread().name}, el valor de i es: {i}")
        i = i + 1

with ThreadPoolExecutor(4) as executor:
    for _ in range(100):
        executor.submit(saludo)