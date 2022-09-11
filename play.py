import pygame

import settings
import tools

class Play:
    """class for a run"""
    def __init__(self):
        self.screen = pygame.display.get_surface() # gets game screen for easy access
        self.UI = None          # holds the UI object
        self.pause_menu = None  # holds the run's pause menu

        self.screen_sprites = pygame.sprite.Group()  # sprites visible on screen
        self.collide_sprites = pygame.sprite.Group() # sprites that collide with boats
        self.cannonballs = pygame.sprite.Group()     # all active cannonballs
        self.create_map()

        self.paused = False     # pauses/resumes the run

        self.time = 0           # time spent in the run (in seconds)
    
    def create_map(self) -> None:
        """creates map at start of game"""
        pass
    
    def update(self) -> None:
        """called once per frame"""
        if not self.paused:
            self.screen_sprites.draw(self.screen)
            self.screen_sprites.update()

            self.timer()
    
    def timer(self) -> None:
        """timer counts up"""
        self.time += 1/tools.get_fps()