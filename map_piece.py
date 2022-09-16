import pygame

import settings
import tools

class MapPiece(pygame.sprite.Sprite):
    """interactible piece of the map"""
    def __init__(self, groups: list[pygame.sprite.Group], topleft: tuple, 
         image: pygame.Surface = pygame.Surface((settings.PIECE_SIZE, settings.PIECE_SIZE))):
        super().__init__(groups)                         # initialise sprite
        self.image = image                               # create image
        self.rect = self.image.get_rect(topleft=topleft) # create container for image

        self.z = 0                                       # set z value for drawing