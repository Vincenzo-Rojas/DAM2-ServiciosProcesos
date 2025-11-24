import threading, time, random                     # importamos módulos: threading para hilos, time para sleeps, random (no usado aquí pero estaba en tu ejemplo original)

# --- Configuración ---
MAX_GALLETAS = 100                                # límite de galletas que puede haber en la mesa
PRODUCCION = 10                                   # abuela produce 10 galletas por minuto (simulado)
TIEMPO_PRODUCCION = 1
# tiempo real entre galletas producidas:
# 1 min simulado = 1s real, produce 10 galletas por ese minuto 

TIEMPO_COMER = 0.33
# tiempo real que tarda un nieto en comerse 1 galleta:
# 20 segundos simulados = 0.333... s real

ESPERA_EXTRA = 3
# tiempo real de espera extra si hay exceso de galletas:
# 3 minutos simulados => 3 s reales por cada galleta de exceso

# --- Recursos compartidos ---
galletas = []                                     # lista que representa las galletas en la mesa (buffer FIFO)
condition = threading.Condition()                 # Condition para sincronizar productores/consumidores

# --- Productor (abuela) ---
def abuela():
    while True:
        with condition:                           # entrar en la sección crítica asociada a la condición
            if len(galletas) < MAX_GALLETAS:     # si la mesa no está llena
                galletas.append("🍪")             # colocar una galleta en la mesa (al final de la lista)
                print(f"Abuela hizo una galleta. Total: {len(galletas)}")
                condition.notify_all()            # notificar a todos los consumidores que hay galletas
            else:
                # si la mesa está llena, la abuela espera a que alguien coma (se libera la condición)
                print("🧓 La abuela espera... la mesa está llena (100 galletas).")
                condition.wait()                 # libera el lock y espera a ser notificada
        time.sleep(TIEMPO_PRODUCCION)             # espera fuera del lock: tiempo entre producir galletas

# --- Consumidor (nieto) ---
def nieto(id):
    while True:
        with condition:                           # entrar en sección crítica para acceder a la mesa
            while not galletas:                   # mientras no haya galletas, esperar
                print(f"Nieto {id} espera, no hay galletas...")
                condition.wait()                 # libera el lock y espera a ser notificado
            galletas.pop(0)                       # comer la primera galleta (FIFO)
            print(f"👦 Nieto {id} comió una galleta. Quedan {len(galletas)}")
            condition.notify_all()                # notificar (a la abuela o a otros nietos) que cambió el buffer

        time.sleep(TIEMPO_COMER)                  # tiempo real que tarda en comerse la galleta (fuera del lock)

        # Regla adicional: si hay más de 10 galletas, los nietos esperan antes de volver a comer.
        # La espera es 3 minutos simulados (3 s reales) por cada galleta que supere las 10.
        if len(galletas) > 10:
            exceso = len(galletas) - 10           # cuántas galletas por encima del umbral
            espera = exceso * ESPERA_EXTRA        # tiempo real total de espera
            print(f"Nieto {id} ve demasiadas galletas ({len(galletas)}), espera {espera:.1f}s")
            time.sleep(espera)
