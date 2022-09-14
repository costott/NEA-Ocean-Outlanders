import pygame

from boat import BoatImage
import settings
import tools

class BoatFeature(BoatImage):
    def __init__(self, path: str, centre_offset: tuple[float, float], effect, alpha: int = 0):
        super().__init__(path, centre_offset, alpha) # initialise boat image

        self.screen_middle = pygame.math.Vector2(settings.WIDTH/2, settings.HEIGHT/2) # vector for middle of screen

        self.size = pygame.math.Vector2(self.image.get_size())       # current size of image
        self.unhover_size = self.size.copy()                         # size of image when mouse not hovering
        self.hover_size = self.size * settings.PB_FEATURE_GROW_SCALE # sime of image when mouse hovering

        self.effect = effect # function to be run on the player boat
    
    def feature_update(self) -> None:
        """called once per frame when player in switching state"""
        # get rect to correct positon and size
        self.rect = self.image.get_rect(center = self.screen_middle 
                                - self.centre_offset.rotate(-settings.current_run.player_boat.angle))

        self.hover()

    def hover(self) -> bool:
        """logic for mouse hovering over feature"""
        if not self.rect.collidepoint(pygame.mouse.get_pos()): # mouse not on feature
            if self.size.x > self.unhover_size.x: # needs to shrink
                self.size.x -= settings.PB_FEATURE_GROW_SPEED
                self.size.y -= settings.PB_FEATURE_GROW_SPEED
                self.image = pygame.transform.smoothscale(self.image, self.size) # remake image
                self.rect = self.image.get_rect(center=self.rect.center)         # remake rect
            return
        
        # hovering over feature
        if self.size.x < self.hover_size.x: # needs to grow
            self.size.x += settings.PB_FEATURE_GROW_SPEED
            self.size.y += settings.PB_FEATURE_GROW_SPEED
            self.image = pygame.transform.smoothscale(self.image, self.size) # remake image
            self.rect = self.image.get_rect(center=self.rect.center)         # remake rect
        
        if pygame.mouse.get_pressed()[0]:
            self.effect()