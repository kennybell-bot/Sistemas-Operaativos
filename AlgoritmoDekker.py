import random

if __name__=='__main__':
    thread1wantstoenter = True
    thread2wantstoenter = True
    completed = False
    



def Thread1():
    global thread1wantstoenter, thread2wantstoenter, completed
    doWhile=False
    while (completed == False or not doWhile):
        doWhile=True
        thread1wantstoenter = True



        while (thread2wantstoenter == True):
            print("El proceso 2 quiere entrar en la seccion critica, espere...")
            pass
        




        thread1wantstoenter = False
        print("El proceso 1 ha salido de la seccion critica")
        completed = True



def Thread2():

    global thread1wantstoenter, thread2wantstoenter, completed
    doWhile=False
    while (completed == False or not doWhile) :
        doWhile=True
        thread2wantstoenter = True

        while (thread1wantstoenter == True):
            print("El proceso 1 quiere entrar en la seccion critica, espere...")
            pass




        thread2wantstoenter = False
        print("El proceso 2 ha salido de la seccion critica")
        completed = True
        


Thread1()
Thread2()
