import socket
import select

HEADER_LENGTH = 10
IP = "192.168.5.173"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP,PORT))
server_socket.listen()

socket_list = [server_socket]
clients = {}

def recive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        
        if not len(message_header):
            return False
        
        message_lenght = int(message_header.decode('UTF-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_lenght)}
     
    except:
        return False

print('Server enabled')
while True:
    read_sockets, _, excepcion_sockets = select.select(socket_list, [], socket_list)
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            
            user = recive_message(client_socket)
            if user is False:
                continue
            
            socket_list.append(client_socket)
            clients[client_socket] = user
            username = user['data'].decode('utf-8')
            print(f'Accepted new connection from {client_address[0]}:{client_address[1]} username: {username}')
        else:
            message = recive_message(notified_socket)
            
            if message is False:
                clients_error_print = clients[notified_socket]['data'].decode('utf-8')
                print(f'Closed connection from {clients_error_print}')
                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            
            user = clients[notified_socket]
            userdata = user['data'].decode('utf-8')
            messagedata = message['data'].decode('utf-8')
            print(f'Recived message from {userdata}: {messagedata}')
            
            for client_socket in clients:
                if  client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
    
    for notified_socket in excepcion_sockets:
        socket_list.remove(notified_socket)
        del clients[notified_socket]