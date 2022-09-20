import pygame
import sys 

from player_stats import PlayerStats
from start_menu import StartMenu
from main_menu import MainMenu
from dbms import dbms
import settings

class Game:
    """class to manage the whole game"""
    def __init__(self):
        pygame.init()               # initialise pygame for use
        pygame.mixer.init()         # initialises pygame's sound system for use
        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN) # create the game screen
        settings.WIDTH, settings.HEIGHT = self.screen.get_size()
        self.clock = pygame.time.Clock() # creates the clock object
        self.running = True         # keeps the main game loop running

        # holds the player stats object once signed up/logged in (default for testing)
        self.player_stats = PlayerStats("test", 0, settings.PB_BASE_HP, settings.PB_BASE_DAMAGE, settings.PB_BASE_SPEED, 0, 0, 0, 0)

        self.state = "start"    # current state of the game (start or main menu)
        self.start_menu = StartMenu()    # holds the start menu
        self.main_menu = MainMenu() # holds the main menu
        
        settings.GAME = self        # puts the game object into settings

    def run(self) -> None:
        """responsible for running the game - main game loop"""
        while self.running:
            self.update()
            self.clock.tick(settings.TARGET_FPS)
        sys.exit()                  # exits the game when running set to false
    
    def update(self) -> None:
        """called once per frame"""
        pygame.event.get(exclude=pygame.KEYDOWN)  # has to be called to tell pygame the game is active and running
        
        self.screen.fill('#d0f2fd') # fills the screen a light blue

        if self.state == "start":       # updates and draws the start menu
            self.start_menu.update()
        elif self.state == "main menu": # updates and draws the main menu
            self.main_menu.update()

        pygame.display.update()     # updates the game screen so all drawn images are updated

    def exit_game(self) -> None:
        """closes the whole game"""
        pygame.quit()
        self.running = False

def main():
    game = Game() # instantiate the game
    game.run()    # run the game

if __name__ == "__main__":
    main()