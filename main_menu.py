import pygame

from menu import HeadingMenu, Button
from end_menu import EndMenu
from play import Play
import settings

class MainMenu(HeadingMenu):
    def __init__(self):
        play_button = Button("PLAY", (settings.WIDTH/2, settings.HEIGHT/3.5), 225, 
                             (settings.WIDTH/2,settings.HEIGHT/2-50), settings.LIGHT_BLUE, settings.LIGHT_BLUE_HOVER, 
                             settings.DARK_BLUE, self.start_run)
        super().__init__([play_button], "MAIN MENU")

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
        settings.GAME.save_progress()
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