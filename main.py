import pygame
from game.menu import Menu
from game.config import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game Evolved")

    menu = Menu(screen)
    menu.run()

if __name__ == "__main__":
    main()