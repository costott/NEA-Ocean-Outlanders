import pygame

from player_boat import PlayerBoat
from hud import HUD
import settings
import tools

class Play:
    """class for a run"""
    def __init__(self):
        self.screen = pygame.display.get_surface() # gets game screen for easy access
        self.HUD = HUD()        # holds the HUD object
        self.pause_menu = None  # holds the run's pause menu

        self.screen_sprites = pygame.sprite.Group()  # sprites visible on screen
        self.collide_sprites = pygame.sprite.Group() # sprites that collide with boats
        self.cannonballs = pygame.sprite.Group()     # all active cannonballs
        self.create_map()

        self.paused = False     # pauses/resumes the run

        self.time = 0           # time spent in the run (in seconds)

        settings.current_run = self
    
    def create_map(self) -> None:
        """creates map at start of game"""
        self.player_boat = PlayerBoat([self.screen_sprites], (settings.WIDTH/2,settings.HEIGHT/2))
    
    def update(self) -> None:
        """called once per frame"""
        if not self.paused:
            self.screen_sprites.draw(self.screen)
            self.screen_sprites.update()

            self.timer()

            self.HUD.draw()
    
    def timer(self) -> None:
        """timer counts up"""
        self.time += 1/tools.get_fps()