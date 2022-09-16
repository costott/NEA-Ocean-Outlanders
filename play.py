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

        self.screen_sprites = ScreenSpriteGroup()    # sprites visible on screen
        self.collide_sprites = pygame.sprite.Group() # sprites that collide with boats
        self.cannonballs = pygame.sprite.Group()     # all active cannonballs
        self.create_map()

        self.camera = Camera()

        self.paused = False     # pauses/resumes the run

        self.time = 0           # time spent in the run (in seconds)

        settings.current_run = self
    
    def create_map(self) -> None:
        """creates map at start of game"""
        self.player_boat = PlayerBoat([self.screen_sprites], (settings.WIDTH/2,settings.HEIGHT/2))

        self.main_map_image = pygame.image.load(settings.MAIN_MAP_IMAGE).convert()
        self.main_map_rect = self.main_map_image.get_rect()
    
    def update(self) -> None:
        """called once per frame"""
        if not self.paused:
            self.camera.update()

            # draw main map image in correct screen position
            self.screen.blit(self.main_map_image, self.main_map_rect.topleft+self.camera.camera_move)

            # draw and update screen sprites
            self.screen_sprites.draw(self.screen, self.camera.camera_move)
            self.screen_sprites.update()

            self.timer()

            self.HUD.draw()
    
    def timer(self) -> None:
        """timer counts up"""
        self.time += 1/tools.get_fps()

class Camera:
    """camera to position sprites on screen"""
    def __init__(self):
        self.screen_centre = pygame.math.Vector2(settings.WIDTH/2, settings.HEIGHT/2) # vector centre of screen

        self.camera_move = pygame.math.Vector2() # direction to move all sprites on map
    
    def update(self) -> None:
        """updates the distance to move sprites on screen"""
        self.camera_move =  self.screen_centre - pygame.math.Vector2(settings.current_run.player_boat.rect.center)

class ScreenSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__() # initialise sprite group
    
    def draw(self, screen: pygame.Surface, camera_move: pygame.math.Vector2) -> None:
        # loop through sprite sorted by their z values (higher z = drawn later+)
        for sprite in sorted(self, key = lambda sprite: sprite.z):     
            # draw sprite to correct camera position on screen
            screen.blit(sprite.image, sprite.rect.topleft+camera_move) 