from item_pedido import Item

class Menu:
    def hamburguesa(pedido, recurso_cocina):
        return Item("hamburguesa", recurso_cocina, 2, pedido)
    def patatas(pedido, recurso_cocina):
        return Item("Patatas", recurso_cocina, 1, pedido)