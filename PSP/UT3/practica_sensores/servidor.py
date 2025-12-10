import socket
import threading
import subprocess
import json
import os
import struct
import time

clientes_chat = []
lock_clientes = threading.Lock()



if __name__ == "__main__":
    '''
    threading.Thread(target=servidor_chat, daemon=True).start()
    threading.Thread(target=servidor_comandos, daemon=True).start()
    threading.Thread(target=servidor_archivos, daemon=True).start()
    threading.Thread(target=servidor_stream, daemon=True).start()
    threading.Thread(target=servidor_json, daemon=True).start()
    threading.Thread(target=servidor_ntp, daemon=True).start()
    threading.Thread(target=servidor_descargas, daemon=True).start()
    '''
    

    print("Servidor multisericio ejecutándose...")
    while True:
        time.sleep(1)
