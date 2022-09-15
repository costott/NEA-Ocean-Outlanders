import pygame

from boat_feature import BoatFeature
from boat import Boat, BoatImage
from cannon import Cannon
import settings
import tools

class PlayerBoat(Boat):
    """controllable player boat"""
    def __init__(self, groups: list[pygame.sprite.Group], start_pos: tuple[float, float]):
        super().__init__(groups, start_pos)
        self.z = 1

        self.state = "sailing" # current state of the boat (switching, steering, sailing, cannons)

        self.cannons.append(Cannon(self, (15,20), True, self.active_cannon0))    # left cannon
        self.cannons.append(Cannon(self, (-15, 20), False, self.active_cannon1)) # right cannon

        self.get_sails()

        main_sail_feature = BoatFeature("main_sail_blue_small.png", (0,-7), self.start_sailing)
        steering_wheel_featue = BoatFeature("steering_wheel.png", (0,-36), self.start_steering)
        self.boat_features = [main_sail_feature, steering_wheel_featue] # group non-cannon features together

        # all boat images to be used to compile main image
        self.images = [self.hull] + self.cannons + self.boat_features + self.sails 
        self.make_main_boat_image()

        self.max_speed = settings.BOAT_BASE_SPEED # maxmim speed the boat can move
        self.speed = 0             # speed starts at 0

        self.holding_space = False # if space is being held to make sure its lifted before acting again

        self.switch_timer = 0      # timer to count down when entering/exiting the switching state
    
    def get_sails(self) -> None:
        """get all player boat sail images"""
        self.main_sail = BoatImage("main_sail_blue.png", (0,-10))
        self.nest = BoatImage("nest.png", (0,self.main_sail.centre_offset.y-23))
        self.flag = BoatImage("flag_blue.png", (0,self.nest.centre_offset.y-10))
        self.small_sail = BoatImage("small_sail_blue.png", (0,31))
        self.sails = [self.main_sail, self.nest, self.flag, self.small_sail]
    
    def update(self) -> None:
        """called once per frame"""
        self.player_input()
        self.states()
        super().update() # boat update
    
    def player_input(self) -> None:
        """controls player input in any state"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not self.holding_space: # pressed space when allowed
            # can't spam space to constantly enter switching if already in the state
            if self.state != "enter switching" and self.state != "switching":
                self.state = "enter switching"                     # change state 
                self.switch_timer = settings.PB_STATE_SWITCH_TIME # start switch timer

        self.holding_space = keys[pygame.K_SPACE] # update whether the player's still holding space

    def states(self) -> None:
        """controls what the boat is doing in different states"""
        if self.state == "steering":
            self.steer()
        elif self.state == "sailing":
            self.sailing()
        elif self.state == "cannons":
            self.control_cannon()
        elif self.state == "enter switching":
            self.enter_switching()
        elif self.state[0:14] == "exit switching":
            self.exit_switching()
        elif self.state == "switching":
            self.switching()
    
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
        self.active_cannon.aim_cannon()             # aim active cannon
        for cannon in self.cannons: cannon.update() # update all cannons
        self.make_main_boat_image()                 # remake boat image

        if pygame.mouse.get_pressed()[0]: # left mouse clicked
            self.active_cannon.shoot()
    
    def enter_switching(self) -> None:
        """enter the switching state"""
        for sail in self.sails:
            # decrease sail alpha
            sail.alpha -= ((255-settings.PB_SAIL_HIDDEN_ALPHA)/settings.PB_STATE_SWITCH_TIME) * 1/tools.get_fps()
        
        for feature in self.boat_features:
            # increase feature alphas
            feature.alpha += (255/settings.PB_STATE_SWITCH_TIME) * 1/tools.get_fps()
        
        self.switch_timer -= 1/tools.get_fps()
        if self.switch_timer <= 0:
            self.switch_timer = 0 # stop timer
            for sail in self.sails: sail.alpha = settings.PB_SAIL_HIDDEN_ALPHA # make sure alphas are correct
            for feature in self.boat_features: feature.alpha = 255             
            self.state = "switching" # enter switching state
        
        self.make_main_boat_image() # remake image as alphas have changed
    
    def exit_switching(self) -> None:
        """exit the switching state"""
        for sail in self.sails:
            # increase sail alpha
            sail.alpha += ((255-settings.PB_SAIL_HIDDEN_ALPHA)/settings.PB_STATE_SWITCH_TIME) * 1/tools.get_fps()
        
        for feature in self.boat_features:
            # decrease feature alphas
            feature.alpha -= (255/settings.PB_STATE_SWITCH_TIME) * 1/tools.get_fps()
        
        self.switch_timer -= 1/tools.get_fps()
        if self.switch_timer <= 0:
            self.switch_timer = 0 # stop timer
            for sail in self.sails: sail.alpha = 255 # make sure alphas are correct
            for feature in self.boat_features: feature.alpha = 0             
            self.state = self.state[15:len(self.state)] # go to next state
        
        self.make_main_boat_image() # remake image as alphas have changed
    
    def switching(self) -> None:
        """logic whilst in the switching state"""
        for cannon in self.cannons: 
            cannon.feature_update()
        for feature in self.boat_features:
            feature.feature_update()
    
    def active_cannon0(self) -> None:
        """sets active cannon to cannon 0"""
        self.state = "exit switching-cannons"             # exit switching state
        self.switch_timer = settings.PB_STATE_SWITCH_TIME # start switch timer
        self.active_cannon = self.cannons[0]              # set active cannon

    def active_cannon1(self) -> None:
        """sets active cannon to cannon 1"""
        self.state = "exit switching-cannons"             # exit switching state
        self.switch_timer = settings.PB_STATE_SWITCH_TIME # start switch timer
        self.active_cannon = self.cannons[1]              # set active cannon

    def start_sailing(self) -> None:
        """switches to sailing state"""
        self.state = "exit switching-sailing"             # exit switching state
        self.switch_timer = settings.PB_STATE_SWITCH_TIME # start switch timer
    
    def start_steering(self) -> None:
        """switches to steering state"""
        self.state = "exit switching-steering"            # exit switching state
        self.switch_timer = settings.PB_STATE_SWITCH_TIME # start switch timer