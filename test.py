import pygame
import sys 

from menu import HeadingMenu, Button
import settings

class Game:
    """class to manage the whole game"""
    def __init__(self):
        pygame.init()           
        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        settings.WIDTH, settings.HEIGHT = self.screen.get_size()
        self.clock = pygame.time.Clock() 
        self.running = True      

        self.background_colour = '#d0f2fd'

        button = Button("test", (250, 125), 40, (settings.WIDTH/2, settings.HEIGHT/2), settings.LIGHT_BROWN, '#BB7935', settings.DARK_BROWN, self.change_background)
        self.main_menu = HeadingMenu([button], "MAIN MENU")
    
    def change_background(self) -> None:
        self.background_colour = "#d0f2fd" if self.background_colour == "green" else "green"

    def run(self) -> None:
        """responsible for running the game - main game loop"""
        while self.running:
            self.update()
            self.clock.tick(settings.TARGET_FPS)
        sys.exit()                  
    
    def update(self) -> None:
        """called once per frame"""
        pygame.event.get()          
        
        self.screen.fill(self.background_colour)

        self.main_menu.update()

        pygame.display.update()    

def main():
    game = Game() # instantiate the game
    game.run()    # run the game

if __name__ == "__main__":
    main()