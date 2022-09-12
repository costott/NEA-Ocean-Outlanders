import pygame
import math

import settings
import tools

class Boat(pygame.sprite.Sprite): # boat is built upon pygame's sprite class
    """base boat class"""
    def __init__(self, groups: list[pygame.sprite.Group], start_pos: tuple[float, float]):
        super().__init__(groups)  # initialises the sprite
        self.pos = pygame.math.Vector2(start_pos) # position (x,y) of centre of boat

        # --- TEMPORARY FOR TESTING ---
        self.orig_img = pygame.image.load("assets/test_boat_image.png").convert_alpha() # non-rotated image
        # make sure original image is pointing up (as angle 0 = north)
        self.orig_img = pygame.transform.rotozoom(self.orig_img, 180, settings.BOAT_SCALE)

        self.image = self.orig_img                          # curent image
        self.rect = self.image.get_rect(center = self.pos)  # container around image
        # --- TEMPORARY FOR TESTING ---

        self.z = 0 # image screen 'depth'

        self.angle = 0                # 0 = north, +ve = anticlockwise (deg)
        self.angle_velocity = 0       # current angle velocity (deg/second)
        # TEMPORARY FOR TESING: how much the angle velocity can change per second
        self.ANGLE_INPUT_ACCELERATION = settings.BOAT_MAX_ANGLE_SPEED/3

        self.speed = settings.BOAT_MAX_ANGLE_SPEED

        self.cannons = []
    
    def update(self) -> None:
        """called once per frame"""
        self.input()  # TEMPORARY FOR TESTING
        self.rotate()
        self.move()
    
    def input(self) -> None:
        """steer boat with player input"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]: # steer anticlockwise
            self.angle_velocity += self.ANGLE_INPUT_ACCELERATION * 1/tools.get_fps()      # increase angle
            self.angle_velocity = min(self.angle_velocity, settings.BOAT_MAX_ANGLE_SPEED) # limit maximum
        
        if keys[pygame.K_d]: # steer clockwise
            self.angle_velocity -= self.ANGLE_INPUT_ACCELERATION * 1/tools.get_fps()       # decrease angle
            self.angle_velocity = max(self.angle_velocity, -settings.BOAT_MAX_ANGLE_SPEED) # limit minimum
    
    def rotate(self) -> None:
        """rotates boat by its angle"""
        self.angle += self.angle_velocity * 1/tools.get_fps() # change angle by angle velocity

        # make sure 0 <= angle <= 360
        if self.angle < 0: self.angle += 360
        if self.angle > 360: self.angle -= 360

        self.image = pygame.transform.rotozoom(self.orig_img, self.angle, 1) # angle image correctly
        self.rect = self.image.get_rect() # re-make container around image
    
    def move(self) -> None:
        """attemps to move the boat"""
        old_x = self.pos.x # save old x in case it has to undo
        self.pos.x -= self.speed * math.sin(self.angle * (math.pi/180)) * 1/tools.get_fps() # move x
        self.rect.center = self.pos # move boat
        if self.collision():
            self.pos.x = old_x
        
        old_y = self.pos.x # same thing for boat's y value
        self.pos.y -= self.speed * math.cos(self.angle * (math.pi/180)) * 1/tools.get_fps()
        self.rect.center = self.pos
        if self.collision():
            self.pos.y = old_y
    
    def collision(self) -> bool:
        """checks for boat collision with collide sprites"""
        for sprite in settings.current_run.collide_sprites:
            if sprite.rect.collidepoint(self.rect.center):
                return True
        return False # no collisions