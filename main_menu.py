import pygame

from menu import HeadingMenu, Button
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
            # update run
            pass
    
    def start_run(self) -> None:
        """starts a new run"""
        self.run = None # creates a new run
        self.state = "run"