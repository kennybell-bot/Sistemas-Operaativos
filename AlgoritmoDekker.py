import random

if __name__=='__main__':
    # flags to indicate if each thread is in
    # queue to enter its critical section
    thread1wantstoenter = False
    thread2wantstoenter = True
    completed = False
    
    #startThreads()


def Thread1():
    global thread1wantstoenter, thread2wantstoenter, completed
    doWhile=False
    while (completed == False or not doWhile):
        doWhile=True
        thread1wantstoenter = True


        # entry section
        # wait until thread2 wants to enter
        # its critical section
        while (thread2wantstoenter == True):
            pass
        

        # critical section

        # exit section
        # indicate thread1 has completed
        # its critical section
        thread1wantstoenter = False
        completed = True

        # remainder section


def Thread2():

    global thread1wantstoenter, thread2wantstoenter, completed
    doWhile=False
    while (completed == False or not doWhile) :
        doWhile=True
        thread2wantstoenter = True

        # entry section
        # wait until thread1 wants to enter
        # its critical section
        while (thread1wantstoenter == True):
            pass

        # critical section

        # exit section
        # indicate thread2 has completed
        # its critical section
        thread2wantstoenter = False
        completed = True
        # remainder section


Thread1()
Thread2()
