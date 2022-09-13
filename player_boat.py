import pygame

from boat import Boat, BoatImage
from cannon import Cannon
import settings
import tools

class PlayerBoat(Boat):
    """controllable player boat"""
    def __init__(self, groups: list[pygame.sprite.Group], start_pos: tuple[float, float]):
        super().__init__(groups, start_pos)
        self.z = 1

        self.state = "cannons" # current state of the boat (switching, steering, sailing, cannons)

        self.cannons.append(Cannon(self, (15,20)))
        self.cannons.append(Cannon(self, (-15, 20)))
        self.active_cannon = self.cannons[0] # cannon being controlled when in the cannons state

        self.get_sails()
        # all boat images to be used to compile main image
        self.images = [self.hull] + self.cannons + self.sails 
        self.make_main_boat_image()

        self.max_speed = settings.BOAT_BASE_SPEED
    
    def get_sails(self) -> None:
        """get all player boat sail images"""
        self.main_sail = BoatImage("main_sail_blue.png", (0,-10))
        self.nest = BoatImage("nest.png", (0,self.main_sail.centre_offset.y-23))
        self.flag = BoatImage("flag_blue.png", (0,self.nest.centre_offset.y-10))
        self.small_sail = BoatImage("small_sail_blue.png", (0,31))
        self.sails = [self.main_sail, self.nest, self.flag, self.small_sail]
    
    def update(self) -> None:
        """called once per frame"""
        self.states()
        super().update() # boat update
    
    def states(self) -> None:
        """controls what the boat is doing in different states"""
        if self.state == "steering":
            self.steer()
        elif self.state == "sailing":
            self.sailing()
        elif self.state == "cannons":
            self.control_cannon()
    
    def steer(self) -> None:
        """steer boat with player input"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]: # steer anticlockwise
            self.angle_velocity += settings.PB_ANGLE_INP_ACCEL * 1/tools.get_fps()        # increase angle
            self.angle_velocity = min(self.angle_velocity, settings.BOAT_MAX_ANGLE_SPEED) # limit maximum
        
        if keys[pygame.K_d]: # steer clockwise
            self.angle_velocity -= settings.PB_ANGLE_INP_ACCEL * 1/tools.get_fps()         # decrease angle
            self.angle_velocity = max(self.angle_velocity, -settings.BOAT_MAX_ANGLE_SPEED) # limit minimum
    
    def sailing(self) -> None:
        """change the speed the boat is moving"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]: # increase speed
            self.speed += settings.PB_INP_ACCEL * 1/tools.get_fps() # increase speed
            self.speed = min(self.speed, self.max_speed)            # limit maximum
        
        if keys[pygame.K_s]: # decrease speed
            self.speed -= settings.PB_INP_ACCEL * 1/tools.get_fps() # decrease speed
            self.speed = max(self.speed, 0)                         # limit minimum
    
    def control_cannon(self) -> None:
        """control active cannnon"""
        for cannon in self.cannons: cannon.update()
        self.make_main_boat_image()