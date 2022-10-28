import pygame
import random

from map_piece import MapPiece
import settings
import tools

class TemporaryUpgrades:
    """class holding the temporary upgrades active in a run"""
    def __init__(self):
        # GET TIMERS
        self.invincibility_timer = TemporaryUpgradeTimer(settings.INVINCIBILITY_TIME)
        self.double_damage_timer = TemporaryUpgradeTimer(settings.DOUBLE_DAMAGE_TIME)
        self.always_steering_timer = TemporaryUpgradeTimer(settings.ALWAYS_STEERING_TIME)
        self.faster_cannons_timer = TemporaryUpgradeTimer(settings.FASTER_CANNONS_TIME)

        self.timers = [self.invincibility_timer, self.double_damage_timer, self.always_steering_timer, 
                       self.faster_cannons_timer] # holds the timers to easily iterate through
        
        self.icons = [
            pygame.image.load("assets/TemporaryUpgrades/invincibility.png").convert_alpha(),
            pygame.image.load("assets/TemporaryUpgrades/double_damage.png").convert_alpha(),
            pygame.image.load("assets/TemporaryUpgrades/always_steering.png").convert_alpha(),
            pygame.image.load("assets/TemporaryUpgrades/fast_cannons.png").convert_alpha()
        ]
    
    def update(self) -> None:
        """called once per frame"""
        [timer.update() for timer in self.timers] # update timers

class TemporaryUpgradeTimer:
    """timer for temporary upgrades"""
    def __init__(self, start_time: float):
        self.active = False          # if the upgrade is active (timer going)
        self.timer = 0               # timer to count down

        self.start_time = start_time # initial time when timer starts
    
    def update(self) -> None:
        """called once per frame"""
        if not self.active: return      # don't need to tick down timer if it's done
        self.timer -= 1/tools.get_fps() # tick down timer

        if self.timer < 0: # timer finished
            self.timer = 0
            self.active = False
    
    def start_timer(self) -> None:
        """restarts the timer"""
        self.timer = self.start_time
        self.active = True

class TemporaryUpgradeSpawner(MapPiece):
    """spawner on the map for temporary upgrades"""
    def __init__(self, groups: list[pygame.sprite.Group], topleft: tuple):
        super().__init__(groups, topleft) # initialise map piece
        self.image = pygame.Surface((settings.PIECE_SIZE+10, settings.PIECE_SIZE), flags=pygame.SRCALPHA).convert_alpha()
        self.image_rect = self.image.get_rect()

        self.centre = pygame.math.Vector2(self.rect.center) # vector of centre of spawner

        # get sail image
        self.green_sail = pygame.image.load("assets/TemporaryUpgrades/green_sail.png").convert_alpha()
        self.green_sail_rect = self.green_sail.get_rect(center=self.image_rect.center)

        self.start_timer()
        self.upgrade = None # holds the upgrade it spawns
    
    def update(self) -> None:
        """called once per frame"""
        if not self.spawned:
            self.timer -= 1/tools.get_fps() # tick down timer

            if self.timer < 0: # timer finished
                self.spawn_upgrade()
        else:
            # player in range to pick up upgrade
            if self.centre.distance_to(settings.current_run.player_boat.pos) <= settings.TEMPORARY_UPGRADE_PICKUP_RADIUS:
                # reset timer for its upgrade
                settings.current_run.temporary_upgrades.timers[self.upgrade].start_timer()
                self.start_timer()
                # reset image to be transparent
                self.image = pygame.Surface((settings.PIECE_SIZE+10, settings.PIECE_SIZE), flags=pygame.SRCALPHA).convert_alpha()

    def start_timer(self) -> None:
        """restarts spawn timer"""
        self.timer = random.uniform(settings.MIN_TEMPORARY_UPGRADE_SPAWN_TIME, 
                                    settings.MAX_TEMPORARY_UPGRADE_SPAWN_TIME)
        self.spawned = False
    
    def spawn_upgrade(self) -> None:
        """spawns a temporary upgrade at the spawner"""
        # get number representing upgrade
        self.upgrade = random.randint(0,len(settings.current_run.temporary_upgrades.timers)-1)
        # reset image to be transparent
        self.image = pygame.Surface((settings.PIECE_SIZE+10, settings.PIECE_SIZE), flags=pygame.SRCALPHA).convert_alpha()

        self.image.blit(self.green_sail, self.green_sail_rect) # draw sail to image

        # get and draw upgrade icon to image
        upgrade_icon = settings.current_run.temporary_upgrades.icons[self.upgrade]
        upgrade_icon = pygame.transform.rotozoom(upgrade_icon, 0, 0.6)
        upgrade_icon_rect = upgrade_icon.get_rect(center=self.image_rect.center)
        self.image.blit(upgrade_icon, upgrade_icon_rect)

        self.spawned = True