import pygame


def init():
    pygame.init()

    win = pygame.display.set_mode((400, 400))


def getKey(keyName):
    ans = False

    for eve in pygame.event.get(): pass

    key_input = pygame.key.get_pressed()

    my_key = getattr(pygame, 'K_{}'.format(keyName))

    # print('K_{}'.format(keyName))

    if key_input[my_key]:
        ans = True

    pygame.display.update()

    return ans


def main():
    if getKey("LEFT"):
        pass
        # print("Left key pressed")

    if getKey("RIGHT"):
        pass
        # print("Right key Pressed")


if __name__ == '__main__':

    init()

    while True:
        main()
