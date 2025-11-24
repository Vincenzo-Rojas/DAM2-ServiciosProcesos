# Manejo de señales y ejemplo de tuberia estilo shell.

# 04_senales_y_tuberias.py
# Este programa muestra dos ejemplos:
# 1. Manejo de señales: captura SIGINT y SIGTERM para salir limpiamente.
# 2. Uso de tuberías estilo shell: conecta 'ls -la' con 'grep py' usando subprocess.

import signal      # Para manejar señales del sistema
import time        # Para pausas temporales
import sys         # Para leer argumentos del programa
import subprocess  # Para ejecutar comandos externos
import os          # Para obtener PID y otras funciones del sistema

# Handler que se ejecuta al recibir una señal
def handler(signum, frame):
    print(f'Proceso {os.getpid()}: recibido {signum}. Saliendo.')
    sys.exit(0)  # Termina el proceso

# Ejemplo de manejo de señales
def ejemplo_senales():
    signal.signal(signal.SIGINT, handler)  # Captura Ctrl+C
    try:
        signal.signal(signal.SIGTERM, handler)  # Captura SIGTERM
    except AttributeError:
        print('SIGTERM no disponible en esta plataforma')
    print(f'PID: {os.getpid()} - espera señales')
    while True:
        time.sleep(1)  # Espera señales en bucle

# Ejemplo de tubería estilo shell: ls -la | grep py
def ejemplo_pipe():
    try:
        # Primer comando: ls -la
        p1 = subprocess.Popen(['ls','-la'], stdout=subprocess.PIPE, text=True)
        # Segundo comando: grep py, toma la salida de p1 como entrada
        p2 = subprocess.Popen(['grep','py'], stdin=p1.stdout, stdout=subprocess.PIPE, text=True)
        p1.stdout.close()  # Cierra el stdout de p1 en p2
        out = p2.communicate()[0]  # Captura la salida filtrada
        print('Salida filtrada:'); print(out)
    except FileNotFoundError as e:
        print('Comando no encontrado', e)

# Función principal que decide qué ejemplo ejecutar según argumento
def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'pipe':
        ejemplo_pipe()       # Ejecutar ejemplo de tubería
    else:
        ejemplo_senales()    # Ejecutar ejemplo de señales

if __name__ == '__main__':
    main()

