entero = 10
decimal = 3.14
texto = "hola mundo"
booleano = True
#print(f"entero: {entero}, decimal: {decimal}, texto: {texto}, bolean: {booleano}")


#cast
edad = int(input("Dime tu edad "))

#operadores
"""
Aritméticos: + - * / % // **

Comparación: == != > < >= <=

Lógicos: and or not

Asignación: += -= *= /=
"""

# Listas, tuplas, diccionarios y conjuntos - diferencias??

#CUANDO USAR CADA UNA
"""
Lista: Colección ordenada y modificable (ej. historial de compras).
Tupla: Colección inmutable y ordenada (ej. coordenadas geográficas).
Diccionario: Mapeo clave-valor (ej. perfil de usuario).
Conjunto: Colección sin duplicados, búsqueda rápida (ej. usuarios únicos que visitaron una página).
"""

#LISTAS
""" Mutabilidad: ✅ Mutable (puedes modificar, añadir o eliminar elementos).
    Orden: ✅ Ordenada (los elementos mantienen el orden en que se insertan).
    Elementos duplicados: ✅ Permite duplicados. """
mi_lista = [1, 2, 3, "Python", True]
mi_lista[0] = 10  # Modificación permitida
mi_lista.append("nuevo")  # Añadir elementos
print(mi_lista)  # [10, 2, 3, 'Python', True, 'nuevo']

#TUPLAS
""" Mutabilidad: ❌ Inmutable (no se pueden modificar después de creadas).
    Orden: ✅ Ordenada.
    Elementos duplicados: ✅ Permite duplicados.
    Tupla de un solo elemento: (valor,) — la coma es obligatoria."""
mi_tupla = (1, 2, 3, "Python")  # 1, 2, 3, "Python" - tmb sin parentesis
# mi_tupla[0] = 10  # Esto daría error: TypeError
print(mi_tupla[1])  # Acceso sí permitido: 2

#DICCIONARIOS
""" Mutabilidad: ✅ Mutable.
    Orden: ✅ Ordenado (orden de inserción se mantiene).
    Elementos duplicados: ❌ Claves únicas (valores sí pueden repetirse)."""
mi_dict = {"nombre": "Ana", "edad": 30, "activo": True}
print(mi_dict["nombre"])  # Ana
mi_dict["edad"] = 31  # Modificación permitida
mi_dict["ciudad"] = "Madrid"  # Añadir nueva clave - valor

#CONJUNTOS
""" Mutabilidad: ✅ Mutable (pero los elementos deben ser inmutables).
    Orden: ❌ Desordenado (no hay garantía de orden).
    Elementos duplicados: ❌ No permite duplicados (automáticamente únicos)."""
mi_set = {1, 2, 3, 3, 2}  # Resulta en {1, 2, 3}
mi_set.add(4)
mi_set.remove(1)
print(mi_set)  # {2, 3, 4}

# Crear set vacío
conjunto_vacio = set()  # {} crea un conjunto vacío

    

# ESTRUCTURAS DE CONTROL

if edad >= 18:
    print("Mayor de edad")
else:
    print("Menor")

for i in range(5):
    print(i)

while edad < 25:
    edad += 1
    print(edad)

# TODOS LOS USOS DEL FOR EN PYTHON

# iterar sobre una lista
frutas = ['manzana', 'pera', 'naranja', 'melón']
for i in frutas:
    print(i)

# iterar sobre diccionarios, pares clave - valor
ficha_usuario = {'nombre': 'Alberto', 'apellido': 'Ramírez', 'edad': 33}
for clave in ficha_usuario.keys():
    print(clave)

for valor in ficha_usuario.values():
    print(valor)

# simultaneo
for clave, valor in ficha_usuario.items():
    print(f'{clave} es igual a: {valor}')

#iterar sobre cadenas de caracteres
saludo = "Hola mundo"
for char in saludo:
    if char == 'm':
        print('Este texto contiene la letra m')

# iterar cadena al reves
texto = "Python"
for i in texto[::-1]:
    print(i)  # Imprime 'n', 'o', 'h', 't', 'y', 'P'

#iterar saltando caracteres
for i in texto[::2]:
    print(i)  # Imprime 'P', 't', 'o'

# sobre rango(x-1)
for num in range(10):
    print(num)  # Imprime 0 a 9

for num in range(5, 15, 2):
    print(num)  # Imprime 5, 7, 9, 11, 13

# cuando no necesitas la variable usar _
def longitud(mi_lista):
    cont = 0
    for _ in mi_lista:
        cont += 1
    return cont

# MAPEAR ARRAYS 2D
matriz = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]

for i in range(len(matriz)):        # i: índice de fila (0, 1, 2)
    for j in range(len(matriz[i])): # j: índice de columna (0, 1, 2)
        print(f"matriz[{i}][{j}] = {matriz[i][j]}")

print(matriz)  # [[2, 4, 6], [8, 10, 12], [14, 16, 18]]

# funciones

def saludar(nombre = "amigo"):
    return f"Hola {nombre}"

print(saludar("Juan"))

def sumar(*args):
    return sum(args)

print(sumar(1,2,3,4,4,5,5,6,5,7,7))

#excepiones
try:
    x = int(input("Número: "))
    print(10 / x)
except ZeroDivisionError:
    print("No se puede dividir por 0")
except ValueError:
    print("Introduce un número válido")
finally:
    print("Fin del programa")


#PROCESOS

    # OS – Sistema operativo
import os

print(os.getcwd())         # ruta actual
# os.mkdir("test_dir")       # crea carpeta
print(os.listdir("."))     # lista archivos

    # SYS – Parámetros y salida estándar
import sys
print(sys.argv)            # argumentos de línea de comandos

    # SUBPROCESS – Crear y controlar procesos
import subprocess

resultado = subprocess.run(["ls", "-l"], capture_output=True, text=True)
print(resultado.stdout)

# Concurrencia y paralelismo