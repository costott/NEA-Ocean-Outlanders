import pygame

from boat import Boat
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

class ChainEffect(pygame.sprite.Sprite):
    """effect that makes the chaining lightning"""
    def __init__(self, groups: list, damage: float, start_pos: pygame.math.Vector2, chains: pygame.sprite.Group):
        super().__init__(groups) # initialise sprite

        self.z = 2 # drawing order
        self.damage = damage # damage each lightning bolt does

        self.chains = chains               # queue of all boats to chain to
        self.current_chain_pos = start_pos # current start of chain
        self.current_chain_distance = 0    # current distance to next boat

        self.image = pygame.Surface((0,0), pygame.SRCALPHA) # empty image
        self.rect = self.image.get_rect()                   # empty rect

        self.zap_sound = pygame.mixer.Sound("sound/zap.wav") # sound when lightning chains

    def update(self) -> None:
        """called once per frame"""
        if len(self.chains) == 0: # finished queue
            self.kill()
            return 
        
        chain_vector = self.chains[0].pos - self.current_chain_pos # get whole vector of chain

        self.current_chain_distance += settings.CHAIN_SPEED * 1/tools.get_fps()                  # increase distance
        self.current_chain_distance = min(self.current_chain_distance, chain_vector.magnitude()) # limit maximum

        distance_fraction = self.current_chain_distance/chain_vector.magnitude() # get fraction of distance to move
        add_vector = chain_vector*distance_fraction                              # get vector to move

        # get screen position of points
        start_screen_pos = self.current_chain_pos + settings.current_run.camera.camera_move
        end_screen_pos = self.current_chain_pos + add_vector + settings.current_run.camera.camera_move
        
        # draw chain
        pygame.draw.line(settings.GAME.screen, "white", start_screen_pos, end_screen_pos, settings.CHAIN_WIDTH)

        if self.current_chain_distance == chain_vector.magnitude(): # reached end of chain - go to next
            self.current_chain_distance = 0
            
            self.zap_sound.play()
            self.chains[0].hit(self.damage)
            if self.chains[0].hp <= 0: # end chain if boat to chain to dies
                self.kill()
                return

            self.current_chain_pos = self.chains.pop(0).pos # dequeue front boat in queue