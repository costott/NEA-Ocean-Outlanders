import pygame

from boat import Boat, BoatImage
import settings
import tools

class PlayerBoat(Boat):
    """controllable player boat"""
    def __init__(self, groups: list[pygame.sprite.Group], start_pos: tuple[float, float]):
        super().__init__(groups, start_pos)
        self.z = 1

        self.state = "steering" # current state of the boat (switching, steering, sails, cannon)

        self.get_sails()
        self.images = [self.hull] + self.sails # all boat images to be used to compile main image
        self.make_main_boat_image()
    
    def get_sails(self) -> None:
        """get all player boat sail images"""
        self.main_sail = BoatImage("main_sail_blue.png", (0,0))
        self.nest = BoatImage("nest.png", (0,0))
        self.flag = BoatImage("flag_blue.png", (0,0))
        self.small_sail = BoatImage("small_sail_blue.png", (0,0))
        self.sails = [self.main_sail, self.nest, self.flag, self.small_sail]