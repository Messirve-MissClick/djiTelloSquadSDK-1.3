import os
import socket
import select
import errno
import sys
from threading import Thread
from time import sleep

def keyboard_control():
    import KeyPressModule as kp
    global message
    from time import sleep

    kp.init()

    def getKeyboardInput():
        global message
        lr, fb, ud, yv = 0, 0, 0, 0

        speed = 50

        if kp.getKey("a"): lr = -speed

        elif kp.getKey("d"): lr = speed

        if kp.getKey("w"): fb = speed

        elif kp.getKey("s"): fb = -speed

        if kp.getKey("SPACE"):ud = speed

        elif kp.getKey("LSHIFT"): ud = -speed

        if kp.getKey("LEFT"):yv = -speed

        elif kp.getKey("RIGHT"): yv = speed

        #if kp.getKey("q"): me.land(); sleep(3)

        #if kp.getKey("e"): me.takeoff()

        return [lr, fb, ud, yv]

    while True:

        vals = getKeyboardInput()

        message = f'rc {vals[0]} {vals[1]} {vals[2]} {vals[3]}'
        sleep(0.05)


def send_msg():
    global HEADER_LENGTH
    global message
    global client_socket
    global message_header
    global my_username
    message = ''
    while True:

        if message:
            send_message = message.encode('utf-8')
            message_header = f'{len(send_message):<{HEADER_LENGTH}}'.encode('utf-8')
            client_socket.send(message_header + send_message)
            sleep(0.05)
            
# def recive_msg():
#     global HEADER_LENGTH
#     global client_socket
#     global message_header
#     global username_header
#     global username
#     global my_username
    
#     while True:
        
#         try:
#             while True:
#                 #recive things
#                 username_header = client_socket.recv(HEADER_LENGTH)
#                 if not len(username_header):
#                     print('connection closed by the server')
#                     sys.exit()
#                 username_length = int(username_header.decode('utf-8').strip())
#                 username = client_socket.recv(username_length).decode('utf-8')
                
#                 message_header = client_socket.recv(HEADER_LENGTH)
#                 message_lenght = int(message_header.decode('utf-8'))
#                 message = client_socket.recv(message_lenght).decode('utf-8')
                
#                 print(f'{username} > {message}')

#         except IOError as e:
#             if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
#                 print('Reading error', str(e))
#                 sys.exit()
#             continue
                    
#         except Exception as e:
#             print('General error',str(e))
#             sys.exit()

HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 1235

clear = lambda: os.system('cls')
clear()

my_username = 'Driver'
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP,PORT))
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f'{len(username):<{HEADER_LENGTH}}'.encode('utf-8')
client_socket.send(username_header + username)

thread1 = Thread(target= keyboard_control)       
thread2 = Thread(target=send_msg)
#thread3 = Thread(target=recive_msg)

thread1.start()
thread2.start()
#thread3.start()