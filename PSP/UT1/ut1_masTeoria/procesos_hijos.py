import time
import os

def calcular_cuadrado(numero):
    # Obtener el ID del proceso actual
    # Cada proceso tiene un PID único que lo identifica en el sistema
    pid = os.getpid()
    print(f"Proceso calcular_cuadrado (PID: {pid}) iniciado")
    
    # Simular trabajo con una pausa
    # Durante este tiempo, el proceso puede estar en estado de espera
    time.sleep(1)
    
    # Realizar el cálculo
    # Este es el trabajo principal del proceso
    resultado = numero * numero
    
    # Mostrar el resultado
    # El proceso tiene su propio espacio de direcciones y recursos
    print(f"El cuadrado de {numero} es {resultado}")
    
    # Finalizar el proceso
    # El proceso pasa al estado terminado y se libera su contexto
    print(f"Proceso calcular_cuadrado (PID: {pid}) finalizado")

def calcular_cubo(numero):
    # Obtener el ID del proceso actual
    # El PID permite identificar unívocamente cada proceso en Linux
    pid = os.getpid()
    print(f"Proceso calcular_cubo (PID: {pid}) iniciado")
    
    # Simular trabajo con una pausa
    # El sistema operativo puede cambiar de contexto durante esta espera
    time.sleep(1.5)
    
    # Realizar el cálculo
    # Cada proceso tiene su propio espacio de memoria independiente
    resultado = numero * numero * numero
    
    # Mostrar el resultado
    # Los procesos no comparten memoria, por lo que la comunicación requiere IPC
    print(f"El cubo de {numero} es {resultado}")
    
    # Finalizar el proceso
    # El proceso terminado pasa a estado zombie hasta que el padre lo recoja
    print(f"Proceso calcular_cubo (PID: {pid}) finalizado")
