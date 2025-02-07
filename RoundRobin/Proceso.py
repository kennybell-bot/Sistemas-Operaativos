class Proceso:
    def __init__(self, id, rafaga, tiempoLlegada):
        self.estado = "Nuevo"
        self.id = id
        self.rafaga = rafaga
        self.rafagaEjecutada = 0
        self.tiempoComienzo = 0
        self.tiempoEspera = 0
        self.tiempoFinal = 0
        self.tiempoLlegada = tiempoLlegada
        self.tiempoRetorno = 0

    # Getters
    def get_estado(self):
        return self.estado

    def get_id(self):
        return self.id

    def get_rafaga(self):
        return self.rafaga

    def get_rafagaEjecutada(self):
        return self.rafagaEjecutada

    def get_tiempoComienzo(self):
        return self.tiempoComienzo

    def get_tiempoEspera(self):
        return self.tiempoEspera

    def get_tiempoFinal(self):
        return self.tiempoFinal

    def get_tiempoLlegada(self):
        return self.tiempoLlegada

    def get_tiempoRetorno(self):
        return self.tiempoRetorno

    # Setters
    def set_estado(self, estado):
        self.estado = estado

    def set_id(self, id):
        self.id = id

    def set_rafaga(self, rafaga):
        self.rafaga = rafaga

    def set_rafagaEjecutada(self, rafagaEjecutada):
        self.rafagaEjecutada = rafagaEjecutada

    def set_tiempoComienzo(self, tiempoComienzo):
        self.tiempoComienzo = tiempoComienzo

    def set_tiempoEspera(self, tiempoEspera):
        self.tiempoEspera = tiempoEspera

    def set_tiempoFinal(self, tiempoFinal):
        self.tiempoFinal = tiempoFinal

    def set_tiempoLlegada(self, tiempoLlegada):
        self.tiempoLlegada = tiempoLlegada

    def set_tiempoRetorno(self, tiempoRetorno):
        self.tiempoRetorno = tiempoRetorno

    # Método para actualizar los tiempos
    def actualizarTiempos(self):
        self.tiempoFinal = self.rafaga + self.tiempoComienzo
        self.tiempoRetorno = self.tiempoFinal - self.tiempoLlegada
        self.tiempoEspera = self.tiempoRetorno - self.rafaga