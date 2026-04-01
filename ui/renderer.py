import pygame
from game.config import *

class Renderer:
    def draw_snake(self, screen, snake):
        for pos in snake.position_list:
            pygame.draw.rect(screen, GREEN, (pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def draw_food(self, screen, active_food):
        for food in active_food:
            pygame.draw.rect(screen, FOOD_COLORS[food.type], (food.position[0]*CELL_SIZE, food.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def draw_grid(self, screen):
        grid_x, grid_y = int(SCREEN_WIDTH/CELL_SIZE), int(SCREEN_HEIGHT/CELL_SIZE)

        for i in range(1, grid_x):
            for j in range(1, grid_y):
                pygame.draw.line(screen, BLACK, (i*CELL_SIZE, 0), (i*CELL_SIZE, SCREEN_HEIGHT))
                pygame.draw.line(screen, BLACK, (0, j*CELL_SIZE), (SCREEN_WIDTH, j*CELL_SIZE))

    def text_label(self, screen, font, text, color, center_pos):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = center_pos
        screen.blit(text_surface, text_rect)
    
    def draw_menu_items(self, screen, item_list, selected_item):

        item_width, item_height = 400, 60
        v_gap = int(SCREEN_HEIGHT/(len(item_list)+2))

        for i, item in enumerate(item_list):
            center_x = SCREEN_WIDTH/2 
            center_y = v_gap*(i+2) 
             
            if selected_item == item:
                pygame.draw.rect(screen, GREEN, (center_x - (item_width/2), center_y - (item_height/2), item_width, item_height))
                self.text_label(screen, FONT, item, WHITE, (center_x, center_y))
            else:             
                pygame.draw.rect(screen, RED, (center_x - (item_width/2), center_y - (item_height/2), item_width, item_height))
                self.text_label(screen, FONT, item, WHITE, (center_x, center_y))
    
    def get_menu_rects(self, item_list):
        rects = []
        item_width, item_height = 400, 60
        v_gap = int(SCREEN_HEIGHT / (len(item_list) + 2))

        for i, item in enumerate(item_list):
            center_x = SCREEN_WIDTH / 2
            center_y = v_gap * (i + 2)
            rect = pygame.Rect(center_x - (item_width / 2), center_y - (item_height / 2), item_width, item_height)
            rects.append((item, rect))
        return rects