#subproces, que indica cuanto tiempo a estado ejecutado el primos.py

import subprocess  # Para ejecutar comandos del sistema operativo

#["bash", "-c", "time python primos.py"]

# Ejecutar 'time' para leer el contenido del fichero

p = subprocess.run(
    args=["bash", "-c", "time python primos.py"],  # Comando a ejecutar
    capture_output=True,   # Capturar la salida del comando
    text=True              # Tratar entrada y salida como texto (no bytes)
)

# Ejecutar 'grep' para buscar la cadena 
p_grep = subprocess.run(
    args=["grep", "El numero de primos"],
    capture_output=True,
    text=True,
    input=p.stdout  # Pasar la salida de cat como entrada a grep
)

print(p_grep.stdout)
print(p.stderr)