import subprocess  # Permite ejecutar comandos externos del sistema
import sys         # Permite leer argumentos pasados al script
import os          # Permite detectar el sistema operativo

# Función principal que lista un directorio y guarda la salida en un fichero
def listar_directorio_y_guardar():
    # Ejecutar el comando como un subproceso y capturar salida y errores
    try:
        # Comprobar que se ha pasado un único argumento (el PID)
        if len(sys.argv) != 2:
            print("Número incorrecto de parámetros, se espera el nombre de un proceso")
            os._exit(-1)  # Salir inmediatamente con código de error
        # Comando 
        parametro = sys.argv[1]  # Nombre del proceso a buscar
        #comando = ['ps', '-eo', 'comm,%mem', '--sort=-%mem', '|','head','-n','5'
        #       ,'|','grep', parametro]
        
        p_ps = subprocess.run(
            args=['ps', '-eo', 'comm,%mem', '--sort=-%mem'],
            capture_output=True,
            text=True
            )
        
        p_head= subprocess.run(
            args=["head", "-n 6"],
            capture_output=True,
            text=True,
            input=p_ps.stdout  # Pasar la salida de cat como entrada a grep
            )
        
        # Ejecutar 'grep' para buscar la cadena dentro del contenido leído
        p_grep = subprocess.run(
            args=["grep", parametro],
            capture_output=True,
            text=True,
            input=p_head.stdout  # Pasar la salida de cat como entrada a grep
        )
        
        if(p_grep.stdout != ""):
            print(p_grep.stdout)  # Imprime las líneas que contienen la cadena buscada
        else:
            print("No hay progamas de los mas 5 usados con ese nombre")
    except FileNotFoundError as e:  # Si el ejecutable no existe
        print('Error: ejecutable no encontrado.', e)
        return False
    except Exception as e:  # Cualquier otro error al ejecutar el comando
        print('Error al ejecutar proceso.', e)
        return False


# Función que define la ruta a listar según argumentos del script
def main():
    listar_directorio_y_guardar()  # Llamada a la función principal

# Ejecutar main solo si se ejecuta directamente el script
if __name__ == '__main__':
    main()

