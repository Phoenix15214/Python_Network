from threading import Thread
from multiprocessing import Process
import time

n = 500000000

def add(n: int):
    sum = 0
    while sum < n:
        sum+=1
    print(f"当前线程累加了{sum}次")

if __name__ == "__main__":
    t1 = Process(target=add, args=(n/2, ))
    t2 = Process(target=add, args=(n/2, ))
    t1.start()
    t2.start()
    start = time.time()
    t1.join()
    t2.join()
    end = time.time()
    print(f"处理耗时{end - start}秒")