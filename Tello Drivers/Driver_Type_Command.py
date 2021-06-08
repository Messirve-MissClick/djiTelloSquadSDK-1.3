import socket


def send_msg():
    global HEADER_LENGTH
    global client_socket
    global my_username
    
    while True:
        message = input()
        if message:
            message = message.encode('utf-8')
            message_header = f'{len(message):<{HEADER_LENGTH}}'.encode('utf-8')
            client_socket.send(message_header + message)


HEADER_LENGTH = 10
IP = '192.168.5.173'
PORT = 1235

my_username = input('Username: ')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP,PORT))
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f'{len(username):<{HEADER_LENGTH}}'.encode('utf-8')
client_socket.send(username_header + username)

send_msg()
