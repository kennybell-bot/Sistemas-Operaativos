from Cola import Cola
from Proceso import Proceso
import random
import plotly.figure_factory as ff
from tkinter import *
import copy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import threading

#Cola de procesos
lista_procesos = Cola()
tiempo = 0
bloqueo = random.randint(1, 10)
tabla = "Historia de procesos\n"
procesoAnterior = None
procesosAGraficar = []

#Generación aleatoria de procesos
def generarProcesos():
    for i in range(random.randint(5, 10)):

        #Generación del primer proceso
        if i==0:
            procesoActual = Proceso(str(i), 0, random.randint(1, 10))
        else:
            procesoActual = Proceso(str(i), random.randint(procesoAnterior.getTiempoLLegada(), procesoAnterior.getTiempoLLegada()+5), random.randint(1, 10))
        lista_procesos.encolar(procesoActual)

        procesoAnterior = procesoActual

def generarDiagrama():

    df = []

    for i in procesosAGraficar:
        print(i)
        grafica = dict(Task=i.getNombre(), Start=i.getTiempoInicio(), Finish=i.getTiempoFinalizacion(), Resource='Complete')
        df.append(grafica)    

    colors = {'Not Started': 'rgb(220, 0, 0)',
            'Incomplete': (1, 0.9, 0.16),
            'Complete': 'rgb(0, 255, 100)'}

    fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True,group_tasks=True)
    fig.update_layout(xaxis=dict(type='linear', title='Tiempo'))

    fig.show()

#Funcion algoritmo FCFS
def atenderProcesos():

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
            hisotricoBloqueados = "Historico Procesos bloqueados\n"
            hisotricoBloqueados += procesoActivo.getNombre()
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

root = Tk()
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


root.geometry("800x600")
root.title("Algoritmo FCFS")
root.mainloop()

