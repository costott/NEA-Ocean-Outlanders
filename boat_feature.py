import pygame

from boat import BoatImage
import settings
import tools

class BoatFeature(BoatImage):
    def __init__(self, path: str, centre_offset: tuple[float, float], effect, alpha: int = 0):
        super().__init__(path, centre_offset, alpha) # initialise boat image

        self.screen_middle = pygame.math.Vector2(settings.WIDTH/2, settings.HEIGHT/2) # vector for middle of screen

        self.effect = effect # function to be run on the player boat
    
    def feature_update(self) -> None:
        """called once per frame when player in switching state"""
        # get rect to correct positon and size
        self.rect = self.image.get_rect(center = self.screen_middle 
                                - self.centre_offset.rotate(-settings.current_run.player_boat.angle))

        self.hover()

    def hover(self) -> bool:
        """logic for mouse hovering over feature"""
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.effect()