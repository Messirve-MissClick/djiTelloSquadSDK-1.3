import socket
import select

HEADER_LENGTH = 10
IP = "192.168.5.173"
PORT = 1235

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

socket_list = [server_socket]
clients = {}


def receive_message(socket_client):
    try:
        message_header = socket_client.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('UTF-8').strip())
        return {'header': message_header, 'data': socket_client.recv(message_length)}
    except:
        return False


print('Server enabled')
while True:
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)
            if user is False:
                continue

            socket_list.append(client_socket)
            clients[client_socket] = user
            username = user['data'].decode('utf-8')
            print(f'Accepted new connection from {client_address[0]}:{client_address[1]} username: {username}')
        else:
            message = receive_message(notified_socket)

            if message is False:
                clients_error_print = clients[notified_socket]['data'].decode('utf-8')
                print(f'Closed connection from {clients_error_print}')
                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            userdata = user['data'].decode('utf-8')
            message_data = message['data'].decode('utf-8')
            print(f'Received message from {userdata}: {message_data}')

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        socket_list.remove(notified_socket)
        del clients[notified_socket]
