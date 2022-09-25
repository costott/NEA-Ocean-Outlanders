import pygame

from menu import HeadingMenu, Button
import settings
import tools

class Controls(HeadingMenu):
    """screen to show players the controls of the boat"""
    def __init__(self, return_method):
        back_button = Button("back", (settings.WIDTH/10, settings.HEIGHT/15), 25,
            (settings.WIDTH/2, settings.HEIGHT-0.55*settings.HEIGHT/7.2),
            settings.LIGHT_BROWN, settings.LIGHT_BROWN_HOVER, settings.DARK_BROWN, return_method)
        super().__init__([back_button], "CONTROLS")

        self.controls_image = pygame.image.load(settings.CONTROLS_IMAGE_LOCATION).convert_alpha()
        self.controls_image = pygame.transform.rotozoom(self.controls_image, 0, settings.CONTROLS_IMAGE_SCALE)
        self.controls_image_rect = self.controls_image.get_rect(center=(settings.WIDTH/2,settings.HEIGHT/2))
    
    def update(self) -> None:
        """called once per frame"""
        super().update() # update heading menu

        self.screen.blit(self.controls_image, self.controls_image_rect)