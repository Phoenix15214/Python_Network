import time
from multiprocessing import Process

def eat():
    for i in range (6):
        print(f"吃饭{i}")
        time.sleep(0.5)

def work():
    for i in range (6):
        print(f"做作业{i}")
        time.sleep(0.5)

if __name__ == '__main__':
    p1 = Process(target=eat, name="进程1")
    p2 = Process(target=work, name="进程2")

    p1.start()
    p2.start()