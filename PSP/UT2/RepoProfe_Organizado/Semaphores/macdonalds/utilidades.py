def limpiar_numero_entero(numero, nom_funcion):
    if isinstance(numero, int):
        return numero
    elif isinstance(numero, str) and numero.isnumeric():
        return int(numero)
    else:
        raise TypeError(f"El tipo de dato tiene que ser entero: {nom_funcion}()")
