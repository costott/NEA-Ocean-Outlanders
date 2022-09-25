import pygame

from menu import HeadingMenu, Button
from leaderboard import Leaderboard
from controls import Controls
from end_menu import EndMenu
from play import Play
from shop import Shop
from dbms import dbms
import settings

class MainMenu(HeadingMenu):
    def __init__(self):
        play_button = Button("PLAY", (settings.WIDTH/2, settings.HEIGHT/3.5), 225, 
                             (settings.WIDTH/2,settings.HEIGHT/2-50), settings.LIGHT_BLUE, settings.LIGHT_BLUE_HOVER, 
                             settings.DARK_BLUE, self.start_run)
        shop_button = Button("shop", (settings.WIDTH/4.2, settings.HEIGHT/7), 100,
                             (settings.WIDTH/10+settings.WIDTH/28, settings.HEIGHT-settings.HEIGHT/4), 
                             settings.LIGHT_BLUE, settings.LIGHT_BLUE_HOVER,settings.DARK_BLUE, self.open_shop)
        leaderboard_button = Button("leaderboard", (settings.WIDTH/2.75, settings.HEIGHT/7), 100,
                             (settings.WIDTH/2, shop_button.rect.centery), 
                             settings.LIGHT_BLUE, settings.LIGHT_BLUE_HOVER, settings.DARK_BLUE, self.open_leaderboard)
        controls_button = Button("controls", (shop_button.rect.width, shop_button.rect.height), 100,
                             (settings.WIDTH-shop_button.rect.centerx, shop_button.rect.centery),
                             settings.LIGHT_BLUE, settings.LIGHT_BLUE_HOVER, settings.DARK_BLUE, self.open_controls)
        exit_button = Button("exit", (settings.WIDTH/10, settings.HEIGHT/15), 25,
                             (settings.WIDTH/2, settings.HEIGHT-0.55*settings.HEIGHT/7.2),
                             settings.LIGHT_BROWN, settings.LIGHT_BROWN_HOVER, settings.DARK_BROWN, self.exit_game)
        super().__init__([play_button, shop_button, leaderboard_button, controls_button, exit_button], "MAIN MENU")

        self.state = "menu" # current state of the main menu
    
    def update(self) -> None:
        """called once per frame"""
        if self.state == "menu":
            super().update() # update menu
        elif self.state == "run":
            self.run.update()
        elif self.state == "complete run":
            self.complete_menu.update()
        elif self.state == "died run":
            self.died_menu.update()
        elif self.state == "shop":
            self.shop.update()
        elif self.state == "leaderboard":
            self.leaderboard.update()
        elif self.state == "controls":
            self.controls.update()
        
        if self.state != "run":
            if not pygame.mouse.get_visible(): # reset mouse to be visible
                pygame.mouse.set_visible(True)

    def start_run(self) -> None:
        """starts a new run"""
        self.run = Play() # creates a new run
        self.state = "run"
    
    def complete_run(self) -> None:
        """called when a port is interacted with to finish a run"""
        settings.GAME.player_stats.gold += self.run.gold # add run gold
        
        # update highscores
        settings.GAME.player_stats.highscore_time = max(settings.GAME.player_stats.highscore_time, self.run.time)
        settings.GAME.player_stats.highscore_wave = max(settings.GAME.player_stats.highscore_wave, self.run.enemy_spawner.current_wave)
    
        dbms.save_progress()
        self.complete_menu = EndMenu("RUN COMPLETE")
        self.state = "complete run"
    
    def died_run(self) -> None:
        """called when the player dies in a run"""
        self.died_menu = EndMenu("YOU DIED")
        self.state = "died run"
    
    def return_main_menu(self) -> None:
        """returns to main menu"""
        self.state = "menu"
        del self.run # delete current run
    
    def open_shop(self) -> None:
        """opens the shop"""
        self.shop = Shop(self.leave_menu) # create new shop
        self.state = "shop"               # menu's in the shop state
    
    def open_leaderboard(self) -> None:
        """opens the leaderboard"""
        self.leaderboard = Leaderboard(self.leave_menu) # create new leaderboard
        self.state = "leaderboard"
    
    def open_controls(self) -> None:
        """opens the controls screen"""
        self.controls = Controls(self.leave_menu) # create new controls screen
        self.state = "controls"
    
    def leave_menu(self) -> None:
        """returns to main menu from other menu"""
        self.state = "menu"

    def exit_game(self) -> None:
        """calls the game's exit game method"""
        settings.GAME.exit_game()