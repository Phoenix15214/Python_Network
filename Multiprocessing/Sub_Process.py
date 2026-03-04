from multiprocessing import Process
import time

# 写一个自定义的类继承Process
class Eat_Process(Process):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self)->None:
        for i in range (6):
            print(f"进程{self.name}吃饭{i}")
            time.sleep(0.5)

class Work_Process(Process):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self)->None:
        for i in range (6):
            print(f"进程{self.name}写作业{i}")
            time.sleep(0.5)

if __name__ == "__main__":
    p1 = Eat_Process("Process-1")
    p2 = Work_Process("Process-2")

    p1.start()
    p2.start()