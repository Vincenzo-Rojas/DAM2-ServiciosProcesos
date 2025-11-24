import threading

def saludo():
    print(f"Hola, soy un hilo: {threading.current_thread().name}")

saludo()

hilo_2 = threading.Thread(target=saludo, name="Hilo_2")
hilo_2.start()


