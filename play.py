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

        self.screen_sprites = CameraSpriteGroup()  # sprites visible on screen
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
            self.screen_sprites.camera_draw()
            self.screen_sprites.update()

            self.timer()

            self.HUD.draw()
    
    def timer(self) -> None:
        """timer counts up"""
        self.time += 1/tools.get_fps()

class CameraSpriteGroup(pygame.sprite.Group):
    """sprite group affected by the camera"""
    def __init__(self) -> None:
        super().__init__() # initialise sprite group
        self.screen = pygame.display.get_surface() # gets screen for easy access
        self.player_offset = pygame.math.Vector2() # offset between player's real position and screen centre
        self.screen_centre = pygame.math.Vector2(settings.WIDTH/2, settings.HEIGHT/2) # vector of screen centre

        self.main_map_img = pygame.image.load(settings.MAIN_MAP_IMAGE).convert() # map map image
        self.main_map_rect = self.main_map_img.get_rect()                        # container for map image
    
    def camera_draw(self) -> None:
        """camera draw"""
        # calculate the player's distance from centre of screen
        self.player_offset = self.screen_centre - pygame.math.Vector2(settings.current_run.player_boat.rect.center)

        map_screen_position = self.main_map_rect.topleft + self.player_offset # position map
        self.screen.blit(self.main_map_img, map_screen_position)              # draw map on screen
    
        # loop through the sprites in the group, sorted by their z values (higher z = drawn later)
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.z): 
            screen_position = sprite.rect.topleft + self.player_offset # offset position to put to screen
            self.screen.blit(sprite.image, screen_position)            # draw sprite to screen