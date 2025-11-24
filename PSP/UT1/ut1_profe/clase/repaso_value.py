# Este programa crea dos procesos que modifican una variable compartida.
# Un proceso suma 1 mil veces y otro resta 1 mil veces.
# Se utiliza Value para compartir la variable entre procesos y un lock implícito para evitar conflictos.

from multiprocessing import Value, Process  # Para procesos y variables compartidas

valor = Value("i", 5)  # Variable entera compartida inicializada a 5
variable = 5            # Variable local normal (no se comparte entre procesos)

# Función que suma 1 a la variable compartida 1000 veces
def suma(valor):
    with valor:  # Bloqueo implícito para acceso seguro
        for i in range(1000):
            valor.value += 1

# Función que resta 1 a la variable compartida 1000 veces
def resta(valor):
    with valor:  # Bloqueo implícito para acceso seguro
        for i in range(1000):
            valor.value -= 1

# Crear procesos para sumar y restar
p_suma = Process(target=suma, args=(valor,))
p_resta = Process(target=resta, args=(valor,))

# Iniciar ambos procesos
p_suma.start()
p_resta.start()

# Esperar a que ambos procesos terminen
p_suma.join()
p_resta.join()

print(valor.value)  # Imprime el valor final de la variable compartida
