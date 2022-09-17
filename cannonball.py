import pygame
import math

import settings
import tools

class Cannonball(pygame.sprite.Sprite):
    def __init__(self, start_pos: tuple[float, float], angle: float, damage: float):
        super().__init__([settings.current_run.screen_sprites, settings.current_run.cannonballs])#initialise groups
        self.image = pygame.image.load("assets/cannonball.png").convert_alpha() # cannonball image
        self.rect = self.image.get_rect(center=start_pos)                       # container around cannonball

        self.z = 2                                                              # drawing order on screen

        self.pos = pygame.math.Vector2(start_pos)                               # centre position
        self.angle = angle                                                      # angle cannonball is moving in

        self.damage = damage                                                    # amount of damage it deals
    
    def update(self) -> None:
        """called once per frame"""
        self.pos.x -= settings.CANNONBALL_SPEED * math.sin(self.angle*(math.pi/180)) * 1/tools.get_fps() # move x
        self.pos.y -= settings.CANNONBALL_SPEED * math.cos(self.angle*(math.pi/180)) * 1/tools.get_fps() # move y

        self.collision()

        self.rect.center = self.pos
    
    def effect(self) -> None:
        """effect that runs when cannonball collides"""
        pass # base cannonball has no effect
    
    def collision(self) -> None:
        """checks for cannonball collision"""
        for sprite in settings.current_run.collide_sprites:
            if sprite.rect.colliderect(self.rect):
                self.effect() 
                self.kill()   # remove cannonball from groups
    
        # boat collision to be implemented later