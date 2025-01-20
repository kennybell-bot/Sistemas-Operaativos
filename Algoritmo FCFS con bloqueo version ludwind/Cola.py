class Cola:
    def __init__(self):
        self.items = []

    def esta_vacia( self ):
        return len(self.items) == 0

    def encolar(self, item):
        self.items.append(item)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)
        else:
            return None

    def tamano(self):
        return len(self.items)

    def frente(self):
        if not self.esta_vacia():
            return self.items[0]
        else:
            return None

    def getItems(self):
        return self.items