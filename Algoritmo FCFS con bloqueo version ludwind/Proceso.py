class Proceso:

    #Revisar si es necesario ingresar y trabajar prioridades
    def __init__(self, nombre, tiempo_llegada, rafaga_ejecucion):
        self.nombre = nombre
        self.tiempo_llegada = tiempo_llegada
        self.rafaga_ejecucion = rafaga_ejecucion
        self.tiempo_inicio = 0
        self.tiempo_finalizacion = 0
        self.tiempo_retorno = 0
        self.tiempo_espera = 0
        self.rafaga_anterior = 0
        self.estado = "Nuevo"
        #aniadido
        self.bloqueado = False
        self.prioridad = 0

    def __str__(self):
        return f"Proceso {self.nombre} \t Llegada: {self.tiempo_llegada} \t Rafaga: {self.rafaga_ejecucion} \t Inicio: {self.tiempo_inicio} \t Finalización: {self.tiempo_finalizacion} \t Retorno: {self.tiempo_retorno} \t Espera: {self.tiempo_espera} \t Prioridad: {self.prioridad}\n"
    #

    def setEstado(self, estado):
        self.estado = estado

    def getEstado(self):
        return self.estado
    
    def getTiempoLLegada(self):
        return self.tiempo_llegada
    
    def setTiempoInicio(self, tiempo_inicio):
        self.tiempo_inicio = tiempo_inicio

    def getTiempoInicio(self):
        return self.tiempo_inicio
    
    def getTiempoFinalizacion(self):
        return self.tiempo_finalizacion
    
    def getRafaEjecucion(self):
        return self.rafaga_ejecucion
    
    def setRafagaEjecucion(self, rafaga_ejecucion_nueva):
        self.rafaga_ejecucion = rafaga_ejecucion_nueva

    def setTiempoFinalziacion(self, tiempo_finalizacion):
        self.tiempo_finalizacion = tiempo_finalizacion

    def getTiempoLlegada(self):
        return self.tiempo_llegada
    
    def setRafagaAnterior(self, rafaga_anterior):
        self.rafaga_anterior += rafaga_anterior

    def setPrioridad(self, prioridad):
        self.prioridad = prioridad

    def getPrioridad(self):
        return self.prioridad
    
    def getBloqueado(self):
        return self.bloqueado
    
    def getNombre(self):
        return self.nombre

    def calcularTiempos(self, bloqueo):
        if (self.rafaga_ejecucion > bloqueo) and self.estado == "Bloqueado" and self.bloqueado == False :
            self.tiempo_finalizacion = bloqueo + self.getTiempoInicio()
            self.tiempo_retorno = self.getTiempoFinalizacion() - self.tiempo_llegada
            self.tiempo_espera = self.tiempo_retorno - bloqueo
            self.rafaga_ejecucion = self.rafaga_ejecucion - bloqueo
            self.bloqueado = True
        else:
            self.tiempo_finalizacion = self.getRafaEjecucion() + self.getTiempoInicio()
            self.tiempo_retorno = self.getTiempoFinalizacion() - self.tiempo_llegada
            self.tiempo_espera = self.tiempo_retorno - self.rafaga_ejecucion
