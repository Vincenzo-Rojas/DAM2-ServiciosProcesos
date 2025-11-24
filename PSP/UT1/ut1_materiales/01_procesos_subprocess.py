# Uso de subprocess para ejecutar comandos del sistema y guardar salida.

# 01_procesos_subprocess.py
# Este programa lista el contenido de un directorio usando un comando del sistema operativo
# y guarda la salida completa en un fichero de texto. Funciona en Windows y Unix/Linux/macOS.

import subprocess  # Permite ejecutar comandos externos del sistema
import sys         # Permite leer argumentos pasados al script
import os          # Permite detectar el sistema operativo

# Función principal que lista un directorio y guarda la salida en un fichero
def listar_directorio_y_guardar(ruta, fichero_salida='salida.txt'):
    # Elegir el comando según el sistema operativo
    if os.name == 'nt':  # Windows
        comando = ['cmd', '/C', 'dir', ruta]  # 'dir' lista el contenido de un directorio
    else:                 # Unix/Linux/macOS
        comando = ['ls', '-la', ruta]        # 'ls -la' lista con detalles y archivos ocultos

    # Ejecutar el comando como un subproceso y capturar salida y errores
    try:
        resultado = subprocess.run(
            comando,           # Comando a ejecutar
            capture_output=True,  # Captura stdout y stderr
            text=True,           # Convierte la salida a texto (str)
            check=False          # No lanza excepción por código de retorno distinto de 0
        )
    except FileNotFoundError as e:  # Si el ejecutable no existe
        print('Error: ejecutable no encontrado.', e)
        return False
    except Exception as e:  # Cualquier otro error al ejecutar el comando
        print('Error al ejecutar proceso.', e)
        return False

    # Si el subproceso generó algún error en stderr, mostrarlo
    if resultado.stderr:
        print('STDERR:', resultado.stderr)

    # Guardar la salida capturada en el fichero de salida
    try:
        with open(fichero_salida, 'w', encoding='utf-8') as f:
            f.write(resultado.stdout)  # Escribir toda la salida del comando
    except Exception as e:  # Captura errores al escribir el fichero
        print('Error al escribir fichero:', e)
        return False

    # Mensaje final indicando ruta, nombre de fichero y código de retorno del subproceso
    print(f"Listado de '{ruta}' guardado en '{fichero_salida}' (rc={resultado.returncode})")
    return True

# Función que define la ruta a listar según argumentos del script
def main():
    ruta = '.'  # Por defecto, se lista el directorio actual
    if len(sys.argv) > 1:  # Si se pasa un argumento, usarlo como ruta
        ruta = sys.argv[1]
    listar_directorio_y_guardar(ruta)  # Llamada a la función principal

# Ejecutar main solo si se ejecuta directamente el script
if __name__ == '__main__':
    main()

