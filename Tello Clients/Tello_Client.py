import socket
import errno
import sys


class Tello(object):
    def __init__(self, timeout=5):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP

        # set timeout in seconds
        self.sock.settimeout(timeout)

    def send(self, command, verbose=True):
        ret = self.sock.sendto(bytes(command, 'utf-8'), (UDP_IP, UDP_PORT))
        if verbose:
            print(f"Sent +-> {command}")
            print('waiting for response...')

        # Get return data:
        try:
            data, server = self.sock.recvfrom(UDP_PORT)
            if verbose:
                print(f"Received +-> {data}")
            return data
        except socket.timeout:
            # Tello did not respond to command
            if verbose:
                print('Timeout, received no data.')
            return "timeout"


def receive_msg():
    global HEADER_LENGTH
    global client_socket
    global message_header
    global username_header
    global username
    global my_username
    drone = Tello()
    drone.send("command")

    while True:

        try:
            while True:
                # receive things
                username_header = client_socket.recv(HEADER_LENGTH)
                if not len(username_header):
                    print('connection closed by the server')
                    sys.exit()
                username_length = int(username_header.decode('utf-8').strip())
                username = client_socket.recv(username_length).decode('utf-8')

                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8'))
                message = client_socket.recv(message_length).decode('utf-8')

                print(f'{username} > {message}')
                drone.send(f'{message}')
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error', str(e))
                sys.exit()
            continue

        except Exception as e:
            print('General error', str(e))
            sys.exit()


HEADER_LENGTH = 10
IP = '192.168.5.173'
PORT = 1234

UDP_IP = "192.168.10.1"
UDP_PORT = 8889

my_username = input('Username: ')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f'{len(username):<{HEADER_LENGTH}}'.encode('utf-8')
client_socket.send(username_header + username)

receive_msg()
