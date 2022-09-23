import pygame

from menu import HeadingMenu, Menu, Button
from dbms import dbms
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
        elif self.state == "sign_ menu":
            self.sign_menu.update()

    def open_sign_in(self) -> None:
        """open the sign in menu"""
        self.sign_menu = SignInMenu(self.return_start_menu)
        self.state = "sign_ menu"
    
    def open_sign_up(self) -> None:
        """open sign up menu"""
        self.sign_menu = SignUpMenu(self.return_start_menu)
        self.state = "sign_ menu"

    def return_start_menu(self) -> None:
        """returns to the start menu from sign in/up menus"""
        self.state = "start"

    def exit_game(self) -> None:
        """quits the game"""
        settings.GAME.exit_game()

class TextBox:
    """input text box to enter text"""
    def __init__(self, prompt: str, center_pos: tuple[float, float], type: str):
        self.screen = pygame.display.get_surface() # main screen for easy access

        self.rect = pygame.Rect(0,0,settings.WIDTH/settings.TEXT_BOX_WIDTH_SCALE,
                                settings.HEIGHT/settings.TEXT_BOX_HEIGHT_SCALE) # main input bar
        self.rect.center = center_pos

        font = pygame.font.Font(None, settings.TEXT_BOX_FONT_SIZE)
        self.prompt_text = font.render(prompt, True, settings.DARK_BROWN)          # text image
        self.prompt_rect = self.prompt_text.get_rect(bottomleft=self.rect.topleft) # text container
        self.prompt_rect.y -= settings.TEXT_BOX_TEXT_OFFSET

        self.active = False # if the user is currently inputting to this box

        self.type = type
        if type == "username":   # limit username range
            self.min_len = settings.MIN_USERNAME_LEN
            self.max_len = settings.MAX_USERNAME_LEN
        elif type == "password": # limit password range
            self.min_len = settings.MIN_PASSWORD_LEN
            self.max_len = settings.MAX_PASSWORD_LEN

        self.input_font = pygame.font.Font(None, 50)
        self.input_content = ""  # player input string
    
    def update(self) -> None:
        """draws and updates text box"""
        if not self.active: # change border colour if text box is active or not
            pygame.draw.rect(self.screen, settings.DARK_BROWN, self.rect.inflate(settings.TEXT_BOX_BORDER_WIDTH,
                                                                                 settings.TEXT_BOX_BORDER_WIDTH))
        else:
            pygame.draw.rect(self.screen, settings.LIGHT_BROWN, self.rect.inflate(settings.TEXT_BOX_BORDER_WIDTH,
                                                                                  settings.TEXT_BOX_BORDER_WIDTH))
        pygame.draw.rect(self.screen, "white", self.rect)    # draw main input box
        self.screen.blit(self.prompt_text, self.prompt_rect) # draw box title

        # draw player input
        if self.type == "username":
            input_text = self.input_font.render(self.input_content, True, settings.DARK_BROWN)
        else:
            input_text = self.input_font.render("*"*len(self.input_content), True, settings.DARK_BROWN)
        input_rect = input_text.get_rect(midleft=self.rect.midleft)
        input_rect.x += settings.TEXT_BOX_INPUT_OFFSET
        self.screen.blit(input_text, input_rect)

        self.user_input()
    
    def user_input(self) -> None:
        """user interaction with the text box"""
        if pygame.mouse.get_pressed()[0]: # change activity of box
            self.active = self.rect.collidepoint(pygame.mouse.get_pos())
        if not self.active: 
            return
        
        if not pygame.key.get_focused(): # no keys pressed
            return

        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            if event.key == pygame.K_BACKSPACE:
                self.input_content = self.input_content[0:len(self.input_content)-1]
                continue
            elif event.key == pygame.K_SPACE:
                continue # ignore space bar
            
            if len(self.input_content) < self.max_len:
                self.input_content += event.unicode

