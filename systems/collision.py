from game.config import *

class CollisionSystem:
    def check_food_collision(self, snake, active_food):

        head = snake.position_list[0]

        for food in active_food:
            if food.position == snake.position_list[0]:
                return food
        
        return None
    
    def check_death(self, snake):
        head = snake.position_list[0]
        
        # Wall Collision
        if (head[0] < 0 or head[0] >= SCREEN_WIDTH // CELL_SIZE or
            head[1] < 0 or head[1] >= SCREEN_HEIGHT // CELL_SIZE):
            return True
        
        # Self Collision
        if head in snake.position_list[1:]:
            return True
            
        return False