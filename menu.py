import pygame
import math

import settings
import tools

class Button:
    """Interactible button in menus"""
    def __init__(self, text: str, size: tuple[float, float], text_size: int, center_pos: tuple[float, float], 
                 unhover_colour: pygame.Color, hover_colour: pygame.Color, border_colour: pygame.Color, action):
        """size: (width, height)"""
        self.rect = pygame.Rect(0,0,size[0],size[1])    # main rect for the button
        self.rect.center = center_pos                   # aligns rect to specified centre

        self.size = pygame.math.Vector2(size[0],size[1])            # current size of the button
        self.unhover_size = self.size.copy()                        # size of the button when not hovering over it
        self.hover_size = self.unhover_size * settings.BUTTON_GROW  # size of the button when hovering over it
        
        # image for the text on the button
        self.text = pygame.font.Font(None, text_size).render(text, True, settings.BUTTON_TEXT_COLOUR) 
        self.text_rect = self.text.get_rect(center = center_pos) # gets the text's rect to easily move the text

        self.unhover_colour = unhover_colour    # colour of the button when not hovering over it
        self.hover_colour = hover_colour        # colour of the button when hovering over it
        self.colour = self.unhover_colour       # current colour of the button

        self.border_colour = border_colour # colour of the border around buttons

        # holds whether the mouse button has already been pressed (to ignore holding the mouse down)
        self.clicked = True 

        self.action = action # function to be called when the button's pressed
    
    def draw(self, surface: pygame.Surface) -> None:
        """draws the button onto the specified surface"""
        pygame.draw.rect(surface, self.colour, self.rect) # draw main background colour
        pygame.draw.rect(surface, self.border_colour, 
                         self.rect.inflate(settings.BUTTON_BORDER_SIZE, settings.BUTTON_BORDER_SIZE), 
                         width=settings.BUTTON_BORDER_SIZE) # draw border
        surface.blit(self.text, self.text_rect) # draw text
    
    def update(self) -> None:
        """called once per frame"""
        self.mouse_interact()
    
    def mouse_interact(self) -> None:
        """mouse interaction with the button"""
        if not self.rect.collidepoint(pygame.mouse.get_pos()): # mouse outside button
            self.colour = self.unhover_colour       # re-colour button
            if self.size.x > self.unhover_size.x:   # shrink button back down to unhover size if it's not already
                self.size.x -= settings.BUTTON_GROW_SPEED
                self.size.y -= settings.BUTTON_GROW_SPEED
                self.rect = pygame.Rect((0,0), self.size) # makes new rect with adjusted size
                self.rect.center = self.text_rect.center  # places rect in correct place
            
            self.clicked = pygame.mouse.get_pressed()[0]
            return # next code is only for hovering
        
        self.colour = self.hover_colour     # re-colour button
        if self.size.x < self.hover_size.x: # grows button up to hover size if it's not already
            self.size.x += settings.BUTTON_GROW_SPEED
            self.size.y += settings.BUTTON_GROW_SPEED
            self.rect = pygame.Rect((0,0), self.size) # makes new rect with adjusted size
            self.rect.center = self.text_rect.center  # places rect in correct place
        
        if pygame.mouse.get_pressed()[0] and not self.clicked: # left mouse button clicked (and hovering over button)
            self.action() # do the button's action
            self.clicked = True
        elif not pygame.mouse.get_pressed()[0]:
            # reason for not pressing the button was that the mouse wasn't clicked
            self.clicked = False

class Menu:
    """base menu class which all menus will inherit from"""
    def __init__(self, buttons: list[Button]):
        self.buttons = buttons

        self.screen = pygame.display.get_surface() # gets the game screen to use to draw

        self.get_background()
        self.bg_scroll = -settings.PIECE_SIZE      # top of the background image
    
    def get_background(self) -> None:
        """gets the background for the menu"""
        rows = math.ceil(settings.HEIGHT/settings.PIECE_SIZE) + 1
        cols = math.ceil(settings.WIDTH/settings.PIECE_SIZE)

        water_image = pygame.image.load("assets/water.png").convert()

        self.background = pygame.Surface((settings.WIDTH, settings.HEIGHT + settings.PIECE_SIZE))
        # draw water images to background
        for row in range(rows):
            for col in range(cols):
                self.background.blit(water_image, (col*settings.PIECE_SIZE, row*settings.PIECE_SIZE))
    
    def update(self) -> None:
        """called once per frame"""
        self.screen.blit(self.background, (0,self.bg_scroll))

        for button in self.buttons:
            button.update()
            button.draw(self.screen)

class HeadingMenu(Menu):
    """base menu class with heading at top"""
    def __init__(self, buttons: list[Button], heading: str):
        super().__init__(buttons)
        
        # create heading text
        self.heading = pygame.font.Font(None, settings.HEADING_TEXT_SIZE).render(heading, True, 
                                                                                 settings.BUTTON_TEXT_COLOUR)

        self.heading_box = self.heading.get_rect().inflate(35, 80)  # create box around heading text
        self.heading_box.midtop = (settings.WIDTH/2,0)              # align box to top middle of screen

        # centre heading text in middle of box
        self.heading_rect = self.heading.get_rect(center = self.heading_box.center)
    
    def update(self) -> None:
        """called once per frame"""
        super().update() # Menu update

        # draw main bar and border
        pygame.draw.rect(self.screen, settings.LIGHT_BROWN, (0,0,settings.WIDTH,settings.BAR_HEIGHT)) 
        pygame.draw.rect(self.screen, settings.DARK_BROWN, (0,0,settings.WIDTH,settings.BAR_HEIGHT), 
                         width=settings.HEADING_BORDER_SIZE) 

        # draw heading box and border
        pygame.draw.rect(self.screen, settings.LIGHT_BROWN, self.heading_box)
        pygame.draw.rect(self.screen, settings.DARK_BROWN, self.heading_box, width=settings.HEADING_BORDER_SIZE)
        # gets rid of heading box border in main bar
        pygame.draw.rect(self.screen, settings.LIGHT_BROWN, (self.heading_box.left,settings.HEADING_BORDER_SIZE,
                         self.heading_box.width+settings.HEADING_BORDER_SIZE,
                         settings.BAR_HEIGHT-2*settings.HEADING_BORDER_SIZE))

        # draw heading text
        self.screen.blit(self.heading, self.heading_rect)