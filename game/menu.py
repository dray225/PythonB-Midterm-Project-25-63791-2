import pygame
import sys

from game.game import Game
from game.profile_menu import ProfileMenu
from ui.renderer import Renderer
from game.config import *
from systems.storage import Storage

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.storage = Storage()
        self.renderer = Renderer()
        self.active_profile = None
        self.options = ["Start Game", "Profile", "View High Scores", "Quit"]
        self.selected_option = 0

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

            
    
    def handle_events(self):

        mouse_pos = pygame.mouse.get_pos()
        menu_rects = self.renderer.get_menu_rects(self.options) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for item, rect in menu_rects:
                        if rect.collidepoint(mouse_pos):
                            self.selected_option = self.options.index(item)
                            self.activate_option()

            if event.type == pygame.MOUSEMOTION:
                for i, (item, rect) in enumerate(menu_rects):
                    if rect.collidepoint(mouse_pos):
                        self.selected_option = i

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.activate_option()
            

    def activate_option(self):
        option = self.options[self.selected_option]
        if option == "Start Game":

            if not self.active_profile:
                profile_menu = ProfileMenu(self.screen, self.storage, self.clock)
                self.active_profile = profile_menu.run()

            if self.active_profile:
                playing = True
                while playing:              
                    game = Game(self.screen, self.storage, self.clock, self.active_profile)
                    score, level, food, length = game.run()

                    playing = self.show_game_over(score, level, food, length)
                
        
        elif option == "Profile":
            profile_menu = ProfileMenu(self.screen, self.storage, self.clock)
            self.active_profile = profile_menu.run()
        
        elif option == "View High Scores":
            self.view_high_scores()

        elif option == "Quit":
            self.running = False
    
    def draw(self):
        self.screen.fill(CREAM)

        if self.active_profile:
            welcome_message =  f"Welcome {self.active_profile.name}!"
        else:
            welcome_message = "No Profile Selected."

        self.renderer.text_label(self.screen, FONT, welcome_message, RED, (SCREEN_WIDTH/2, 100))

        self.renderer.draw_menu_items(self.screen, self.options, self.options[self.selected_option])

        pygame.display.flip()

    def view_high_scores(self):
        leaderboard = self.storage.get_leaderboard()
        viewing = True

        while viewing:
            self.screen.fill(CREAM)
            self.renderer.text_label(self.screen, FONT, "TOP 3 SCORES", RED, (SCREEN_WIDTH/2, 50))
            
            for i, entry in enumerate(leaderboard):
                text = f"{i+1}. {entry['name']} - {entry['score']}"
                self.renderer.text_label(self.screen, FONT, text, BLACK, (SCREEN_WIDTH/2, 150 + (i*50)))
            
            self.renderer.text_label(self.screen, FONT, "Press ESC to Return", GREEN, (SCREEN_WIDTH/2, SCREEN_HEIGHT - 50))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    viewing = False
    
    def show_game_over(self, session_score, session_level, session_food, final_length):
        leaderboard = self.storage.get_leaderboard()
        # Check if the session score reached a Personal Best
        is_personal_best = session_score >= self.active_profile.high_score
        
        viewing = True
        while viewing:
            self.screen.fill(CREAM)
            
            # 1. Header
            self.renderer.text_label(self.screen, FONT, "GAME OVER", RED, (SCREEN_WIDTH/2, 50))
            
            # 2. Session Stats
            stats_y = 100
            pb_text = " (NEW PERSONAL BEST!)" if is_personal_best else ""
            self.renderer.text_label(self.screen, FONT, f"Score: {session_score}{pb_text}", BLACK, (SCREEN_WIDTH/2, stats_y))
            self.renderer.text_label(self.screen, FONT, f"Final Length: {final_length} | Level: {session_level}", BLACK, (SCREEN_WIDTH/2, stats_y + 30))
            
            # 3. Food Eaten this session
            food_text = "Food: " + ", ".join([f"{k.capitalize()}: {v}" for k, v in session_food.items() if v > 0])
            self.renderer.text_label(self.screen, FONT, food_text, GREEN, (SCREEN_WIDTH/2, stats_y + 70))

            # 4. Leaderboard Section
            self.renderer.text_label(self.screen, FONT, "TOP 3 LEADERBOARD", RED, (SCREEN_WIDTH/2, 250))
            for i, entry in enumerate(leaderboard):
                # If this entry is the one the player just achieved, highlight YELLOW
                color = YELLOW if (entry['name'] == self.active_profile.name and entry['score'] == session_score) else RED
                text = f"{i+1}. {entry['name']} - {entry['score']}"
                self.renderer.text_label(self.screen, FONT, text, color, (SCREEN_WIDTH/2, 300 + (i*40)))

            # 5. Instructions
            self.renderer.text_label(self.screen, FONT, "Press ENTER to Play Again", BLACK, (SCREEN_WIDTH/2, SCREEN_HEIGHT - 80))
            self.renderer.text_label(self.screen, FONT, "Press ESC for Main Menu", BLACK, (SCREEN_WIDTH/2, SCREEN_HEIGHT - 40))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True  # Signal to play again
                    if event.key == pygame.K_ESCAPE:
                        return False # Signal to go to menu