from threading import Condition

class Mesa:
    def __init__(self, huecos):
        self.galletas = 0
        self.huecos_max = huecos
        self.condition = Condition
    
    def ayadir_bandeja(self, galletas_abuela):
        self.galleta += galletas_abuela

    def coger_galleta(self):
        self.galletas -= 1