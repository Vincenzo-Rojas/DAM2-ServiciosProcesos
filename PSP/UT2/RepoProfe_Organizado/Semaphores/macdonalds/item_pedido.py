import utilidades

class Item:
    def __init__(self, nombre, recurso, tiempo_prep, pedido):
        self.nombre = str(nombre)
        self.recurso = recurso
        self.tiempo_prep = utilidades.limpiar_numero_entero(tiempo_prep, "Item.__init__")
        self.pedido = pedido

    def terminar_item(self):
        print(f"Item {self} del pedido de {self.pedido.cliente.upper()} terminado")
        self.pedido.terminar_item()

    def preparar_item(self):
        self.recurso.preparar_item(self)

    def __str__(self):
        return self.nombre

    

    
