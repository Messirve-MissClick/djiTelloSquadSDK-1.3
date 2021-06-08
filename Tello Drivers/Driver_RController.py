import socket
from threading import Thread
from time import sleep
import KeyPressModule as keyboard


def getKeyboardInput():
    global message
    lr, fb, ud, yv = 0, 0, 0, 0

    speed = 50

    if keyboard.getKey("a"):
        lr = -speed

    elif keyboard.getKey("d"):
        lr = speed

    if keyboard.getKey("w"):
        fb = speed

    elif keyboard.getKey("s"):
        fb = -speed

    if keyboard.getKey("SPACE"):
        ud = speed

    elif keyboard.getKey("LSHIFT"):
        ud = -speed

    if keyboard.getKey("LEFT"):
        yv = -speed

    elif keyboard.getKey("RIGHT"):
        yv = speed

    if keyboard.getKey("q"):
        message = 'land'
        sleep(1)

    if keyboard.getKey("e"):
        message = 'takeoff'
        sleep(1)

    return [lr, fb, ud, yv]


def keyboard_control():
    global message

    keyboard.init()

    while True:
        vals = getKeyboardInput()

        message = f'rc {vals[0]} {vals[1]} {vals[2]} {vals[3]}'
        sleep(0.5)


def send_msg():
    global message

    header_length = 10
    ip = '192.168.5.173'
    port = 1235

    my_username = 'Driver'
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    client_socket.setblocking(False)

    username = my_username.encode('utf-8')
    username_header = f'{len(username):<{header_length}}'.encode('utf-8')
    client_socket.send(username_header + username)

    message = ''
    command_list = ['takeoff', 'land', 'flip']

    while True:

        if message:
            send_message = message.encode('utf-8')
            message_header = f'{len(send_message):<{header_length}}'.encode('utf-8')
            client_socket.send(message_header + send_message)
            if message in command_list:
                message = 'rc 0 0 0 0'
            sleep(1)


thread1 = Thread(target=keyboard_control)
thread2 = Thread(target=send_msg)

thread1.start()
thread2.start()
