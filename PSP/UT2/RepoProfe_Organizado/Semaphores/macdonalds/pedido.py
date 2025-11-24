
class Pedido:
    def __init__(self, cliente, items):
        self.cliente = cliente
        self.items = []
        for i in items:
            self.annadir_item(i)
        self.en_prep = False
        self.num_items = len(self.items)

    def annadir_item(self, item):
        if not self.en_prep:
            self.items.append(item)
            self.num_items += 1
        elif self.en_prep:
            print("No se pueden añadir artículos a un pedido en preparación")
        else:
            raise Exception("No se pueden añadir cosas al pedido que no sean Item")
    
    def iniciar_preparacion(self):
        self.en_prep = True
        print(f"Pedido de {self.cliente.upper()} en preparación: Quedan {self.num_items} para terminar")
        for i in self.items:
            i.preparar_item()
    
    def terminar_pedido(self):
        print(f"Pedido de {self.cliente.upper()} terminado, disfrute su comida")
    
    def terminar_item(self):
        self.num_items -= 1
        print(f"Quedan {self.num_items} items en el pedido de {self.cliente} por preparar")
        if self.num_items == 0: # se ha terminado el pedido completo
            self.terminar_pedido()
        