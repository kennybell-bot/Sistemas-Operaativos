import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import threading
from SO import SO

class Ventana:
    def __init__(self, root, so):
        self.root = root
        self.so = so
        self.root.title("Simulación de Procesos - Diagrama de Gantt")

        # Crear la tabla
        self.tree = ttk.Treeview(root, columns=("ID", "Tiempo Llegada", "Ráfaga", "Ráfaga Ejecutada", "Tiempo Inicio", "Tiempo Final", "Tiempo Espera", "Tiempo Retorno"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tiempo Llegada", text="Tiempo Llegada")
        self.tree.heading("Ráfaga", text="Ráfaga")
        self.tree.heading("Ráfaga Ejecutada", text="Ráfaga Ejecutada")
        self.tree.heading("Tiempo Inicio", text="Tiempo Inicio")
        self.tree.heading("Tiempo Final", text="Tiempo Final")
        self.tree.heading("Tiempo Espera", text="Tiempo Espera")
        self.tree.heading("Tiempo Retorno", text="Tiempo Retorno")
        self.tree.pack(side=tk.TOP, fill=tk.X)

        # Crear el gráfico de Gantt
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Crear botones
        self.btn_generar = tk.Button(root, text="Generar Proceso", command=self.generar_proceso)
        self.btn_generar.pack(side=tk.LEFT)

        self.btn_bloquear = tk.Button(root, text="Bloquear Proceso", command=self.bloquear_proceso)
        self.btn_bloquear.pack(side=tk.LEFT)

        self.btn_iniciar = tk.Button(root, text="Iniciar", command=self.iniciar_procesos)
        self.btn_iniciar.pack(side=tk.LEFT)

        self.btn_desbloquear = tk.Button(root, text="Desbloquear Proceso", command=self.desbloquear_proceso)
        self.btn_desbloquear.pack(side=tk.LEFT)

        # Crear etiqueta para mostrar el estado del semáforo
        self.lbl_semaforo = tk.Label(root, text=f"Semáforo: {self.so.get_semaforo()}")
        self.lbl_semaforo.pack(side=tk.BOTTOM)

        # Crear etiqueta para mostrar la información de los procesos bloqueados
        self.lbl_bloqueados = tk.Label(root, text="Procesos Bloqueados: Ninguno")
        self.lbl_bloqueados.pack(side=tk.BOTTOM)

        # Asociar el evento de cierre de la ventana con el método on_closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def generar_proceso(self):
        threading.Thread(target=self.so.generarProceso).start()
        self.actualizar_interfaz()

    def bloquear_proceso(self):
        if not self.so.get_colaProcesos().esta_vacia():
            proceso = self.so.get_colaProcesos().items[0]
            self.so.bloquearProceso(proceso)
            self.actualizar_interfaz()

    def desbloquear_proceso(self):
        threading.Thread(target=self.so.desbloquearProceso).start()
        self.actualizar_interfaz()

    def iniciar_procesos(self):
        threading.Thread(target=self.ejecutar_procesos).start()

    def ejecutar_procesos(self):
        while True:
            self.so.atenderProceso()
            self.actualizar_interfaz()
            self.root.after(1000)  # Esperar 1 segundo entre cada proceso

    def actualizar_interfaz(self):
        self.actualizar_tabla(self.so.get_procesosTerminados().items)
        self.actualizar_grafico(self.so.get_procesosTerminados().items)
        self.lbl_semaforo.config(text=f"Semáforo: {self.so.get_semaforo()}")
        self.actualizar_bloqueados()

    def actualizar_tabla(self, procesos):
        # Limpiar la tabla de manera segura
        for i in self.tree.get_children():
            try:
                self.tree.delete(i)
            except tk.TclError:
                pass
        for proceso in procesos:
            self.tree.insert("", "end", values=(proceso.get_id(), proceso.get_tiempoLlegada(), proceso.get_rafaga(), proceso.get_rafagaEjecutada(), proceso.get_tiempoComienzo(), proceso.get_tiempoFinal(), proceso.get_tiempoEspera(), proceso.get_tiempoRetorno()))

    def actualizar_grafico(self, procesos):
        self.ax.clear()
        for proceso in procesos:
            self.ax.broken_barh([(proceso.get_tiempoComienzo(), proceso.get_tiempoFinal() - proceso.get_tiempoComienzo())], (proceso.get_id() * 10, 9), facecolors=('tab:blue'))
        self.ax.set_xlabel('Tiempo')
        self.ax.set_ylabel('Procesos')
        self.ax.set_yticks([proceso.get_id() * 10 + 5 for proceso in procesos])
        self.ax.set_yticklabels([f'P{proceso.get_id()}' for proceso in procesos])
        self.canvas.draw()

    def actualizar_bloqueados(self):
        procesos_bloqueados = self.so.get_colaBloqueados().items
        if procesos_bloqueados:
            texto_bloqueados = "Procesos Bloqueados: " + ", ".join([f"P{proceso.get_id()}" for proceso in procesos_bloqueados])
        else:
            texto_bloqueados = "Procesos Bloqueados: Ninguno"
        self.lbl_bloqueados.config(text=texto_bloqueados)

    def on_closing(self):
        # Detener cualquier hilo en ejecución
        if hasattr(self, 'ejecutar_procesos_thread'):
            self.ejecutar_procesos_thread.join(0)
        self.root.destroy()
# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    so = SO(quantum=5)
    ventana = Ventana(root, so)
    root.mainloop()