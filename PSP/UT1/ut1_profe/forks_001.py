# Este programa demuestra cómo funciona la creación de procesos hijos
# en sistemas tipo Unix usando 'os.fork()'. Cada llamada a fork()
# crea un nuevo proceso duplicando el proceso actual.
# Esto genera múltiples procesos que ejecutan el mismo código
# a partir del punto donde se hace el fork.

import os  # Importa el módulo 'os' para acceder a funcionalidades del sistema operativo

print("INICIO")  # Imprime "INICIO" en la terminal

os.fork()  
# Crea un nuevo proceso hijo.
# Después de esta línea, habrá 2 procesos ejecutando el código a partir de aquí:
# - El proceso original (padre)
# - El nuevo proceso (hijo)

os.fork()
# Cada proceso que llega a esta línea crea otro hijo.
# Ahora habrá 4 procesos en total ejecutando el código a partir de este punto.

print("FINAL")  
# Cada uno de los 4 procesos imprime "FINAL".
# Por eso, veremos "FINAL" impreso 4 veces en la salida (aunque el orden puede variar
# porque los procesos se ejecutan concurrentemente).
