import os
import socket
import select
import errno
import sys
from threading import Thread
from time import sleep



def send_msg():
    global HEADER_LENGTH
    global message
    global client_socket
    global message_header
    global my_username
    
    while True:
        message = input()
        #print(f'{username} > {message}')
        # message = "" # makes a reader user
        if message:
            message = message.encode('utf-8')
            message_header = f'{len(message):<{HEADER_LENGTH}}'.encode('utf-8')
            client_socket.send(message_header + message)
            
def recive_msg():
    global HEADER_LENGTH
    global client_socket
    global message_header
    global username_header
    global username
    global my_username
    
    while True:
        
        try:
            while True:
                #recive things
                username_header = client_socket.recv(HEADER_LENGTH)
                if not len(username_header):
                    print('connection closed by the server')
                    sys.exit()
                username_length = int(username_header.decode('utf-8').strip())
                username = client_socket.recv(username_length).decode('utf-8')
                
                message_header = client_socket.recv(HEADER_LENGTH)
                message_lenght = int(message_header.decode('utf-8'))
                message = client_socket.recv(message_lenght).decode('utf-8')
                
                print(f'{username} > {message}')
                
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error', str(e))
                sys.exit()
            continue
                    
        except Exception as e:
            print('General error',str(e))
            sys.exit()

HEADER_LENGTH = 10
IP = '192.168.5.173'
PORT = 1235

clear = lambda: os.system('cls')
clear()

my_username = input('Username: ')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP,PORT))
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f'{len(username):<{HEADER_LENGTH}}'.encode('utf-8')
client_socket.send(username_header + username)
            
thread1 = Thread(target=send_msg)
thread2 = Thread(target=recive_msg)

thread1.start()
thread2.start()