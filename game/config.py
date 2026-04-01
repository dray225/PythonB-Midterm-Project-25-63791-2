import pygame

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Grid
CELL_SIZE = 20

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CREAM = (253, 251, 212)
GREEN = (70, 128, 34)
RED = (201, 38, 57)
YELLOW = (237, 190, 19)
BLUE = (19, 30, 237)
AQUA = (53, 227, 240)

# Color Dict for Food
FOOD_COLORS = {
    "normal": RED,
    "big": YELLOW,
    "speed": BLUE,
    "shrink": AQUA
}

# Fonts
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 24)