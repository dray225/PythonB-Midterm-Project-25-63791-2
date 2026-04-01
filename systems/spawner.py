import random
from game.config import *
from entities.food import NormalFood, GoldenFood, ShrinkFood, SpeedFood

class Spawner:
    def __init__(self):
        self.normal_food_exists = False

        self.spawn_timer = 0
        self.spawn_interval = 2

        self.active_food = []

    def update(self, deltatime, level, snake):
        self.spawn_timer += deltatime

        if not self.normal_food_exists:
            self.spawn_normal(snake)

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.spawn_special(level, snake)

    def spawn_normal(self, snake):
        position = self.get_valid_position(snake)

        food = NormalFood(position)
        self.active_food.append(food)

        self.normal_food_exists = True

    def spawn_special(self, level, snake):
        roll = random.random()

        options = []

        if level >= 2:
            options.append("big")
        if level >= 3:
            options.append("shrink")
        if level >= 4:
            options.append("speed")

        if not options:
            return
        
        if roll > 0.2:
            return

        food_type = random.choice(options)
        position = self.get_valid_position(snake)

        if food_type == "big":
            food = GoldenFood(position)
        elif food_type == "shrink":
            food = ShrinkFood(position)
        elif food_type == "speed":
            food = SpeedFood(position)
        
        self.active_food.append(food)
    
    def get_valid_position(self, snake):
        while True:
            x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1)
            y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1)

            position = (x, y)

            if position in snake.position_list:
                continue
                
            if any(position == food.position for food in self.active_food):
                continue

            return position
    
