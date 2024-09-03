from threading import Thread, current_thread

class Display:

    def evenNum(self):
        print(current_thread().name) 
        for i in range(1, 11):
            if i % 2 == 0:
                print(i)

    def oddNum(self):
        print(current_thread().name) 
        for i in range(1, 11):
            if i % 2 != 0:
                print(i)

    def printNum(self):
        print(current_thread().name) 
        for i in range(1, 101):
            print(i)


d = Display()

t0 = Thread(target=d.printNum)
t1 = Thread(target=d.evenNum)
t2 = Thread(target=d.oddNum)

t0.start()
t1.start()
t2.start()

# Wait for all threads to complete
t0.join()
t1.join()
t2.join()
