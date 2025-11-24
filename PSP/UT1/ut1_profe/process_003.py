# Este programa crea dos procesos que modifican una variable compartida.
# Un proceso suma 1 cien veces y otro resta 1 cien veces.
# Se utiliza Value para compartir la variable entre procesos y un lock implícito para evitar condiciones de carrera.

from multiprocessing import Process, Value  # Para crear procesos y variables compartidas

variable = Value("i", 0)  # Variable entera compartida inicializada a 0

def sumar(variable):
    for x in range(100):
        with variable:  # Bloqueo implícito para asegurar acceso exclusivo
            variable.value += 1  # Suma 1 a la variable

def restar(variable):
    for x in range(100):
        with variable:  # Bloqueo implícito para acceso seguro
            variable.value -= 1  # Resta 1 a la variable

# Crear procesos para sumar y restar
proc_suma = Process(target=sumar, args=(variable,))
proc_resta = Process(target=restar, args=(variable,))

# Iniciar ambos procesos
proc_suma.start()
proc_resta.start()

# Esperar a que ambos procesos terminen
proc_suma.join()
proc_resta.join()

print(variable.value)  # Imprime el valor final de la variable compartida
