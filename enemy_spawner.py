import pygame
import random

from enemy_boat import EnemyBoat
import settings
import tools

class EnemySpawner:
    """responsible for spawning enemies and waves"""
    def __init__(self):
        # enemy stats
        self.current_enemy_hp = settings.ENEMY_BASE_HP
        self.current_enemy_dmg = settings.ENEMY_BASE_DMG
        self.current_enemy_spd = settings.ENEMY_BASE_SPD

        self.current_wave = 1         
        self.total_wave_enemies = settings.START_WAVE_NUM   # total enemies to be spawned in this wave
        self.wave_spawned_enemies = 0                       # enemies spawned in this wave
        self.wave_dead_enemies = 0                          # enemies killed in this wave
        self.finished_wave = False

        self.spawn_timer = 0      # timer to count down between spawns
        self.wave_break_timer = 0 # timer to count down between waves
    
    def update(self) -> None:
        """called once per frame"""
        # need to spawn enemies
        if self.wave_spawned_enemies < self.total_wave_enemies:
            self.spawn_timer -= 1/tools.get_fps()
            self.spawn_timer = max(self.spawn_timer, 0) # limit minimum

            if self.spawn_timer == 0: # timer finished
                self.spawn_enemies(self.total_wave_enemies-self.wave_spawned_enemies)
                self.spawn_timer = random.uniform(settings.MIN_SPAWN_TIME, settings.MAX_SPAWN_TIME)
            return
        
        # all enemies spawned and killed - end wave
        elif self.wave_spawned_enemies == self.total_wave_enemies == self.wave_dead_enemies and not self.finished_wave:
            self.wave_break_timer = settings.WAVE_BREAK_TIME # start wave break
            self.finished_wave = True                        # finished wave
        
        # all enemies spawned and killed - wave ended (in wave break)
        elif self.wave_spawned_enemies == self.total_wave_enemies == self.wave_dead_enemies and self.finished_wave:
            self.wave_break_timer -= 1/tools.get_fps()
            self.wave_break_timer = max(self.wave_break_timer, 0) # limit minimum

            if self.wave_break_timer == 0:
                self.increase_wave()
    
    def spawn_enemies(self, max_enemies: int) -> None:
        """spawn a random number of enemies"""
        # only spawn a maximum proportion of the total enemies
        if max_enemies > int(self.total_wave_enemies/settings.MAX_SPAWN_DIVIDE):
            max_enemies = int(self.total_wave_enemies/settings.MAX_SPAWN_DIVIDE)
        
        # get spawnable tiles in range
        spawn_choices = []
        for spawnable in settings.current_run.enemy_spawnable:
            if (settings.MIN_SPAWN_DISTANCE 
                <= settings.current_run.player_boat.pos.distance_to(pygame.math.Vector2(spawnable.rect.center)) 
                <= settings.MAX_SPAWN_DISTANCE): # spawnable within range
                spawn_choices.append(spawnable.rect.center)
        
        if len(spawn_choices) == 0: return # return if no choices

        # spawn random number of enemies in random spawnable locations
        enemy_count = random.randint(1, max_enemies)
        for _ in range(enemy_count):
            EnemyBoat([settings.current_run.screen_sprites], random.choice(spawn_choices))
        
        self.wave_spawned_enemies += enemy_count
    
    def increase_wave(self) -> None:
        """go to the next wave"""
        # increase wave and enemy stats
        self.current_wave += 1
        self.current_enemy_hp += settings.ENEMY_HP_ADD
        self.current_enemy_dmg += settings.ENEMY_DMG_ADD
        self.current_enemy_spd += settings.ENEMY_SPD_ADD

        self.total_wave_enemies += settings.WAVE_ENEMY_INCREASE
        self.wave_spawned_enemies = 0
        self.finished_wave = False