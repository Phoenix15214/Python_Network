import socket

# 创建服务端的UDP socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 前者为family类型,后者表示UDP协议
# IP为127.0.0.1时,只能本地通讯
# IP为本机IPV4地址时(218.197.235.5),可以和其他主机通讯
# 当IP地址为空字符时,表示该服务端绑定到所有的IP上
server_socket.bind(('127.0.0.1', 11451))

while True:
    msg, addr = server_socket.recvfrom(1024)# addr包含原地址和端口号
    decoded_msg = msg.decode('utf8')
    if decoded_msg == 'quit':
        print('Server off.')
        break
    print(f'来自客户端IP:{addr[0]},端口号{addr[1]}的消息:{decoded_msg}')
    
    send_msg = input('Server side>>')
    # sendto发送的数据不能是字符串，只能是字节数据
    server_socket.sendto(send_msg.encode('utf8'), addr)

server_socket.close()