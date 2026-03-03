import socket

connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connect_socket.bind(('', 11451))
# 数值表示服务器等待建立连接的客户端的最大个数
connect_socket.listen(114)
server_socket, client_addr = connect_socket.accept()

while True:
    # 正式开始传输
    msg = server_socket.recv(1024).decode('utf8')
    if msg == 'quit':
        print('Server off.')
        break
    print(f'来自客户端{client_addr[0]},端口号{client_addr[1]}的消息:{msg}')
    send_msg = input('Server side>>')
    server_socket.send(send_msg.encode('utf8'))

server_socket.close()
connect_socket.close()
