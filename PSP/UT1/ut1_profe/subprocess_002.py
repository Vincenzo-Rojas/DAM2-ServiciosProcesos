# Este programa lee un archivo de texto y busca líneas que contengan "rit" usando grep.
# Se utiliza subprocess.run para ejecutar el comando grep pasando el texto desde Python.

import subprocess  # Para ejecutar comandos del sistema operativo

texto = ""  # Variable para almacenar el contenido del archivo

# Abrir y leer el archivo "texto_prueba.txt"
with open("texto_prueba.txt", "r") as file:
    texto = file.read()

# Ejecutar grep para buscar "rit" en el contenido leído
p = subprocess.run(
    args=["grep", "rit"],  # Comando a ejecutar
    input=texto,           # Pasar el texto como entrada
    capture_output=True,   # Capturar la salida del comando
    text=True              # Tratar entrada y salida como texto (no bytes)
)

print(p.stdout)  # Imprime las líneas que contienen "rit"
