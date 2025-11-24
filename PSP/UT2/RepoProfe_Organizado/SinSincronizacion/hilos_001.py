import threading

def saludo():
    print(f"Hola, soy el hilo : {threading.current_thread().name}")

saludo()

h_2 = threading.Thread(target=saludo, name="HiloHermano")
h_2.start()