# Este programa divide una lista en partes y suma sus elementos usando múltiples procesos.
# Cada proceso suma una porción de la lista y actualiza una variable compartida.
# Se puede especificar el número de procesos como argumento; por defecto son 4.

import sys
from multiprocessing import Process, Value  # Para crear procesos y variables compartidas

valor = Value("i", 0)  # Variable compartida donde se acumula la suma

# Función que suma los elementos de una lista parcial y actualiza la variable compartida
def suma_par(lista, valor):
    res = 0
    for i in lista:
        res += i
    with valor:  # Bloqueo implícito para acceso seguro
        valor.value += res

# Número de procesos a usar
if len(sys.argv) != 2:
    num_proc = 4  # Por defecto 4 procesos
else:
    num_proc = int(sys.argv[1])  # Número de procesos pasado como argumento

lista = [x for x in range(1, 101)]  # Lista de números del 1 al 100


'''print(lista[2*3:])#ultimo 
print(lista[0*3:0*3 + 3])#primero 
print(lista[1*3:1*3 + 3])#segundo '''

lista_proc = []  # Lista para almacenar los procesos

num_ventana = len(lista) // num_proc  # Tamaño de cada porción de la lista

# Crear procesos asignando porciones de la lista
for i in range(num_proc):
    if i == num_proc - 1:  # Último proceso se queda con el resto
        p = Process(target=suma_par, args=(lista[i*num_ventana:], valor))
    else:  # Otros procesos con su porción correspondiente
        p = Process(target=suma_par, args=(lista[i*num_ventana: i*num_ventana + num_ventana], valor))
    lista_proc.append(p)

# Iniciar todos los procesos
for p in lista_proc:
    p.start()

# Esperar a que todos los procesos terminen
for p in lista_proc:
    p.join()

print(valor.value)  # Imprime la suma total de la lista
