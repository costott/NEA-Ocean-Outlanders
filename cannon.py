import pygame
import math

from cannonball import Cannonball, ExplosiveCannonball, ChainingCannonball
from boat_feature import BoatFeature
import settings
import tools

class Cannon(BoatFeature):
    """cannon to shoot cannonballs"""
    def __init__(self, boat, centre_offset: tuple[float, float], points_left: bool, effect, damage: float, shooter: str):
        super().__init__("cannon.png", centre_offset, effect, 255) # initialises boat image
        self.relative_angle = 0    # angle relative to boat angle (0 = start angle)

        self.boat = boat           # boat the cannon is on
        self.points_left = points_left # whether the cannon points left or right

        self.orig_img = self.image # un rotated image
        self.rotate()              # make sure starting angle is correct

        self.pos = self.boat.pos - self.centre_offset.rotate(-self.boat.angle) # centre position

        self.fire_rate = settings.CANNONS_BASE_FIRE_RATE
        self.fire_timer = 0        # counts down to 0 when fired to tell the cannon when it can fire again
        self.holding_left_mouse = False # used to make sure mouse gets lifted before firing again

        self.damage = damage # amount of damage a shot cannonball does

        self.shooter = shooter # who is using the cannon (player/enemy)

        self.active_cannonball = Cannonball # current cannonball the cannon is shooting

        self.cannon_sound = pygame.mixer.Sound("sound/cannon.wav") # shoot cannon sound
        self.cannon_sound.set_volume(0.75)                         # volume of sound
    
    def update(self) -> None:
        """called once per frame"""
        self.rotate()
        self.timer()
        self.left_mouse()
    
    def rotate(self) -> None:
        """rotates image by angle"""
        self.image = pygame.transform.rotozoom(self.orig_img, self.relative_angle, 1) # new rotated image 
        # container around image
        self.rect = self.image.get_rect(center = self.boat.pos - self.centre_offset.rotate(-self.boat.angle))
        self.pos = self.rect.center # update self.pos
    
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
    
    def timer(self) -> None:
        """determines when the cannon can be shot again"""
        if self.fire_timer > 0: # only run when the timer has started
            self.fire_timer -= 1/tools.get_fps()      # decrease timer
            self.fire_timer = max(0, self.fire_timer) # limit timer minimum to 0
    
    def left_mouse(self) -> None:
        """checks when left mouse stopped being held"""
        if not self.holding_left_mouse: return

        self.holding_left_mouse = pygame.mouse.get_pressed()[0] # turns false when not pressing left mouse
    
    def shoot(self) -> None:
        """shoots cannon"""
        if not self.holding_left_mouse and self.fire_timer == 0:
            cannon_pos = self.pos
            self.active_cannonball(cannon_pos, self.boat.angle+self.relative_angle, self.damage, self.shooter) # create cannonball

            # get volume of cannon sound
            sound_multiplier = 1 - (settings.current_run.player_boat.pos - self.pos).magnitude()/settings.CANNONS_MAXIMUM_SOUND_DISTANCE
            sound_multiplier = max(sound_multiplier, 0) # make sure multiplier >= 0
            self.cannon_sound.set_volume(settings.CANNONS_MAXIMUM_VOLUME*sound_multiplier)

            self.cannon_sound.play()

            self.fire_timer = self.fire_rate # start fire timer
        
        self.holding_left_mouse = True # shoot only called when left mouse is pressed