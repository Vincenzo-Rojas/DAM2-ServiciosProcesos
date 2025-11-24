# exam1_subprocess.py
# Ejercicio 1 — Subprocess: crear proceso que liste un directorio y guarde resultado.
# Enunciado:
# - Implementa la función 'listar_y_guardar(ruta, fichero_salida)' que debe:
#   1) ejecutar 'ls -la <ruta>' en Unix o 'dir <ruta>' en Windows usando subprocess.run
#   2) guardar la salida stdout en 'fichero_salida'
#   3) devolver True si la operación tuvo éxito (archivo creado) o False en caso contrario
#
# Autoevaluación:
# - El script crea 'salida_exam1.txt' y al final imprime 'RESULTADO: OK' si todo es correcto.

import subprocess  # Para ejecutar comandos del sistema
import os          # Para operaciones con el sistema de ficheros
import sys         # Para argumentos y salida

def listar_y_guardar(ruta, fichero_salida):
    # Detectamos sistema operativo; construimos el comando como lista.
    if os.name == 'nt':
        cmd = ['cmd', '/C', 'dir', ruta]
    else:
        cmd = ['ls', '-la', ruta]
    try:
        # Ejecuta el comando y captura la salida.
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except Exception as e:
        # En caso de error al ejecutar, devolvemos False.
        print('Error al ejecutar comando:', e)
        return False
    # Intentamos escribir la salida en el fichero destino.
    try:
        with open(fichero_salida, 'w', encoding='utf-8') as f:
            f.write(res.stdout)
    except Exception as e:
        print('Error al escribir fichero:', e)
        return False
    # Comprobamos que el fichero existe y no está vacío.
    if os.path.exists(fichero_salida) and os.path.getsize(fichero_salida) > 0:
        return True
    return False

def main():
    # Ruta por defecto: directorio actual.
    ruta = '.'
    salida = 'salida_exam1.txt'
    # Ejecutamos la función y comprobamos resultado.
    ok = listar_y_guardar(ruta, salida)
    if ok:
        print('Archivo creado:', salida)
        print('RESULTADO: OK')
        sys.exit(0)
    else:
        print('RESULTADO: FAIL')
        sys.exit(2)

if __name__ == '__main__':
    main()
