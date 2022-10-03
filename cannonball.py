import pygame
import random
import math

from effects import ExplosionEffect, ChainEffect
import settings
import tools

class Cannonball(pygame.sprite.Sprite):
    def __init__(self, start_pos: tuple[float, float], angle: float, damage: float, shooter: str):
        super().__init__([settings.current_run.screen_sprites])#initialise groups
        self.image = pygame.image.load("assets/cannonball.png").convert_alpha() # cannonball image
        self.rect = self.image.get_rect(center=start_pos)                       # container around cannonball

        self.z = 2                                                              # drawing order on screen

        self.pos = pygame.math.Vector2(start_pos)                               # centre position
        self.angle = angle                                                      # angle cannonball is moving in

        self.damage = damage                                                    # amount of damage it deals
        
        self.shooter = shooter                                                  # who shot the cannonball
    
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
    
        for boat in settings.current_run.boat_sprites:
            if boat == settings.current_run.player_boat and self.shooter == "player":
                continue # don't let the player shoot itself
            elif boat != settings.current_run.player_boat and self.shooter == "enemy":
                continue # don't let enemies shoot each other

            if self.rect.colliderect(boat.rect): # check for collision
                boat.hit(self.damage) # damage boat
                self.effect()
                self.kill()

class ExplosiveCannonball(Cannonball):
    """cannonball that creates an explosion when it collides"""
    def __init__(self, start_pos: tuple[float, float], angle: float, damage: float, shooter: str):
        super().__init__(start_pos, angle, damage, shooter)

        self.image = pygame.image.load("assets/red_cannonball.png").convert_alpha() # explosive cannonball image

        self.explosion_sound = pygame.mixer.Sound("sound/explosion.mp3") # sound when explosion happens
        self.explosion_sound.set_volume(0.7)
    
    def effect(self) -> None:
        """explosive cannonball effect"""
        ExplosionEffect([settings.current_run.screen_sprites], self.pos)
        self.explosion_sound.play()

        for boat in settings.current_run.boat_sprites:
            if boat == settings.current_run.player_boat and self.shooter == "player":
                continue # don't let the player explode itself
            elif boat != settings.current_run.player_boat and self.shooter == "enemy":
                continue # don't let enemies explode each other

            distance = self.pos.distance_to(boat.pos)                    # boat's distance to middle of explosion
            if distance > settings.EXPLOSIVE_CANNONBALL_RADIUS: continue # out of range

            distance_fraction = distance/settings.EXPLOSIVE_CANNONBALL_RADIUS # fraction of total distance
            # fraction of explosion damage relative to distance fraction
            damage_multiplier = (settings.EXPLOSIVE_CANNONBALL_FALLOFF-1)*(distance_fraction**2) + 1

            # damage to deal
            damage = self.damage*settings.EXPLOSIVE_CANNONBALL_DAMAGE_MULTIPLIER * damage_multiplier

            boat.hit(damage)

class ChainingCannonball(Cannonball):
    """cannonball that chains to enemy boats when it collides"""
    def __init__(self, start_pos: tuple[float, float], angle: float, damage: float, shooter: str):
        super().__init__(start_pos, angle, damage, shooter)

        self.image = pygame.image.load("assets/white_cannonball.png").convert_alpha() # chaining cannonball image
    
    def effect(self) -> None:
        """effect when the chaining cannonball collides"""
        chains = self.chain(self.pos, settings.CHAINING_CANNONBALL_RADIUS, [])
        ChainEffect([settings.current_run.screen_sprites], 
                    self.damage*settings.CHAINING_CANNONBALL_DAMAGE_MULTIPLIER , self.pos, chains)
    
    def chain(self, start_pos: pygame.math.Vector2, radius: float, chains: list) -> list:
        """recurisvely chains to a random boat in the given range
        returns the positions in order of where to chain"""
        boats = [] # list of boats in range
        for boat in settings.current_run.boat_sprites: # get boats in range
            if boat == settings.current_run.player_boat and self.shooter == "player":
                continue # don't let the player chain to itself
            elif boat != settings.current_run.player_boat and self.shooter == "enemy":
                continue # don't let enemies chain each other
                
            if boat.pos == start_pos: continue # don't let boat chain to itself
                
            # boat is able to be chained if in range
            if start_pos.distance_to(boat.pos) <= radius: boats.append(boat)
        
        if len(boats) > 0: # chain if there's available boats
            chain_boat = random.choice(boats) # choose boat to chain to
            chains.append(chain_boat)
            chains = self.chain(chain_boat.pos, radius*settings.CHAINING_CANNONBALL_DECAY, chains) # chain to next boat
        
        return chains