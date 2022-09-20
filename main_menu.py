from cProfile import run
import pygame

from menu import HeadingMenu, Button
from end_menu import EndMenu
from play import Play
from dbms import dbms
import settings

class MainMenu(HeadingMenu):
    def __init__(self):
        play_button = Button("PLAY", (settings.WIDTH/2, settings.HEIGHT/3.5), 225, 
                             (settings.WIDTH/2,settings.HEIGHT/2-50), settings.LIGHT_BLUE, settings.LIGHT_BLUE_HOVER, 
                             settings.DARK_BLUE, self.start_run)
        exit_button = Button("exit", (settings.WIDTH/10, settings.HEIGHT/15), 25,
                (settings.WIDTH/2, settings.HEIGHT-0.55*settings.HEIGHT/7.2),
                settings.LIGHT_BROWN, settings.LIGHT_BROWN_HOVER, settings.DARK_BROWN, self.exit_game)
        super().__init__([play_button, exit_button], "MAIN MENU")

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
        pass

    def exit_game(self) -> None:
        """calls the game's exit game method"""
        settings.GAME.exit_game()