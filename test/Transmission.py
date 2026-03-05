import socket
import cv2
import struct
from threading import Thread
from multiprocessing import Process, Pipe

send_pipe1, recv_pipe1 = Pipe()
send_pipe2, recv_pipe2 = Pipe()

def Video_Process(tx, rx):
    cap = cv2.VideoCapture(0)
    isConnected = False
    if not cap.isOpened():
        print("无法打开摄像头")
        exit()
    while True:
        if rx.poll():
            msg = rx.recv()
            if type(msg) == bool:
                isConnected = msg
            else:
                print(msg)
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contours = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        total_area = 0.0
        cx, cy = 0.0, 0.0
        if len(contours) > 0:
            # 提取最大面积轮廓
            largest_cnt = max(contours, key=cv2.contourArea)
            # 使用cv2.moments计算图形矩
            m = cv2.moments(largest_cnt)
            # 计算中心坐标
            # 防止除0
            if m['m00'] > 0:
                cx = int(m['m10'] / m['m00'])
                cy = int(m['m01'] / m['m00'])
                # 绘制中心点
                # cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
                # cv2.putText(frame, f'Avg X: {cx}', (10, 70),
                #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                # cv2.putText(frame, f'contour: {len(contours)}', (10, 30),
                #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                # for cnt in contours:
                #     cv2.drawContours(frame, cnt, -1, (0, 255, 0), 3)
        # cv2.imshow("image", frame)
        # cv2.waitKey(1)
        # send_msg = f"{cx}, {cy}\n"
        send_msg = [cx, cy]
        if isConnected:
            # print(send_msg)
            tx.send(send_msg)


def _send_by_firewater(data_list, socket):
    send_msg = ",".join(str(x) for x in data_list) + "\n"
    socket.send(send_msg.encode("utf8"))

def _send_by_justfloat(data_list, socket):
    format_string = '<' + 'f' * len(data_list)
    packed_data = struct.pack(format_string, *data_list)
    tail = b'\x00\x00\x80\x7f'
    socket.send(packed_data + tail)

def _send_thread(tx, rx, method, socket):
    while True:
            msg = rx.recv()
            try:
                if method == "firewater":
                    _send_by_firewater(msg, socket)
                elif method == "justfloat":
                    _send_by_justfloat(msg, socket)
            except:
                print("客户端断开连接")
                isConnected = False
                tx.send(isConnected)
                break

def _recv_thread(tx, rx, method, socket):
    while True:
        try:
            msg = socket.recv(1024).decode("utf8")
            if len(msg) == 0:
                break
            tx.send(msg)
        except:
            break

def Send_Process(tx, rx, method="justfloat"):
    if method not in ("justfloat", "firewater"):
        print("发送方式不正确")
        method = "justfloat"
        print("自动更改格式为justfloat")
    isConnected = False
    connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect_socket.bind(("", 11451))
    while True:    
        connect_socket.listen(3)
        server_socket, client_addr = connect_socket.accept()
        isConnected = True
        print("客户端已连接")
        tx.send(isConnected)
        t1 = Thread(target=_send_thread, args=(tx, rx, method, server_socket))
        t2 = Thread(target=_recv_thread, args=(tx, rx, method, server_socket))
        t1.start()
        t2.start()
        

if __name__ == "__main__":
    p1 = Process(target=Video_Process, args=(send_pipe1, recv_pipe2))
    p2 = Process(target=Send_Process, args=(send_pipe2, recv_pipe1))

    p1.start()
    p2.start()






