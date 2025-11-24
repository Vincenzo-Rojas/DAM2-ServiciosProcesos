# Este programa simula un efecto de animación de un carácter "#" 
# que se mueve de izquierda a derecha y de vuelta en la terminal.
# Utiliza bucles y pausas cortas para que el movimiento parezca fluido,
# y limpia la pantalla en cada paso para mostrar solo el "#" en su posición actual.

import time  # Importa el módulo 'time' para poder pausar la ejecución del programa
import subprocess  # Importa el módulo 'subprocess' para ejecutar comandos del sistema operativo


def limpiar():
    # Función que limpia la pantalla de la terminal
    subprocess.run(args=["clear"])  # Ejecuta el comando 'clear' de la terminal (Linux/Mac). En Windows sería 'cls'


def derecha():
    # Función que mueve el "#" hacia la derecha
    for j in range(20):  # Bucle que va de 0 a 19 (20 pasos hacia la derecha)
        print(j * " " + "#")  # Imprime '#' precedido de 'j' espacios en blanco, simulando movimiento
        time.sleep(0.05)  # Pausa de 0.05 segundos para que la animación sea visible
        limpiar()  # Limpia la pantalla antes del siguiente paso


def izquierda():
    # Función que mueve el "#" hacia la izquierda
    for j in range(20, -1, -1):  # Bucle que va de 20 a 0 (20 pasos hacia la izquierda)
        print(j * " " + "#")  # Imprime '#' precedido de 'j' espacios en blanco
        time.sleep(0.05)  # Pausa de 0.05 segundos
        limpiar()  # Limpia la pantalla antes del siguiente paso


if __name__ == "__main__":
    # Punto de entrada del programa: solo se ejecuta si el script se ejecuta directamente
    while True:  # Bucle infinito para que la animación se repita indefinidamente
        derecha()  # Llama a la función que mueve '#' hacia la derecha
        izquierda()  # Llama a la función que mueve '#' hacia la izquierda
