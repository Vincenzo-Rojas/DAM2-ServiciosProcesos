# autograder.py
# Script que ejecuta todas las pruebas de los ejercicios y muestra una puntuación.
# Comentado línea a línea en español.

import subprocess  # Para ejecutar los scripts de los ejercicios como procesos separados
import sys         # Para control de salida
import os          # Para operaciones con rutas

# Lista de ejercicios a evaluar (archivo, puntos)
EXAMS = [
    ("PSP/UT1/ut1_examenes/exam1_subprocess.py", 20),
    ("PSP/UT1/ut1_examenes/exam2_pipe.py", 20),
    ("PSP/UT1/ut1_examenes/exam3_lock.py", 20),
    ("PSP/UT1/ut1_examenes/exam4_signals.py", 20),
    ("PSP/UT1/ut1_examenes/exam5_queue.py", 20),
]

def run_test(file):
    # Ejecuta un script de ejercicios y recoge su salida y código de retorno.
    # Devuelve (exito_bool, salida_texto)
    try:
        # Llamamos a Python para ejecutar el script; timeout para evitar bloqueos infinitos.
        proc = subprocess.run([sys.executable, file], capture_output=True, text=True, timeout=10)
        out = proc.stdout + proc.stderr
        # Interpretamos que éxito es código de retorno 0 y salida que contenga 'OK' (definido por cada examen).
        ok = (proc.returncode == 0) and ("RESULTADO: OK" in out)
        return ok, out
    except subprocess.TimeoutExpired as e:
        return False, f"TIMEOUT: {e}"
    except Exception as e:
        return False, f"ERROR EJECUCIÓN: {e}"

def main():
    # Calcula nota total sumando puntos de pruebas superadas.
    total = 0
    max_total = sum(p for _, p in EXAMS)
    print("Autograder UT1 - Ejercicios tipo examen")
    print("--------------------------------------")
    for fname, pts in EXAMS:
        if not os.path.exists(fname):
            print(f"{fname}: NO ENCONTRADO -> 0/{pts} puntos")
            continue
        ok, out = run_test(fname)
        if ok:
            total += pts
            print(f"{fname}: OK -> {pts}/{pts} puntos")
        else:
            print(f"{fname}: FAIL -> 0/{pts} puntos")
        # Mostrar salida resumida (primeras 8 líneas)
        print("Salida (resumen):")
        for line in out.splitlines()[:8]:
            print("  ", line)
        print("-" * 40)
    print(f"Puntuación total: {total}/{max_total}")
    # Exit code 0 si todo aprobado
    if total == max_total:
        print("ENHORABUENA: Todas las pruebas pasaron.")
        sys.exit(0)
    else:
        print("Algunas pruebas fallaron. Revisa la salida.")
        sys.exit(1)

if __name__ == '__main__':
    main()
