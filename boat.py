import pygame
import math

import settings
import tools

class BoatImage:
    """class for individual images on the main boat image"""
    def __init__(self, path: str, centre_offset: tuple[int, int], alpha: int = 255):
        self.image = pygame.image.load("assets/Boat/"+path).convert_alpha() # get image from path
        self.rect = self.image.get_rect()                    # create container around image

        # offset of the image from the centre of the main image
        self.centre_offset = pygame.math.Vector2(centre_offset) 
        self.alpha = alpha # opacity of the image (0=none, 255=full)

class Boat(pygame.sprite.Sprite): # boat is built upon pygame's sprite class
    """base boat class"""
    def __init__(self, groups: list[pygame.sprite.Group], start_pos: tuple[float, float]):
        super().__init__(groups)  # initialises the sprite
        self.pos = pygame.math.Vector2(start_pos) # position (x,y) of centre of boat

        self.hull = BoatImage("hull.png", (0,0))

        self.z = 0 # image screen 'depth'

        self.angle = 0                # 0 = north, +ve = anticlockwise (deg)
        self.angle_velocity = 0       # current angle velocity (deg/second)

        self.speed = settings.BOAT_BASE_SPEED # speed in angle's direction

        self.cannons = [] # boat's cannons

        self.collide_center = pygame.math.Vector2(99999, 99999)

    def make_main_boat_image(self) -> None:
        """compile all boat images into one image"""
        # make empty container for images (main_sail set by specific boat)
        orig_img = pygame.Surface((self.main_sail.rect.width, self.hull.rect.height+8), pygame.SRCALPHA).convert_alpha()
        rect = orig_img.get_rect()

        # align+draw images into correct place in the container (images set by specific boat)
        for boat_img in self.images:
            boat_img.rect.center = rect.center + boat_img.centre_offset # algin
            boat_img.image.set_alpha(boat_img.alpha)                    # set transparency
            orig_img.blit(boat_img.image, boat_img.rect)                # draw
        
        self.orig_img = pygame.transform.rotozoom(orig_img, 180, settings.BOAT_SCALE) # non-rotated image
        self.image = pygame.transform.rotozoom(self.orig_img, self.angle, 1)          # current image
        self.rect = self.image.get_rect()                                             # container around image
    
    def update(self) -> None:
        """called once per frame"""
        self.update_collide_range()

        self.rotate()
        self.move()
    
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
            self.pos.x = old_x # undo movement
            self.rect.center = self.pos
        
        old_y = self.pos.y # same thing for boat's y value I AM STUPID
        self.pos.y -= self.speed * math.cos(self.angle * (math.pi/180)) * 1/tools.get_fps()
        self.rect.center = self.pos
        if self.collision():
            self.pos.y = old_y
            self.rect.center = self.pos
    
    def collision(self) -> bool:
        """checks for boat collision with collide sprites"""
        for sprite in self.collide_sprites:
            if sprite.rect.collidepoint(self.rect.center):
                return True
        return False # no collisions
    
    def update_collide_range(self) -> None:
        """sees if the boat needs to update its colliders"""
        # boat went out of range in the x direction
        if abs(self.pos.x - self.collide_center.x) > settings.COLLIDE_SIZE: 
            self.update_colliders()
        # boat went out of range in the y direction
        elif abs(self.pos.y - self.collide_center.y) > settings.COLLIDE_SIZE: 
            self.update_colliders()

    def update_colliders(self) -> None:
        """makes new collide sprites with sprites in proper range"""
        self.collide_center = self.pos.copy()        # original centre of collide range
        self.collide_sprites = pygame.sprite.Group() # sprites in collide range
        for sprite in settings.current_run.collide_sprites:
            if abs(self.pos.x - sprite.rect.centerx) < settings.COLLIDE_SIZE:   # x in range
                self.collide_sprites.add(sprite)
            elif abs(self.pos.y - sprite.rect.centery) < settings.COLLIDE_SIZE: # y in range
                self.collide_sprites.add(sprite)