palabra = "playa"
conjunto = set()
conjunto.add("l")
resultado = ""

for l in palabra:
    resultado += l if l in conjunto else "_"
        

print(resultado)