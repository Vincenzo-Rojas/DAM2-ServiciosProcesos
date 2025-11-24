# Este programa suma los números del 1 al 100 usando dos procesos.
# Cada proceso suma la mitad de la lista y actualiza una variable compartida.
# Se utiliza Value para compartir el resultado entre procesos.

from multiprocessing import Process, Value  # Para procesos y variables compartidas

lista_numeros = [x for x in range(1, 101)]  # Lista de números del 1 al 100
valor = Value("i", 0)  # Variable compartida para acumular la suma

# Mostrar las dos mitades de la lista
print(lista_numeros[:len(lista_numeros) // 2])  # Primera mitad
print(lista_numeros[len(lista_numeros) // 2:])  # Segunda mitad

# Función que suma los elementos de una lista parcial y actualiza la variable compartida
def suma_par(lista, valor):
    res = 0
    for i in lista:
        res += i
    with valor:  # Bloqueo implícito para acceso seguro
        valor.value += res

# Crear procesos para sumar cada mitad de la lista
p_1 = Process(target=suma_par, args=(lista_numeros[:len(lista_numeros)//2], valor))
p_2 = Process(target=suma_par, args=(lista_numeros[len(lista_numeros)//2:], valor))

# Iniciar ambos procesos
p_1.start()
p_2.start()

# Esperar a que ambos procesos terminen
p_1.join()
p_2.join()

print(valor.value)  # Imprime la suma total de la lista (resultado esperado: 5050)
