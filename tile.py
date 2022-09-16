import pygame

import settings
import tools

class Tile(pygame.sprite.Sprite):
    """interactible piece of the map"""
    def __init__(self, groups: list[pygame.sprite.Group], pos: tuple, 
            image: pygame.Surface = pygame.Surface((settings.TILESIZE, settings.TILESIZE))):
        super().__init__(groups)                     # initialise sprite
        self.image = image                           # create image
        self.rect = self.image.get_rect(topleft=pos) # create container for image
        
        self.z = 0                                   # set z value for drawing