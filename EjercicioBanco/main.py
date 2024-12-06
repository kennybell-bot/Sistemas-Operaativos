from Cola import Cola
from Cliente import Cliente
from Cajero import Cajero
import random

if __name__ == "__main__":

    def ingresarCLiente():
        clienteNuevo = Cliente(random.randint(1,10),len(cola.getItems())-1)
        cola.encolar(clienteNuevo)

    def actualizarPantalla():
        print("---------------")
        for i in range(len(cola.getItems())):
            if i>0:
                print(f"{items[i].getId()} con {items[i].getCantidadTransacciones()} transacciones"  )


cajero = Cajero()
cola = Cola(cajero)
cantidadClientes = random.randint(1,15)

for i in range(cantidadClientes):
    ingresarCLiente()
    cola.actualizarReferencias()

items = cola.getItems()

actualizarPantalla()

while(not cola.esta_vacia()):
    cajero.atenderClientes(cola)
    actualizarPantalla()

print("End")