from Cliente import Cliente

class Cola:
    def __init__(self, cajero):
        self.items = [cajero]

    def esta_vacia( self ):
        return len(self.items) == 1

    def encolar(self, item):
        self.items.append(item)
        self.actualizarReferencias()

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(1)
        else:
            return None

    def tamano(self):
        return len(self.items)

    def frente(self):
        if not self.esta_vacia():
            return self.items[1]
        else:
            return None

    def actualizarReferencias(self):
        if not self.esta_vacia():
            for i in range(len(self.items)-1):
                self.items[i].setSiguiente(self.items[i+1])

    def getItems(self):
        return self.items
