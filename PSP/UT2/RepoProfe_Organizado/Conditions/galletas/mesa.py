from threading import Condition

class Mesa:
    def __init__(self, huecos):
        self.huecos_max = huecos
        self.condicion = Condition()
        self.galletas = 0
    
    def annadir_bandeja(self):
        self.galletas += 10

    def coger_galleta(self):
        self.galletas -= 1