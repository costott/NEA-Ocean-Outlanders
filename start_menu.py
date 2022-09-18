import pygame

from menu import Menu, Button
import settings
import tools

class StartMenu(Menu):
    """start menu when game first opened"""
    def __init__(self):
        sign_in_button = Button("sign in", (settings.WIDTH/5, settings.HEIGHT/3.6), 75, 
                (settings.WIDTH/2-0.75*settings.WIDTH/5, settings.HEIGHT/2+1.25*settings.HEIGHT/7.2), 
                settings.LIGHT_BROWN, settings.LIGHT_BROWN_HOVER, settings.DARK_BROWN, self.open_sign_in)
        sign_up_button = Button("sign up", (settings.WIDTH/5, settings.HEIGHT/3.6), 75, 
                (settings.WIDTH/2+0.75*settings.WIDTH/5, sign_in_button.rect.centery), 
                settings.LIGHT_BROWN, settings.LIGHT_BROWN_HOVER, settings.DARK_BROWN, self.open_sign_up)
        exit_button = Button("exit", (settings.WIDTH/10, settings.HEIGHT/15), 25,
                (settings.WIDTH/2, settings.HEIGHT-0.55*settings.HEIGHT/7.2),
                settings.LIGHT_BROWN, settings.LIGHT_BROWN_HOVER, settings.DARK_BROWN, self.exit_game)
        super().__init__([sign_in_button, sign_up_button, exit_button])

        self.state = "start" # start, sign_menu

        title_font = pygame.font.Font("assets/Pacifico-Regular.ttf", 125)
        
        self.title_text = title_font.render("Ocean Outlanders", True, settings.DARK_BLUE)
        self.title_rect = self.title_text.get_rect(center=(settings.WIDTH/2, 200))
    
    def update(self) -> None:
        """called once per frame"""
        if self.state == "start":
            # scroll background
            self.bg_scroll += settings.START_MENU_BG_SCROLL_SPEED * 1/tools.get_fps()
            if self.bg_scroll >= 0:
                self.bg_scroll = -settings.PIECE_SIZE

            super().update() # update menu

            self.screen.blit(self.title_text, self.title_rect)

    def open_sign_in(self) -> None:
        """open the sign in menu"""
        pass
    
    def open_sign_up(self) -> None:
        """open sign up menu"""
        pass

    def exit_game(self) -> None:
        """quits the game"""
        settings.GAME.exit_game()