class SignUpMenu(HeadingMenu):
    """menu to create a new player account"""
    def __init__(self, return_start_menu):
        back_button = Button("back", (settings.WIDTH/10, settings.HEIGHT/15), 25,
            (settings.WIDTH/20+25, settings.HEIGHT-settings.HEIGHT/30-25), 
            settings.LIGHT_BROWN, settings.LIGHT_BROWN_HOVER, settings.DARK_BROWN, return_start_menu)
        confirm_button = Button("CONFIRM", (settings.WIDTH/6, settings.HEIGHT/8), 35,
            (settings.WIDTH/2, settings.HEIGHT-settings.HEIGHT/8), settings.LIGHT_BROWN, 
            settings.LIGHT_BROWN_HOVER, settings.DARK_BROWN, self.sign_up)
        super().__init__([back_button, confirm_button], "SIGN UP")

        self.username = TextBox("username", (settings.WIDTH/2, 
                         settings.HEIGHT/2-1.5*settings.HEIGHT/settings.TEXT_BOX_HEIGHT_SCALE), "username")
        self.password = TextBox("password", (settings.WIDTH/2, settings.HEIGHT/2), "password")
        self.confirm_password = TextBox("confirm password", (settings.WIDTH/2, 
                         settings.HEIGHT/2+1.5*settings.HEIGHT/settings.TEXT_BOX_HEIGHT_SCALE), "password")
        self.text_boxes = [self.username, self.password, self.confirm_password]

        self.error = ""                              # error for the player
        self.error_font = pygame.font.Font(None, 40) # font the error uses
    
    def update(self) -> None:
        """called once per frame"""
        super().update() # update heading menu

        for text_box in self.text_boxes: # update text boxes
            text_box.update()
        
        # display error
        error_text = self.error_font.render(self.error, True, settings.RED)
        error_rect = error_text.get_rect(midbottom = (settings.WIDTH/2, settings.HEIGHT/4))
        self.screen.blit(error_text, error_rect)
    
    def sign_up(self) -> None:
        """sign up with given credentials"""
        self.error = "" # reset error
        # username not in range
        if not(settings.MIN_USERNAME_LEN<=len(self.username.input_content)<=settings.MAX_USERNAME_LEN):
            self.error = f"username must be {settings.MIN_USERNAME_LEN}-{settings.MAX_USERNAME_LEN} characters"
            return
        # passwords not in range
        if not (settings.MIN_PASSWORD_LEN<=len(self.password.input_content)<=settings.MAX_PASSWORD_LEN and 
                settings.MIN_PASSWORD_LEN<=len(self.confirm_password.input_content)<=settings.MAX_PASSWORD_LEN):
            self.error = f"password must be {settings.MIN_PASSWORD_LEN}-{settings.MAX_PASSWORD_LEN} characters"
            return
        # passwords don't match
        if self.password.input_content != self.confirm_password.input_content:
            self.error = "passwords do not match"
            return
        # username already taken
        if dbms.user_exists(self.username.input_content):
            self.error = "username taken"
            return
        
        # No error, user able to sign up
        dbms.sign_up(self.username.input_content, self.password.input_content)
        settings.GAME.state = "main menu" # go to main menu

class SignInMenu(HeadingMenu):
    """menu to access player account"""
    def __init__(self, return_start_menu):
        back_button = Button("back", (settings.WIDTH/10, settings.HEIGHT/15), 25,
            (settings.WIDTH/20+25, settings.HEIGHT-settings.HEIGHT/30-25), 
            settings.LIGHT_BROWN, settings.LIGHT_BROWN_HOVER, settings.DARK_BROWN, return_start_menu)
        confirm_button = Button("CONFIRM", (settings.WIDTH/6, settings.HEIGHT/8), 35,
            (settings.WIDTH/2, settings.HEIGHT-settings.HEIGHT/8), settings.LIGHT_BROWN, 
            settings.LIGHT_BROWN_HOVER, settings.DARK_BROWN, self.sign_in)
        super().__init__([back_button, confirm_button], "SIGN IN")

        self.username = TextBox("username", (settings.WIDTH/2, 
                         settings.HEIGHT/2-settings.HEIGHT/settings.TEXT_BOX_HEIGHT_SCALE), "username")
        self.password = TextBox("password", (settings.WIDTH/2, 
                         settings.HEIGHT/2+settings.HEIGHT/settings.TEXT_BOX_HEIGHT_SCALE), "password")
        self.text_boxes = [self.username, self.password]

        self.error = ""                              # error for the player
        self.error_font = pygame.font.Font(None, 40) # font the error uses
    
    def update(self) -> None:
        """called once per frame"""
        super().update() # update heading menu

        for text_box in self.text_boxes: # update text boxes
            text_box.update()

        # display error
        error_text = self.error_font.render(self.error, True, settings.RED)
        error_rect = error_text.get_rect(midbottom = (settings.WIDTH/2, settings.HEIGHT/4))
        self.screen.blit(error_text, error_rect)
    
    def sign_in(self) -> None:
        """sign in with given credentials"""
        self.error = ""
        # username not in range
        if not(settings.MIN_USERNAME_LEN<=len(self.username.input_content)<=settings.MAX_USERNAME_LEN):
            self.error = f"username must be {settings.MIN_USERNAME_LEN}-{settings.MAX_USERNAME_LEN} characters"
            return
        # password not in range
        if not (settings.MIN_PASSWORD_LEN<=len(self.password.input_content)<=settings.MAX_PASSWORD_LEN):
            self.error = f"password must be {settings.MIN_PASSWORD_LEN}-{settings.MAX_PASSWORD_LEN} characters"
            return
        # invalid password
        if not dbms.sign_in(self.username.input_content, self.password.input_content):
            self.error = "invalid password"
            return
        
        # No error, user able to sign in
        dbms.load_progress(self.username.input_content)
        settings.GAME.state = "main menu"