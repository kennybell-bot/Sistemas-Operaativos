class Cliente():

    def __init__(self, cantidadTransacciones: int, id: str):
        self.cantidadTransacciones = cantidadTransacciones
        self.id = "Cliente "+str(id)
        self.satisfecho = False
        self.siguiente = None

    def setSiguiente(self, siguiente):
        self.siguiente = siguiente

    def setSatisfecho(self, valor:bool):
        self.satisfecho = valor

    def getCantidadTransacciones(self):
        return self.cantidadTransacciones
    
    def getId(self):
        return self.id
    
    def setCantidadTransacciones(self, cantidadTransacciones):
        self.cantidadTransacciones = cantidadTransacciones