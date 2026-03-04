from multiprocessing import Process, Pool
import time

def eat(name):
    for i in range (6):
        print(f"{name}正在吃饭{i}")
        time.sleep(0.5)

def work():
    for i in range (6):
        print(f"正在做作业{i}")
        time.sleep(0.5)

def game():
    for i in range (6):
        print(f"正在打游戏{i}")
        time.sleep(0.5)

if __name__ == "__main__":
    process_pool = Pool(2)
    process_pool.apply_async(eat, args=("张三", ))
    process_pool.apply_async(work)
    process_pool.apply_async(game)

    process_pool.close()
    process_pool.join()