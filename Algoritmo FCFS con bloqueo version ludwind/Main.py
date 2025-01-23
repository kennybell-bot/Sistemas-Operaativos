from Cola import Cola
from Proceso import Proceso
import random
import plotly.figure_factory as ff
from tkinter import *
from tkinter import ttk
import copy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import threading
from PIL import Image, ImageTk
import pandas as pd

root = Tk()
#Cola de procesos
lista_procesos = Cola()
tiempo = 0
nom =0
bloqueo = random.randint(1, 10)
tabla = "Historia de procesos\n"
procesoAnterior = None
procesosAGraficar = []
# Lista para almacenar los datos del diagrama de Gantt
gantt_data = []
hisotricoBloqueados = "Historico Procesos bloqueados: "

#Generación aleatoria de procesos
def generarProcesos():
    global tiempo
    global nom

    for i in range(random.randint(1, 10)):

        #Generación del primer proceso
        if i==0:
            procesoActual = Proceso(str(nom), tiempo, random.randint(1, 10))
        else:
            procesoActual = Proceso(str(nom), random.randint(procesoAnterior.getTiempoLLegada(), procesoAnterior.getTiempoLLegada()+5), random.randint(1, 10))
        lista_procesos.encolar(procesoActual)

        procesoAnterior = procesoActual
        nom=nom+1

#Funcion algoritmo FCFS
def atenderProcesos():

    global hisotricoBloqueados
    global tiempo
    global tabla
    global procesoAnterior
    global bloqueo
    
    print(f"**"+str(bloqueo)+"**")
    seccionOcupada = False
    procesoActivo = lista_procesos.frente()

    if lista_procesos.esta_vacia() == False:

        #Actualizacion del tiempo en pantalla
        print(f"Tiempo: {tiempo}")
        labelTiempo.config(text=f"Tiempo: {tiempo}")

        #Paso de estado nuevo a estado listo
        if procesoActivo.tiempo_llegada <= tiempo and procesoActivo.getEstado() == "Nuevo":
            procesoActivo.setEstado("Listo")
            print(f"Proceso {procesoActivo.nombre} en estado {procesoActivo.estado}")
            labelEstadoProceso.config(text=f"Proceso {procesoActivo.nombre} en estado {procesoActivo.estado}")

        #Paso del estado listo al estado ejecucion
        if seccionOcupada == False and procesoActivo.getEstado() == "Listo":
            procesoActivo.setEstado("Ejecución")
            if procesoAnterior == None:
                procesoActivo.setTiempoInicio(tiempo)
            elif procesoActivo.getTiempoLLegada() < procesoAnterior.getTiempoFinalizacion():
                procesoActivo.setTiempoInicio(procesoAnterior.getTiempoFinalizacion())
            else:
                procesoActivo.setTiempoInicio(procesoActivo.getTiempoLLegada())
            procesoActivo.calcularTiempos(bloqueo)
            print(f"Proceso {procesoActivo.nombre} en estado {procesoActivo.estado}")
            print(procesoActivo)
            labelEstadoProceso.config(text=f"Proceso {procesoActivo.nombre} en estado {procesoActivo.estado}")
            seccionOcupada = True

        #Bloqueo de proceso
        elif procesoActivo.getEstado() == "Ejecución" and procesoActivo.getRafaEjecucion() > bloqueo and procesoActivo.getBloqueado() == False and tiempo != procesoActivo.getTiempoInicio() and tiempo != procesoActivo.getTiempoFinalizacion():
            procesoActivo.setEstado("Bloqueado")
            print(f"Proceso {procesoActivo.nombre} en estado {procesoActivo.estado}")
            #Recalcular rafaga ejecutada
            procesoActivo.calcularTiempos(bloqueo)
            copiaProceso = copy.deepcopy(procesoActivo)
            procesosAGraficar.append(copiaProceso)
            procesoActivo.setRafagaEjecucion(bloqueo)
            print("Proceso recalculado quedo")
            print(procesoActivo)
            #Refereacia proceso anterior
            procesoAnterior = procesoActivo
            procesoActivo.setEstado("Listo")
            #Encolar proceso
            lista_procesos.encolar(lista_procesos.desencolar())
            hisotricoBloqueados += procesoActivo.getNombre()
            hisotricoBloqueados += "-"
            labelProcesosBloqueados.config(text=hisotricoBloqueados)
            tabla += str(procesoActivo)
            labelTabla.config(text=tabla)
            #Deoscupar la seccion critica
            seccionOcupada = False
        

        #Salida de la seccion critica
        if procesoActivo.getEstado() == "Ejecución" and tiempo == procesoActivo.tiempo_finalizacion:
            procesoActivo.setEstado("Terminado")
            print(f"Proceso {procesoActivo.nombre} en estado {procesoActivo.estado}")
            labelEstadoProceso.config(text=f"Proceso {procesoActivo.nombre} en estado {procesoActivo.estado}")
            procesoAnterior = lista_procesos.desencolar()
            procesosAGraficar.append(procesoAnterior)
            tabla += str(procesoAnterior)
            labelTabla.config(text=tabla)  
            print(len(lista_procesos.items))
            procesoActivo = lista_procesos.frente()
            seccionOcupada = False
            print(f"Cantidad de procesos: {len(lista_procesos.items)}")
            


    else:
        labelEstadoProceso.config(text="Cola vacía")
        labelProcesosBloqueados.config(text=" ")

    tiempo += 1
    root.after(1000, atenderProcesos)

generarProcesos()

def generarDiagrama():

    # Limpiar el canvas anterior si existe
    for widget in frame_diagrama.winfo_children():
        widget.destroy()
    
    gantt_data.clear()

    for i in procesosAGraficar:
        print(i)
        gantt_data.append(dict(Task=f"Proceso {i.nombre}", Start=i.getTiempoInicio(), Finish=i.getTiempoFinalizacion()))

    global ax,canvas,df

    df = pd.DataFrame(gantt_data)
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, row in df.iterrows():
        ax.barh(row['Task'], row['Finish'] - row['Start'], left=row['Start'], color='skyblue')

    ax.set_xlabel('Tiempo')
    ax.set_title('Diagrama de Gantt de Procesos')
    ax.grid(True)

    # Crear un canvas de matplotlib y agregarlo a la ventana de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

hilo = threading.Thread(target=generarProcesos)
def generacionProceosos():
    tabla = "Historia de procesos\n"
    hilo.start()



labelTiempo = Label(root, text="Tiempo")
labelTiempo.pack()
labelEstadoProceso = Label(root, text="Estado")
labelEstadoProceso.pack()
labelProcesosBloqueados = Label(root, text="")
labelProcesosBloqueados.pack()
labelTabla = Label(root, text=tabla)
labelTabla.pack()
mybutton = Button(root, text="Avanzar", command=atenderProcesos)
mybutton.pack()
btonDiagrama = Button(root, text="Generar diagrama", command=generarDiagrama)
btonDiagrama.pack()
botonGenerar = Button(root, text="Generar procesos", command=generacionProceosos)
botonGenerar.pack()

# Frame para el diagrama de Gantt
frame_diagrama = ttk.Frame(root, padding="10 10 10 10", style='TFrame')
frame_diagrama.pack(fill=BOTH, expand=True)


root.geometry("800x600")
root.title("Algoritmo FCFS")
root.mainloop()

