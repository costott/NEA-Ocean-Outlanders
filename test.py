import pygame
import sys 

from menu import Button
import settings

class Game:
    """class to manage the whole game"""
    def __init__(self):
        pygame.init()           
        self.screen = pygame.display.set_mode((800, 600))
        settings.WIDTH, settings.HEIGHT = self.screen.get_size()
        self.clock = pygame.time.Clock() 
        self.running = True      

        self.button = Button("test", (250, 125), 40, (settings.WIDTH/2, settings.HEIGHT/2), 'brown', 'red', 'black', print)

    def run(self) -> None:
        """responsible for running the game - main game loop"""
        while self.running:
            self.update()
            self.clock.tick(settings.TARGET_FPS)
        sys.exit()                  
    
    def update(self) -> None:
        """called once per frame"""
        pygame.event.get()          
        
        self.screen.fill('#d0f2fd')

        self.button.update()
        self.button.draw(self.screen)

        pygame.display.update()    

def main():
    game = Game() # instantiate the game
    game.run()    # run the game

if __name__ == "__main__":
    main()