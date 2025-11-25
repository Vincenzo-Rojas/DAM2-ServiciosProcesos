from multiprocessing import Process, Value, Lock
import time, random

META = 30
tortuga_pos = Value('i', 0)  # posición compartida de la tortuga
liebre_pos = Value('i', 0)   # posición compartida de la liebre
lock = Lock()