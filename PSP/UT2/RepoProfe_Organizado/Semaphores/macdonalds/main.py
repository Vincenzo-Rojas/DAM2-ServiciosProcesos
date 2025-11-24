from pedido import Pedido
from recurso_cocina import RecursoCocina
from menu import Menu


plancha = RecursoCocina("plancha", 6)
freidora = RecursoCocina("freidora", 2)

p_aurora = Pedido("Aurora", [])
p_aurora.annadir_item(Menu.hamburguesa(p_aurora, plancha))
p_aurora.annadir_item(Menu.patatas(p_aurora, freidora))

p_aurora.iniciar_preparacion()