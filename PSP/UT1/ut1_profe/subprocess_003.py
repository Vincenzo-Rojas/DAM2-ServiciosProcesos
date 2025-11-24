# Este programa pide un fichero y una cadena al usuario,
# luego busca la cadena dentro del fichero usando cat y grep.
# Se ejecutan comandos del sistema con subprocess y se pasa la salida de cat a grep.

import subprocess  # Para ejecutar comandos del sistema operativo

# Pedir al usuario el nombre del fichero y la cadena a buscar
fichero = input("Ingrese nombre de fichero:\t")
aguja = input("Ingrese cadena a buscar:\t")

# Ejecutar 'cat' para leer el contenido del fichero
p_cat = subprocess.run(
    args=["cat", fichero],
    capture_output=True,
    text=True
)

# Ejecutar 'grep' para buscar la cadena dentro del contenido leído
p_grep = subprocess.run(
    args=["grep", aguja],
    capture_output=True,
    text=True,
    input=p_cat.stdout  # Pasar la salida de cat como entrada a grep
)

print(p_grep.stdout)  # Imprime las líneas que contienen la cadena buscada
