from multiprocessing import Process, Value, Lock
import time, random

META = 30  # Meta de la carrera

def mover_animal(nombre, pos, velocidad, prob_dormir, winner, lock):
    """
    Función genérica para mover un animal.
    nombre: str -> nombre del animal
    pos: Value -> posición compartida
    velocidad: float -> tiempo entre pasos
    prob_dormir: float -> probabilidad de dormir en cada paso (0 a 1)
    winner: Value -> flag de ganador
    lock: Lock -> para sincronizar acceso a variables compartidas
    """
    while pos.value < META and not winner.value:
        time.sleep(velocidad)
        
        # La liebre puede dormirse
        if prob_dormir > 0 and random.random() < prob_dormir:
            print(f"💤 {nombre} se durmió un segundo")
            time.sleep(1)
        
        with lock:
            if winner.value:
                break  # alguien ya ganó, salimos
            pos.value += 1
            print(f"{nombre} avanzó a {pos.value} {'🐢' if nombre=='Tortuga' else '🐇'}")
            
            if pos.value >= META:
                winner.value = True
                print(f"\n🏁 ¡{nombre} ha llegado a la meta!")

def main():
    # Variables compartidas
    tortuga_pos = Value('i', 0)
    liebre_pos = Value('i', 0)
    ganador = Value('b', False)
    lock = Lock()

    # Crear procesos
    p_tortuga = Process(target=mover_animal, args=("Tortuga", tortuga_pos, 0.5, 0, ganador, lock))
    p_liebre = Process(target=mover_animal, args=("Liebre", liebre_pos, 0.3, 0.15, ganador, lock))

    # Iniciar procesos
    p_tortuga.start()
    p_liebre.start()

    # Esperar a que terminen
    p_tortuga.join()
    p_liebre.join()

    # Resultado final
    print("\n📊 Resultado final de la carrera:")
    print(f"Tortuga: {tortuga_pos.value} {'🏁' if tortuga_pos.value >= META else ''}")
    print(f"Liebre: {liebre_pos.value} {'🏁' if liebre_pos.value >= META else ''}")

if __name__ == "__main__":
    main()
