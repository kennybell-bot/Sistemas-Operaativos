from Cola import Cola
from Cliente import Cliente
from Cajero import Cajero
from tkinter import *
import random
import time
import threading

def ingresarCLiente(cantidadTransacciones):
    clienteNuevo = Cliente(cantidadTransacciones,len(cola.getItems())-1)
    cola.encolar(clienteNuevo)

def botonIngresar():
    ingresarCLiente(int(ingreso.get()))

def actualizarPantalla():
    global cadenatotal
    cadenatotal = ""
    print("---------------")
    for i in range(len(items)):
        if i>0:
            cadena = f"{items[i].getId()} con {items[i].getCantidadTransacciones()} transacciones\n"
            cadenatotal += cadena
    print(cadenatotal)

def generarescenario():
    for i in range(random.randint(1,15)):
        ingresarCLiente(random.randint(1,10))
        cola.actualizarReferencias()

    actualizarPantalla()

def avanzar():
    #while(not cola.esta_vacia()):
    cajero.atenderClientes(cola)
    actualizarPantalla()
    var1 = StringVar()
    var1.set(cadenatotal)
    label4.configure(textvariable=var1)
    var2 = StringVar()
    var2.set(f"Atendiendo {cajero.siguiente.getId()}")
    label2.configure(textvariable=var2)
    root.after(2000, avanzar)


def generarAleatorio():
    generarescenario()
    root.after(10000, generarAleatorio)

cajero = Cajero()
cola = Cola(cajero)
cantidadClientes = random.randint(1,15)
items = cola.getItems()
root = Tk()
hilo = threading.Thread(target=generarescenario)
hilo.start()

label2 = Label(root, text="Cajero:")
label2.pack()

label4 = Label(root, text="La fila esta vacia")
label4.pack()

mybutton = Button(root, text="Avanzar", command=avanzar)
mybutton.pack()

label5 = Label(root, text="Ingrese la cantiad de transacciones del nuevo cliente")
label5.pack()

ingreso = Entry()
ingreso.pack()

button2 = Button(root,text="Ingresar", command=botonIngresar)
button2.pack()

button3 = Button(root, text="Generar", command=generarAleatorio)
button3.pack()

root.geometry("800x600")
root.title("Ejercicio del banco")
root.mainloop()

print("End")