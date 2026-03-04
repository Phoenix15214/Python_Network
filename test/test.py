from multiprocessing import Pipe

parent_conn, child_conn = Pipe()

# 子进程发送数据（此处模拟）
child_conn.send("hello")

# 检查是否有数据
if parent_conn.poll():
    msg = parent_conn.recv()
    print(msg)  # 输出 "hello"
else:
    print("No data")