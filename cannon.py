import pygame
import math

from boat import BoatImage
import settings
import tools

class Cannon(BoatImage):
    """cannon to shoot cannonballs"""
    def __init__(self, boat, centre_offset: tuple[float, float], points_left: bool):
        super().__init__("cannon.png", centre_offset) # initialises boat image
        self.relative_angle = 0    # angle relative to boat angle (0 = start angle)

        self.boat = boat           # boat the cannon is on
        self.points_left = points_left # whether the cannon points left or right

        self.orig_img = self.image # un rotated image
        self.rotate()              # make sure starting angle is correct
    
    def update(self) -> None:
        """called once per frame"""
        self.rotate()
    
    def rotate(self) -> None:
        """rotates image by angle"""
        self.image = pygame.transform.rotozoom(self.orig_img, self.relative_angle, 1) # new rotated image 
        self.rect = self.image.get_rect(center = self.rect.center)                    # container around image
    
    def aim_cannon(self) -> None:
        """player can rotate cannon with mouse"""
        mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos()) # vector of mouse's position
        cannon_screen_pos = pygame.math.Vector2(settings.WIDTH/2, settings.HEIGHT/2) - (
            self.centre_offset.rotate(-self.boat.angle))        # vector of cannon position on screen

        dy = mouse_pos.y-cannon_screen_pos.y # difference in y
        dx = mouse_pos.x-cannon_screen_pos.x # difference in x

        # angle between cannon and mouse
        screen_angle = math.atan2(dy, dx) * (180/math.pi)
        self.relative_angle = 270 - screen_angle - self.boat.angle # adjust relative angle
        
        # make sure 0 <= relative_angle <= 360
        if self.relative_angle > 360: self.relative_angle -= 360
        if self.relative_angle < 0: self.relative_angle += 360

        # limit angle
        if self.points_left:
            # allow angles from N-SW
            if 270 <= self.relative_angle <= 360: self.relative_angle = 0  # angles 270-360 stay 0   (N)
            if 135 <= self.relative_angle < 270: self.relative_angle = 135 # angles 135-270 stay 135 (SW)
        else: # cannon points right
            # allow angles for N-SE
            if 0 <= self.relative_angle <= 90: self.relative_angle = 0     # angles 0-90 stay 0      (N)
            if 90 < self.relative_angle <= 225: self.relative_angle = 225  # anlgles 90-225 stay 225 (SE)