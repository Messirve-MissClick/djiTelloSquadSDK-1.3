
import socket
import errno
import sys


class Tello(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
               socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
        

    def send(self, message, verbose=True):
        ret = self.sock.sendto(bytes(message, 'utf-8'), (UDP_IP, UDP_PORT))
        if verbose:
            print(f'sent {message}')
        
       


HEADER_LENGTH = 10
IP = '192.168.5.173'
PORT = 1235

UDP_IP = "192.168.10.1"
UDP_PORT = 8889
 
clear = lambda: os.system('cls')
clear()

my_username = input('Username: ')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP,PORT))
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f'{len(username):<{HEADER_LENGTH}}'.encode('utf-8')
client_socket.send(username_header + username)
            
dron = Tello()
dron.send("command")

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
            dron.send(f'{message}')

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error',str(e))
        sys.exit()
