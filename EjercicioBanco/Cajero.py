from Cola import Cola
import time as reloj

class Cajero():
    def __init__(self):
        self.siguiente = self

    def atenderClientes(self, colaPresente):
        cola = colaPresente
        if ((self.siguiente.getCantidadTransacciones()-5)>0):
            print("--------")
            print(f"Atendiendo {self.siguiente.getId()}")
            reloj.sleep(0.5)
            self.siguiente.setCantidadTransacciones(self.siguiente.getCantidadTransacciones()-5)
            cola.desencolar()
            cola.encolar(self.siguiente)
            cola.actualizarReferencias()
        else:
            print("--------")
            print(f"Atendiendo {self.siguiente.getId()}")
            cola.desencolar()
            cola.actualizarReferencias()

    def getSiguiente(self):
        return self.siguiente

    def setSiguiente(self, siguiente):
        self.siguiente = siguiente

    def getId():
        return "cajero"
