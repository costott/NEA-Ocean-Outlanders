import pygame
import random
import math

from boat import Boat, BoatImage
from cannon import Cannon
import settings
import tools

class EnemyBoat(Boat):
    """boat with enemy behaviour"""
    def __init__(self, groups: list[pygame.sprite.Group], start_pos: tuple, 
                 start_hp: float, start_damage: float, start_speed: float):
        super().__init__(groups, start_pos)
        self.z = 0

        # STATS
        self.hp = start_hp
        self.damage = start_damage
        self.speed = start_speed
        
        self.state = "following"                         # current state the enemy is in (following/shooting)

        # add variation so enemies will be shooting from different distances
        self.shoot_variation = random.randint(-100, 100)
        self.shoot_distance = settings.ENEMY_SHOOT_DISTANCE + self.shoot_variation

        self.cannons.append(Cannon(self, (0,45), True, None, self.damage))
        self.get_sails()
        self.images = [self.hull] + self.cannons + self.sails # all boat images to be used to compile main image
        self.make_main_boat_image()

        self.shoot_timer = 0 # counts down to 0 when the enemy's shooting for enemy to shoot cannon
    
    def get_sails(self) -> None:
        """get all enemy boat sail images"""
        self.main_sail = BoatImage("main_sail_black.png", (0,-10))
        self.nest = BoatImage("nest.png", (0,self.main_sail.centre_offset.y-23))
        self.flag = BoatImage("flag_black.png", (0,self.nest.centre_offset.y-10))
        self.small_sail = BoatImage("small_sail_black.png", (0,31))
        self.sails = [self.main_sail, self.nest, self.flag, self.small_sail]
    
    def update(self) -> None:
        """called once per frame"""
        self.states()

        if self.state == "following":
            self.adjust_angle()
        if self.state == "shooting":
            self.try_shoot()
        
        super().update()
    
    def states(self) -> None:
        """changes the state of the enemy boat"""
        # if the boat is too far away from the player to shoot
        if abs(self.pos.distance_to(settings.current_run.player_boat.pos)) > self.shoot_distance:
            self.state = "following"

            if self.speed < settings.BOAT_BASE_SPEED: # needs to slow down
                self.speed += settings.ENEMY_ACCELERATION * 1/tools.get_fps() # increase speed
                self.speed = min(self.speed, settings.BOAT_BASE_SPEED)        # limit maximum
        else:
            self.state = "shooting"

            if self.speed > 0: # needs to speed up
                self.speed -= settings.ENEMY_ACCELERATION * 1/tools.get_fps() # decrease speed
                self.speed = max(self.speed, 0)                               # limit mimimum
    
    def adjust_angle(self) -> None:
        """changes the angle of the enemy to try to point at the player"""
        player = settings.current_run.player_boat # store player for easy access

        # calculate angle between enemy and player
        target_angle = math.atan2(player.pos.x-self.pos.x, player.pos.y-self.pos.y)
        target_angle = target_angle*(180/math.pi) + 180

        angle_diff = target_angle - self.angle # how much the current angle needs to change

        # change in angle is greater than the maximum change in angle per frame
        if abs(angle_diff) > settings.BOAT_MAX_ANGLE_SPEED * 1/tools.get_fps():
            self.angle += (angle_diff/abs(angle_diff)) * settings.BOAT_MAX_ANGLE_SPEED * 1/tools.get_fps()
        else:
            self.angle = target_angle
    
    def try_shoot(self) -> None:
        """enemy tries to shoot at player"""
        self.aim_cannon()
        self.cannons[0].update()
        self.make_main_boat_image() # remake image as cannon has changed angle

        if self.shoot_timer > 0: # timer is running
            self.shoot_timer -= 1/tools.get_fps()
            self.shoot_timer = max(self.shoot_timer, 0) # limit minimum
        
        if self.shoot_timer == 0: # timer ended
            self.cannons[0].shoot()

            # reset timer
            self.shoot_timer = random.uniform(settings.ENEMY_MIN_SHOOT_TIME, settings.ENEMY_MAX_SHOOT_TIME) 
    
    def aim_cannon(self) -> None:
        """aim cannon at player"""
        player_pos = settings.current_run.player_boat.pos # vector of player's position
        cannon_pos = self.pos - (self.cannons[0].centre_offset.rotate(-self.angle)) # vector of cannon position

        dy = player_pos.y-cannon_pos.y # difference in y
        dx = player_pos.x-cannon_pos.x # difference in x

        # angle between cannon and player
        angle = math.atan2(dy, dx) * (180/math.pi)
        relative_angle = 270 - angle - self.angle # adjust relative angle
        
        # make sure 0 <= relative_angle <= 360
        if relative_angle > 360: relative_angle -= 360
        if relative_angle < 0: relative_angle += 360

        self.cannons[0].relative_angle = relative_angle
    
    def hit(self, damage: float) -> None:
        """enemy boat takes damage"""
        self.hp -= damage

        if self.hp <= 0:
            self.die()
    
    def die(self) -> None:
        """what happens when an enemy dies"""
        settings.current_run.kills += 1                           # increase total kills
        settings.current_run.enemy_spawner.wave_dead_enemies += 1 # increasae wave kills
        self.kill() # remove enemy from all groups