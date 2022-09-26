import pygame

import settings
import tools

class ExplosionEffect(pygame.sprite.Sprite):
    """effect that makes an explosion at a point"""
    def __init__(self, groups: list, pos: tuple):
        super().__init__(groups) # initialise sprite
        self.pos = pygame.math.Vector2(pos) # position of effect

        self.z = 2 # drawing order

        self.current_frame = 0 # current frame of the animation
        # timer to count down when to change frames
        self.frame_timer = settings.EXPLOSION_ANIMATION_SWITCH_TIME
        
        # all images for the animation
        image1 = tools.scaled_image("assets/Effects/explosion3.png", settings.EXPLOSION_SCALE)
        image2 = tools.scaled_image("assets/Effects/explosion2.png", settings.EXPLOSION_SCALE)
        image3 = tools.scaled_image("assets/Effects/explosion1.png", settings.EXPLOSION_SCALE)
        self.images = [image1, image2, image3]

        self.get_image()
    
    def get_image(self) -> None:
        """manages the image for the explosion"""
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect(center = self.pos)
    
    def update(self) -> None:
        """called once per frame"""
        # count down the timer
        self.frame_timer -= 1/tools.get_fps()
        if self.frame_timer < 0: # timer ended - animate
            self.current_frame += 1
            # animation finished
            if self.current_frame >= len(self.images)-1: self.kill()

            self.get_image()
            # start next frame of animation
            self.frame_timer = settings.EXPLOSION_ANIMATION_SWITCH_TIME