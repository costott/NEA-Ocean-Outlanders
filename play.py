import pygame
import random
import csv

from enemy_spawner import EnemySpawner
from menu import HeadingMenu, Button
from player_boat import PlayerBoat
from map_piece import MapPiece
from port import Port
from hud import HUD
import settings
import tools

class Play:
    """class for a run"""
    def __init__(self):
        self.screen = pygame.display.get_surface() # gets game screen for easy access
        self.HUD = HUD()        # holds the HUD object

        # PAUSE MENU
        resume = Button("RESUME", (settings.WIDTH/2, settings.HEIGHT/3), 200, 
                (settings.WIDTH/2, settings.HEIGHT/2-settings.HEIGHT/16), settings.LIGHT_BLUE, 
                settings.LIGHT_BLUE_HOVER, settings.DARK_BLUE, self.resume)
        shop = Button("SHOP", (settings.WIDTH/4, settings.HEIGHT/8), 75, 
                (settings.WIDTH/2, settings.HEIGHT/2+settings.HEIGHT/4), settings.LIGHT_BLUE,  
                settings.LIGHT_BLUE_HOVER, settings.DARK_BLUE, settings.GAME.main_menu.open_shop)
        quit = Button("quit", (shop.rect.width, shop.rect.height), 75, 
                (settings.WIDTH/2, shop.rect.centery+shop.rect.height*1.25), settings.LIGHT_BROWN, settings.LIGHT_BROWN_HOVER, 
                settings.DARK_BROWN, settings.GAME.main_menu.return_main_menu)
        self.pause_menu = HeadingMenu([resume,shop,quit], "PAUSED")  # holds the run's pause menu

        self.screen_sprites = ScreenSpriteGroup()    # sprites visible on screen
        self.collide_sprites = pygame.sprite.Group() # sprites that collide with boats
        self.enemy_spawnable = pygame.sprite.Group() # places enemies can spawn
        self.boat_sprites = pygame.sprite.Group()    # all boats
        self.port_sprites = pygame.sprite.Group()    # all ports
        self.create_map()

        self.camera = Camera()

        self.enemy_spawner = EnemySpawner()

        self.paused = False     # pauses/resumes the run

        self.time = 0           # time spent in the run (in seconds)

        settings.current_run = self

        # RUN STATS
        self.kills = 0
        self.gold = 0
    
    def create_map(self) -> None:
        """creates map at start of game"""
        self.main_map_image = pygame.image.load(settings.MAIN_MAP_IMAGE).convert()
        self.main_map_rect = self.main_map_image.get_rect()

        player_spawns = []

        rock_nums = { # csv number to image number
            "48": 1,
            "49": 2,
            "50": 3,
            "64": 4,
            "65": 5,
            "66": 6,
        }

        layers = {
            "colliders": self.map_csv_list("colliders"),
            "rocks": self.map_csv_list("rocks"),
            "ports": self.map_csv_list("ports"),
            "player_spawn": self.map_csv_list("player spawn"),
            "spawnable": self.map_csv_list("spawnable")
        }
        map_height = len(layers["colliders"])   # number of map pieces vertically
        map_width = len(layers["colliders"][0]) # number of map pieces horizontally

        for row in range(map_height):
            for col in range(map_width):
                topleft = (col*settings.PIECE_SIZE, row*settings.PIECE_SIZE) # position of map piece

                for layer_name, csv_list in layers.items():
                    if csv_list[row][col] == "-1": continue # move on if empty

                    if layer_name == "colliders":
                        MapPiece([self.collide_sprites], topleft)
                    elif layer_name == "rocks":
                        rock_image = pygame.image.load(f"map/rocks/rock{rock_nums[csv_list[row][col]]}.png").convert_alpha()
                        MapPiece([self.screen_sprites, self.collide_sprites], topleft, rock_image)
                    elif layer_name == "player_spawn":
                        player_spawns.append(topleft)
                    elif layer_name == "spawnable":
                        MapPiece([self.enemy_spawnable], topleft)
                    elif layer_name == "ports":
                        Port([self.screen_sprites, self.port_sprites], topleft)

        self.player_boat = PlayerBoat([self.screen_sprites, self.boat_sprites], random.choice(player_spawns))
    
    def update(self) -> None:
        """called once per frame"""
        if not self.paused:
            self.camera.update()

            # draw main map image in correct screen position
            self.screen.blit(self.main_map_image, self.main_map_rect.topleft+self.camera.camera_move)

            # draw and update screen sprites
            self.screen_sprites.draw(self.screen, self.camera.camera_move)
            self.screen_sprites.update()

            self.enemy_spawner.update()

            self.timer()
            self.check_pause()

            self.HUD.draw()
        else:
            if not pygame.mouse.get_visible(): # make sure mouse is visible
                pygame.mouse.set_visible(True)

            self.pause_menu.update()
    
    def timer(self) -> None:
        """timer counts up"""
        self.time += 1/tools.get_fps()
    
    def check_pause(self) -> None:
        """checks if the game is paused"""
        self.paused = pygame.key.get_pressed()[pygame.K_ESCAPE]
    
    def resume(self) -> None:
        """resumes the game"""
        self.paused = False
    
    def map_csv_list(self, name: str) -> list:
        """returns a list from a given csv file for the map\n
        name is name in map/csv_files/map_[name].csv"""
        csv_list = []
        with open(f"map/csv_files/map_{name}.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                csv_list.append(row)
        return csv_list    

class Camera:
    """camera to position sprites on screen"""
    def __init__(self):
        self.screen_centre = pygame.math.Vector2(settings.WIDTH/2, settings.HEIGHT/2) # vector centre of screen

        self.camera_move = pygame.math.Vector2() # direction to move all sprites on map
    
    def update(self) -> None:
        """updates the distance to move sprites on screen"""
        self.camera_move =  self.screen_centre - pygame.math.Vector2(settings.current_run.player_boat.rect.center)

class ScreenSpriteGroup(pygame.sprite.Group):
    """sprite group for screen sprites"""
    def __init__(self):
        super().__init__() # initialise sprite group
    
    def draw(self, screen: pygame.Surface, camera_move: pygame.math.Vector2) -> None:
        """draw sprites to screen with correct screen position"""
        # loop through sprite sorted by their z values (higher z = drawn later)
        for sprite in sorted(self, key = lambda sprite: sprite.z):     
            # draw sprite to correct camera position on screen
            screen.blit(sprite.image, sprite.rect.topleft+camera_move) 