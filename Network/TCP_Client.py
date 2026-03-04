import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('127.0.0.1', 11451))

while True:
    send_msg = input('Client side>>')
    client_socket.send(send_msg.encode('utf8'))
    if send_msg == 'quit':
        print('Client closing.')
        break
    msg = client_socket.recv(1024).decode('utf8')
    print(f"来自服务端的消息:{msg}")

client_socket.close()