from game.config import *
from data.profile import Profile
from ui.renderer import Renderer
import sys
import pygame

class ProfileMenu:
    def __init__(self, screen, storage, clock):
        
        self.screen = screen
        self.storage = storage
        self.clock = clock

        self.running = True

        self.selected_option = 0
        self.selected_profile = None

        self.renderer = Renderer()

        self.options = ["New Profile"]
        self.state = "select"
        self.name_input = ""

        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_interval = 0.5 

        
        profiles = self.storage.get_profiles()

        if len(profiles) != 0:
            for profile in profiles:
                self.options.append(profile.name)
        else:
            self.state = "create"

        self.scroll_index = 0
        self.max_visible = 5

    def run(self):

        while self.running:
            deltatime = self.clock.tick(FPS) / 1000

            self.handle_events()
            self.update(deltatime)
            self.draw()
            
        
        return self.selected_profile

    def update(self, deltatime):
        if self.state == "create":
            self.cursor_timer += deltatime

            if self.cursor_timer >= self.cursor_interval:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0

    
    def handle_events(self):
        if self.state == "select":
            self.handle_select_events()
        elif self.state == "create":
            self.handle_create_events()
    
    def draw(self):
        if self.state == "select":
            self.draw_select()
        elif self.state == "create":
            self.draw_create()
        
    def handle_select_events(self):

        mouse_pos = pygame.mouse.get_pos()
        menu_rects = self.renderer.get_menu_rects(self.options[self.scroll_index : self.scroll_index + self.max_visible]) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if self.scroll_index > 0:
                        self.scroll_index -= 1
                        
                elif event.button == 5:
                    if self.scroll_index < len(self.options) - self.max_visible:
                        self.scroll_index += 1

                elif event.button == 1:
                    choice = self.options[self.selected_option]
                    if choice == "New Profile":
                        self.state = "create"
                    else:
                        self.selected_profile = self.storage.get_profile(choice)
                        self.running = False

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                # Get rects ONLY for the items currently visible in the scroll window
                visible_items = self.options[self.scroll_index : self.scroll_index + self.max_visible]
                menu_rects = self.renderer.get_menu_rects(visible_items) 

                for i, (item_name, rect) in enumerate(menu_rects):
                    if rect.collidepoint(mouse_pos):
                        # The actual index in the master list is i + scroll_index
                        self.selected_option = i + self.scroll_index

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                    
                    if self.selected_option == len(self.options) - 1:
                        self.scroll_index = max(0, len(self.options) - self.max_visible)

                    elif self.selected_option < self.scroll_index:
                        self.scroll_index = self.selected_option

                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)

                    if self.selected_option == 0:
                        self.scroll_index = 0

                    elif self.selected_option >= self.scroll_index + self.max_visible:
                        self.scroll_index = self.selected_option - self.max_visible + 1

                elif event.key == pygame.K_RETURN:
                    choice = self.options[self.selected_option]

                    if choice == "New Profile":
                        self.state = "create"
                    
                    else:
                        profile = self.storage.get_profile(choice)
                        self.selected_profile = profile
                        self.running = False

                elif event.key == pygame.K_ESCAPE:
                    self.running = False

    
    def handle_create_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(self.name_input) == 3:
                    profile = Profile(self.name_input.upper())
                    
                    self.storage.save_profile(profile)
                    self.selected_profile = profile
                    self.running = False
            
                elif event.key == pygame.K_BACKSPACE:
                    self.name_input = self.name_input[:-1]
                
                elif len(self.name_input) < 3 and event.unicode.isalpha():
                    self.name_input += event.unicode.upper()

                elif event.key == pygame.K_ESCAPE:
                    self.state = "select"
    
    def draw_select(self):
        self.screen.fill(CREAM)
        start = self.scroll_index
        end = start + self.max_visible
        visible_items = self.options[start:end]

        self.renderer.draw_menu_items(self.screen, visible_items, self.options[self.selected_option])
        pygame.display.flip()
    
    def draw_create(self):
        self.screen.fill(CREAM)
        
        self.renderer.text_label(self.screen, FONT, "Enter 3 Letter Name for New Profile: ", RED, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2-100))
        
        display_text = self.name_input
        
        if len(self.name_input) < 3:
            input_color = RED
            
            if self.cursor_visible:
                display_text += '|'

        elif len(self.name_input) == 3:
            input_color = GREEN

        self.renderer.text_label(self.screen, FONT, display_text, RED, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

        pygame.display.flip()