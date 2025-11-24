# exam4_signals.py
# Ejercicio 4 — Señales: crear un proceso hijo que espere y el padre envia SIGTERM.
# Enunciado:
# - El hijo debe registrar un manejador para SIGTERM que termine con exit code 0
# - El padre debe enviar SIGTERM al hijo y comprobar que el hijo finaliza correctamente.
#
# Autoevaluación:
# - Si el hijo finaliza con código 0 y el padre detecta esto, imprimir 'RESULTADO: OK'.
# Nota: Funciona en sistemas POSIX; en Windows behavior puede variar.

import multiprocessing as mp
import os
import signal
import sys
import time

def hijo_espera():
    # Manejador simple para SIGTERM que sale con código 0
    def manejador(signum, frame):
        # Salimos explícitamente con código 0 al recibir SIGTERM
        sys.exit(0)
    # Registramos manejador
    signal.signal(signal.SIGTERM, manejador)
    # Esperamos indefinidamente hasta recibir la señal
    while True:
        time.sleep(0.5)

def main():
    # Crear proceso hijo con target hijo_espera
    p = mp.Process(target=hijo_espera)
    p.start()
    # Esperamos un poco para asegurar que el hijo está en su bucle
    time.sleep(1)
    # Enviamos SIGTERM al proceso hijo
    try:
        os.kill(p.pid, signal.SIGTERM)
    except Exception as e:
        print('Error al enviar señal:', e)
        p.terminate()
        p.join()
        print('RESULTADO: FAIL')
        sys.exit(5)
    # Esperamos a que termine y comprobamos exitcode
    p.join(timeout=5)
    # Si sigue vivo, terminamos forzosamente
    if p.is_alive():
        p.terminate()
        p.join()
        print('Hijo no terminó a tiempo.')
        print('RESULTADO: FAIL')
        sys.exit(6)
    # Comprobamos código de salida (exitcode == 0 esperable)
    if p.exitcode == 0:
        print('Hijo finalizó con exitcode 0.')
        print('RESULTADO: OK')
        sys.exit(0)
    else:
        print('Hijo finalizó con exitcode', p.exitcode)
        print('RESULTADO: FAIL')
        sys.exit(7)

if __name__ == '__main__':
    main()
