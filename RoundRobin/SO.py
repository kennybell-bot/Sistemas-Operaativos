import random
from Cola import Cola
from Proceso import Proceso

class SO:
    def __init__(self, quantum):
        self.colaProcesos = Cola()
        self.colaBloqueados = Cola()
        self.procesosTerminados = Cola()
        self.quantum = quantum
        self.reloj = 0
        self.semaforo = False
        self.cantidadTotalProcesos = 0

    # Getters
    def get_colaBloqueados(self):
        return self.colaBloqueados

    def get_colaProcesos(self):
        return self.colaProcesos

    def get_procesosTerminados(self):
        return self.procesosTerminados

    def get_quantum(self):
        return self.quantum

    def get_reloj(self):
        return self.reloj

    def get_semaforo(self):
        return self.semaforo

    def get_cantidadTotalProcesos(self):
        return self.cantidadTotalProcesos

    # Setters
    def set_colaBloqueados(self, colaBloqueados):
        self.colaBloqueados = colaBloqueados

    def set_colaProcesos(self, colaProcesos):
        self.colaProcesos = colaProcesos

    def set_procesosTerminados(self, procesosTerminados):
        self.procesosTerminados = procesosTerminados

    def set_quantum(self, quantum):
        self.quantum = quantum

    def set_reloj(self, reloj):
        self.reloj = reloj

    def set_semaforo(self, semaforo):
        self.semaforo = semaforo

    def set_cantidadTotalProcesos(self, cantidadTotalProcesos):
        self.cantidadTotalProcesos = cantidadTotalProcesos

    # Método para generar entre 1 y 5 procesos con tiempo de llegada y ráfaga aleatorias
    def generarProceso(self):
        num_procesos = random.randint(1, 5)  # Generar entre 1 y 5 procesos
        for _ in range(num_procesos):
            id_proceso = self.cantidadTotalProcesos + 1
            rafaga = random.randint(1, 10)  # Ejemplo: ráfaga aleatoria entre 1 y 10
            tiempoLlegada = self.reloj  # Tiempo de llegada es el valor del reloj actual
            nuevo_proceso = Proceso(id=id_proceso, rafaga=rafaga, tiempoLlegada=tiempoLlegada)
            self.colaProcesos.encolar(nuevo_proceso)
            self.cantidadTotalProcesos += 1  # Incrementar en 1
            print(f"Proceso {id_proceso} creado con ráfaga {rafaga} y tiempo de llegada {tiempoLlegada} e inicia en {nuevo_proceso.get_tiempoComienzo()}")

    # Método para bloquear un proceso
    def bloquearProceso(self, proceso):
        if proceso in self.colaProcesos.items:
            # Hacer una copia del proceso antes de bloquearlo
            proceso_copia = Proceso(proceso.get_id(), proceso.get_rafagaEjecutada(), proceso.get_tiempoLlegada())
            proceso_copia.set_tiempoComienzo(proceso.get_tiempoComienzo())
            proceso_copia.set_tiempoFinal(self.get_reloj())
            proceso_copia.set_estado("Bloqueado")
            proceso_copia.actualizarTiempos()
            self.procesosTerminados.encolar(proceso_copia)
            
            # Actualizar el estado y la ráfaga del proceso original
            proceso.set_estado("Bloqueado")
            proceso.set_rafaga(proceso.get_rafaga() - proceso.get_rafagaEjecutada())
            proceso.set_rafagaEjecutada(0)
            proceso.actualizarTiempos()
        
            # Bloquear el proceso original
            self.colaProcesos.items.remove(proceso)
            print(f"Proceso {proceso.get_id()} bloqueado")
            self.colaBloqueados.encolar(proceso)
            self.set_semaforo(False)

    # Método para desbloquear un proceso
    def desbloquearProceso(self):
        if not self.colaBloqueados.esta_vacia():
            proceso = self.colaBloqueados.desencolar()
            proceso.set_estado("Listo")
            self.colaProcesos.encolar(proceso)
            print(f"Proceso {proceso.get_id()} desbloqueado y encolado en la cola de procesos listos")

    # Método para atender un proceso
    def atenderProceso(self):
        tiempoLimiteProceso = None  # Inicializar la variable al inicio
        print(f"Reloj: {self.reloj}")
        if not self.colaProcesos.esta_vacia():
            proceso = self.colaProcesos.items[0]
            print(f"Proceso: {proceso.get_id()} - Estado: {proceso.get_estado()}")
            if proceso.get_tiempoLlegada() <= self.get_reloj() and (proceso.get_estado() == "Nuevo" or proceso.get_estado() == "Listo"):
                proceso.set_estado("Listo")
                if not self.get_semaforo():
                    proceso.set_estado("Ejecucion")
                    proceso.set_tiempoComienzo(self.get_reloj())
                    proceso.actualizarTiempos()
                    self.set_semaforo(True)
            if proceso.get_estado() == "Ejecucion":
                # Inicializar la variable tiempoLimiteProceso
                tiempoLimiteProceso = self.get_quantum() + proceso.get_tiempoComienzo()
                if self.get_reloj() != proceso.get_tiempoFinal() and self.get_reloj() != tiempoLimiteProceso:
                    proceso.set_rafagaEjecutada(proceso.get_rafagaEjecutada() + 1)
                if tiempoLimiteProceso is not None and self.get_reloj() == tiempoLimiteProceso:
                    # Hacer una copia del proceso, asignar la ráfaga ejecutada y recalcular tiempos
                    proceso_terminado = Proceso(proceso.get_id(), proceso.get_rafagaEjecutada(), proceso.get_tiempoLlegada())
                    proceso_terminado.set_tiempoComienzo(proceso.get_tiempoComienzo())
                    proceso_terminado.set_rafagaEjecutada(proceso.get_rafagaEjecutada())
                    proceso_terminado.set_estado("Terminado")
                    proceso_terminado.actualizarTiempos()
                    self.procesosTerminados.encolar(proceso_terminado)
                    # Desencolar el proceso original, actualizar su estado y ráfaga, y volver a encolarlo
                    self.colaProcesos.desencolar()
                    proceso.set_estado("Nuevo")
                    proceso.set_rafaga(proceso.get_rafaga() - proceso.get_rafagaEjecutada())
                    proceso.set_rafagaEjecutada(0)
                    self.colaProcesos.encolar(proceso)
                    self.set_semaforo(False)
                    # Imprimir la lista de procesos en la cola
                    print("Procesos en la cola:")
                    for p in self.colaProcesos.items:
                        print(f"Proceso {p.get_id()} - Estado: {p.get_estado()} - Ráfaga: {p.get_rafaga()} - Ráfaga Ejecutada: {p.get_rafagaEjecutada()}")
                    # Iniciar el siguiente proceso en el mismo instante
                    if not self.colaProcesos.esta_vacia():
                        siguiente_proceso = self.colaProcesos.items[0]
                        siguiente_proceso.set_estado("Ejecucion")
                        siguiente_proceso.set_tiempoComienzo(self.get_reloj())
                        siguiente_proceso.actualizarTiempos()
                        self.set_semaforo(True)
                if self.get_reloj() == proceso.get_tiempoFinal():
                    proceso.set_estado("Terminado")
                    self.colaProcesos.desencolar()
                    self.procesosTerminados.encolar(proceso)
                    self.set_semaforo(False)
                    # Iniciar el siguiente proceso en el mismo instante
                    if not self.colaProcesos.esta_vacia():
                        siguiente_proceso = self.colaProcesos.items[0]
                        siguiente_proceso.set_estado("Ejecucion")
                        siguiente_proceso.set_tiempoComienzo(self.get_reloj())
                        siguiente_proceso.actualizarTiempos()
                        self.set_semaforo(True)
        self.reloj += 1