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


