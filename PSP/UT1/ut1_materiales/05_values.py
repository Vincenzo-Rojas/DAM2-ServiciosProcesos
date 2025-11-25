from multiprocessing import Process, Value

def incrementar(x):
    x.value += 1

if __name__ == "__main__":
    v = Value('i', 0)
    p1 = Process(target=incrementar, args=(v,))
    p2 = Process(target=incrementar, args=(v,))
    
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    
    print(v.value)  # Resultado esperado: 2