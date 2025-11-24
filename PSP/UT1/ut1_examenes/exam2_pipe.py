# exam2_pipe.py
# Ejercicio 2 — Pipe: comunicación padre-hijo con Pipe.
# Enunciado:
# - Implementa la función en el proceso hijo 'contar_letras_conn(conn)'
#   que reciba una cadena por conn.recv(), cuente las letras alfabéticas
#   y envíe el resultado de vuelta con conn.send(int).
# - El padre enviará una cadena de prueba y debe recibir el número correcto.
#
# Autoevaluación:
# - Si el padre recibe el número esperado, el script imprime 'RESULTADO: OK'.

from multiprocessing import Process, Pipe
import os
import sys

def contar_letras_conn(conn):
    # Recibe mensaje del padre; debe contar letras alpha y enviar el número.
    try:
        texto = conn.recv()
    except EOFError:
        # Si no hay dato, enviamos -1 para indicar error.
        conn.send(-1)
        conn.close()
        return
    # Contar solo caracteres alfabéticos.
    cuenta = sum(1 for c in texto if c.isalpha())
    # Enviar resultado al padre.
    conn.send(cuenta)
    # Cerrar la conexión local.
    conn.close()

def main():
    parent_conn, child_conn = Pipe()
    p = Process(target=contar_letras_conn, args=(child_conn,))
    p.start()
    # Texto de prueba conocido;  'Abc 123 XY' -> letras = 5 (A b c X Y)
    texto_prueba = 'Abc 123 XY'
    parent_conn.send(texto_prueba)
    # Recibimos respuesta del hijo
    try:
        res = parent_conn.recv()
    except EOFError:
        print('RESULTADO: FAIL')
        p.join()
        sys.exit(2)
    p.join()
    # Comprobación automática: debe ser 5
    if res == 5:
        print('Padre recibió:', res)
        print('RESULTADO: OK')
        sys.exit(0)
    else:
        print('Padre recibió (incorrecto):', res)
        print('RESULTADO: FAIL')
        sys.exit(3)

if __name__ == '__main__':
    main()
