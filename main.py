import pygame
import sys 

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

        self.player_username = None # holds the player's username once signed up/logged in
        self.player_stats = None    # holds the player stats object once signed up/logged in

        self.state = "start"        # currest state of the game (start or main menu)
        self.start_screen = None    # holds the start menu
        self.main_menu = None       # holds the main menu
        
        settings.GAME = self        # puts the game object into settings

    def run(self) -> None:
        """responsible for running the game - main game loop"""
        while self.running:
            self.update()
            self.clock.tick(settings.TARGET_FPS)
        sys.exit()                  # exits the game when running set to false
    
    def update(self) -> None:
        """called once per frame"""
        pygame.event.get()          # has to be called to tell pygame the game is active and running
        
        self.screen.fill('#d0f2fd') # fills the screen a light blue

        if self.state == "start":       # updates and draws the start menu
            pass
        elif self.state == "main menu": # updates and draws the main menu
            pass

        pygame.display.update()     # updates the game screen so all drawn images are updated
    
    def load_progress(self) -> None:
        """loads player progress using username into player stats"""
        pass

    def save_progress(self) -> None:
        """saves player progress to username using player stats"""
        pass

def main():
    game = Game() # instantiate the game
    game.run()    # run the game

if __name__ == "__main__":
    main()