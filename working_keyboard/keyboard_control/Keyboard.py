

import KeyPressModule as kp

from time import sleep

kp.init()

def getKeyboardInput():

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

    print(f'rc {vals[0]} {vals[1]} {vals[2]} {vals[3]}')

    sleep(1)