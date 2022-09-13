import pygame

from boat import BoatImage
import settings
import tools

class Cannon(BoatImage):
    """cannon to shoot cannonballs"""
    def __init__(self, boat, centre_offset: tuple[float, float], start_angle: float):
        super().__init__("cannon.png", centre_offset) # initialises boat image
        self.relative_angle = 0    # angle relative to boat angle (0 = start angle)

        self.boat = boat           # boat the cannon is on

        self.orig_img = pygame.transform.rotozoom(self.image, start_angle, 1) # un rotated image
        self.rotate()              # make sure starting angle is correct
    
    def update(self) -> None:
        """called once per frame"""
        self.rotate()
    
    def rotate(self) -> None:
        """rotates image by angle"""
        self.image = pygame.transform.rotozoom(self.orig_img, self.boat.angle+self.relative_angle, 1)
        self.rect = self.image.get_rect(center = self.rect.center)

    def test_rotation(self) -> None:
        """quick rotation test"""
        self.relative_angle += 1
        # make sure 0 <= angle <= 360
        if self.relative_angle < 0: self.relative_angle += 360
        if self.relative_angle > 360: self.relative_angle -= 360