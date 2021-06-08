import os
import socket
import sys
from threading import Thread
from time import sleep
import KeyPressModule as kp

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

    if kp.getKey("q"):
        message = 'land'
        sleep(1)

    if kp.getKey("e"):
        message = 'takeoff'
        sleep(1)

    return [lr, fb, ud, yv]


def keyboard_control():
    global message


    kp.init()
    
    while True:

        vals = getKeyboardInput()

        message = f'rc {vals[0]} {vals[1]} {vals[2]} {vals[3]}'
        sleep(0.5)


def send_msg():
    global message
    
    HEADER_LENGTH = 10
    IP = '192.168.5.173'
    PORT = 1235


    my_username = 'Driver'
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP,PORT))
    client_socket.setblocking(False)

    username = my_username.encode('utf-8')
    username_header = f'{len(username):<{HEADER_LENGTH}}'.encode('utf-8')
    client_socket.send(username_header + username)
    
    message = ''
    comand_list = ['takeoff','land','flip']
    
    while True:

        if message:
            send_message = message.encode('utf-8')
            message_header = f'{len(send_message):<{HEADER_LENGTH}}'.encode('utf-8')
            client_socket.send(message_header + send_message)
            if message in comand_list:
                message = 'rc 0 0 0 0'
            sleep(1)
            

clear = lambda: os.system('cls')
clear()



thread1 = Thread(target= keyboard_control)       
thread2 = Thread(target=send_msg)


thread1.start()
thread2.start()
