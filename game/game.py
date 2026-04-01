from entities.snake import Snake
from systems.spawner import Spawner
from systems.level_manager import LevelManager
from systems.collision import CollisionSystem
from ui.renderer import Renderer
from game.config import *

import pygame
import sys

class Game:
    def __init__(self, screen, storage, clock, profile):
        
        self.active_profile = profile
        self.session_food = {"normal": 0, "big": 0, "speed": 0, "shrink": 0}
        
        self.running = True

        self.screen = screen
        self.clock = clock
        self.storage = storage
        self.collision_system = CollisionSystem()
        self.renderer = Renderer()
        self.snake = Snake()
        self.spawner = Spawner()
        self.level_manager = LevelManager()

        self.score = 0
    
        self.move_timer = 0
        self.move_delay = 0.1
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.snake.set_direction((0, -1))

                if event.key == pygame.K_e:
                    self.snake.grow(3)

                if event.key == pygame.K_f:
                    self.snake.shrink(1)

                if event.key == pygame.K_r:
                    self.snake.boost(5)

                elif event.key == pygame.K_a:
                    self.snake.set_direction((-1, 0))

                elif event.key == pygame.K_s:
                    self.snake.set_direction((0, 1))

                elif event.key == pygame.K_d:
                    self.snake.set_direction((1, 0))


    def update(self, deltatime):
        self.move_timer += deltatime

        if self.snake.remaining_boost_duration > 0:
            self.snake.remaining_boost_duration -= deltatime

            if self.snake.remaining_boost_duration <= 0:
                self.snake.reset_boost()
        
        if self.move_timer >= (self.move_delay/self.snake.speed):
            self.snake.move()
            self.level_manager.update(self.score)
            self.move_timer = 0
        
        self.spawner.update(deltatime, self.level_manager.level, self.snake)

        if self.collision_system.check_death(self.snake):
            self.end_game()

        collided_food = self.collision_system.check_food_collision(self.snake, self.spawner.active_food)

        if collided_food:
            self.handle_food(collided_food)

            if collided_food.type == "normal":
                self.spawner.normal_food_exists = False
            
            self.spawner.active_food.remove(collided_food)

    def render(self):
        self.screen.fill(CREAM)
        #self.renderer.draw_grid(self.screen)
        self.renderer.draw_snake(self.screen, self.snake)
        self.renderer.draw_food(self.screen, self.spawner.active_food)
        
        self.renderer.text_label(self.screen, FONT, f"Score: {self.score}", YELLOW, (SCREEN_WIDTH/2, 40))
        self.renderer.text_label(self.screen, FONT, f"Level: {self.level_manager.level}", BLUE, (SCREEN_WIDTH/2 - 50, 70))
        self.renderer.text_label(self.screen, FONT, f"Multiplier: {self.snake.multiplier}x", RED, (SCREEN_WIDTH/2 + 50, 70))

        pygame.display.flip()

    def handle_food(self, food):
        food.apply_effect(self.snake)
        self.score += food.points * self.snake.multiplier
        self.session_food[food.type] += 1
        self.level_manager.update(self.score)

    def end_game(self):
        for food_type, count in self.session_food.items():
            for _ in range(count):
                self.active_profile.add_food(food_type)
        
        self.active_profile.apply_game_result(self.score, self.level_manager.level)
        
        self.storage.save_profile(self.active_profile)
        self.storage.update_leaderboard(self.active_profile.name, self.score)
        
        self.running = False 


    def run(self):
        while self.running:
            deltatime = self.clock.tick(FPS) / 1000

            self.handle_events()
            self.update(deltatime)
            self.render()
        
        return self.score, self.level_manager.level, self.session_food, self.snake.length
           

