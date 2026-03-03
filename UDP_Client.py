import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 客户端不需要bind,所以端口号由操作系统自动分配

while True:

    send_msg = input('Client side>>')
    client_socket.sendto(send_msg.encode('utf8'), ('127.0.0.1', 11451))
    if send_msg == 'quit':
        break
    msg, addr = client_socket.recvfrom(1024)
    print(f'来自服务端IP:{addr[0]},端口号{addr[1]}的消息:{msg.decode("utf8")}')

client_socket.close()