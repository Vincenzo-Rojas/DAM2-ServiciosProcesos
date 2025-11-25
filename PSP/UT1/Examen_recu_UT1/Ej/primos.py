from multiprocessing import Process, Value, Lock  # Para procesos y variables compartidas

lista_numeros = [x for x in range(1, 10001)]  # Lista de números del 1 al 100
valor = Value("i", 0)  # Variable compartida para acumular la suma
lock = Lock()

# Mostrar las partes de la lista
'''
print(lista_numeros[:len(lista_numeros) // 3])  
print(lista_numeros[len(lista_numeros) // 3 : (len(lista_numeros) // 3)*2:])  
print(lista_numeros[(len(lista_numeros) // 3)*2: ])  
'''
# Función que suma los elementos de una lista parcial y actualiza la variable compartida
def suma_primo(lista, valor, lock):
    for i in lista:
        # comprobar que es primo
        if comprobar_primo(i):
            with lock:  # Bloqueo implícito para acceso seguro
                valor.value += 1

def comprobar_primo(numero):
    if numero == 1:
        return False
    
    elif numero==2:
        return True
    
    elif numero%2==0:
        return False
    
    else:
        for i in range(3,numero,1):
            if numero%i == 0:
                return False
        return True    
        

# Crear procesos para sumar cada mitad de la lista
p_1 = Process(target=suma_primo, args=(lista_numeros[:len(lista_numeros)//3], valor, lock))
p_2 = Process(target=suma_primo, args=(lista_numeros[len(lista_numeros) // 3 : (len(lista_numeros) // 3)*2:], valor, lock))
p_3 = Process(target=suma_primo, args=(lista_numeros[(len(lista_numeros) // 3)*2: ], valor, lock))

# Iniciar ambos procesos
p_1.start()
p_2.start()
p_3.start()

# Esperar a que ambos procesos terminen
p_1.join()
p_2.join()
p_3.join()


print(f"El numero de primos {valor.value}")  # Imprime la suma total de la lista (resultado esperado: 5050)
