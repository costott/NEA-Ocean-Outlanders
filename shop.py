import pygame

from menu import HeadingMenu, Button
from dbms import dbms
import settings
import tools

class ShopButton(Button):
    """button on shop to buy an upgrade"""
    def __init__(self, center_pos: tuple[float, float], price: int, action):
        self.screen = pygame.display.get_surface() # screen for easy access

        # create button
        main_rect_size = (settings.WIDTH/settings.SHOP_BUTTON_WIDTH_SCALE,settings.HEIGHT/
                          settings.SHOP_BUTTON_HEIGHT_SCALE)
        super().__init__("", main_rect_size, 0, center_pos, (0,0,0), (0,0,0), (0,0,0), action)

        self.price_font = pygame.font.Font(None, 100) # font for price text

        self.make_rects()        # create initial rects
        self.change_price(price) # create initial price image
    
    def make_rects(self) -> None:
        """make the different rects for the image"""
        # make back rect
        self.back_rect = self.rect
        self.back_border_rect = self.back_rect.inflate(settings.SHOP_BUTTON_BORDER_WIDTH, 
                                                       settings.SHOP_BUTTON_BORDER_WIDTH)

        # make price rects
        self.price_rect = pygame.Rect(0,0,self.back_rect.width/settings.SHOP_PRICE_WIDTH_SCALE, 
                                      self.back_rect.height)
        self.price_rect.midleft = self.back_rect.midleft
        self.price_border_rect = self.price_rect.inflate(settings.SHOP_BUTTON_BORDER_WIDTH, 
                                                         settings.SHOP_BUTTON_BORDER_WIDTH)
    
    def change_price(self, new_price) -> None:
        """changes the price once it's bought"""
        self.price = new_price # update price in case it changed

        self.price_text = self.price_font.render(str(self.price), True, 'white')
        self.price_text_rect = self.price_text.get_rect(center = self.price_rect.center)
    
    def update(self) -> None:
        """called once per frame"""
        super().update()
        self.make_rects()             # update rects in case the button has grown
        self.change_price(self.price) # update price image in case the button has grown

        # draw shop button to screen
        pygame.draw.rect(self.screen, settings.DARK_BLUE, self.back_border_rect, 
                         border_radius=settings.SHOP_BUTTON_BORDER_RADIUS)
        pygame.draw.rect(self.screen, settings.LIGHT_BLUE, self.back_rect, 
                         border_radius=settings.SHOP_BUTTON_BORDER_RADIUS)
        pygame.draw.rect(self.screen, settings.DARK_BROWN, self.price_border_rect, 
                         border_radius=settings.SHOP_BUTTON_BORDER_RADIUS)
        pygame.draw.rect(self.screen, settings.LIGHT_BROWN, self.price_rect, 
                         border_radius=settings.SHOP_BUTTON_BORDER_RADIUS)
        self.screen.blit(self.price_text, self.price_text_rect)

class SingleBuyShopButton(ShopButton):
    """shop button that can only be bought once"""
    def __init__(self, center_pos: tuple[float, float], price: int, action, check_bought) -> None:
        super().__init__(center_pos, price, action)

        self.check_bought = check_bought # method which checks if the upgrade's already bought
    
    def update(self) -> None:
        """called once per frame"""
        if not self.check_bought():
            super().update() # normal shop button functionality if not bought yet
            return           # next code is for when the upgrade's bought
        
        if self.size.x > self.unhover_size.x: # size hasn't decreased back to unhover
            self.mouse_interact()             # decrease size when mouse leaves button
            self.make_rects()                 # remake rects+price as size may change
            self.change_price(self.price)

        # draw shop button to screen differently if already bought
        pygame.draw.rect(self.screen, settings.DARK_BLUE_HOVER, self.back_border_rect, 
                         border_radius=settings.SHOP_BUTTON_BORDER_RADIUS)
        pygame.draw.rect(self.screen, settings.LIGHT_BLUE_HOVER, self.back_rect, 
                         border_radius=settings.SHOP_BUTTON_BORDER_RADIUS)
        pygame.draw.rect(self.screen, settings.DARK_BROWN_HOVER, self.price_border_rect, 
                         border_radius=settings.SHOP_BUTTON_BORDER_RADIUS)
        pygame.draw.rect(self.screen, settings.LIGHT_BROWN_HOVER, self.price_rect, 
                         border_radius=settings.SHOP_BUTTON_BORDER_RADIUS)
        self.screen.blit(self.price_text, self.price_text_rect)

class Shop(HeadingMenu):
    """shop menu to upgrade player stats"""
    def __init__(self, return_method):
        back_button = Button("back", (settings.WIDTH/10, settings.HEIGHT/15), 25,
            (settings.WIDTH/2, settings.HEIGHT-0.55*settings.HEIGHT/7.2),
            settings.LIGHT_BROWN, settings.LIGHT_BROWN_HOVER, settings.DARK_BROWN, self.exit_shop)
        super().__init__([back_button], "SHOP")

        # upgrade buttons
        explosive_button = SingleBuyShopButton((settings.WIDTH/5, settings.HEIGHT/3), settings.EXPLOSIVE_PRICE, 
                                      settings.GAME.player_stats.buy_explosive, lambda: settings.GAME.player_stats.explosive)
        chaining_button = SingleBuyShopButton((settings.WIDTH-settings.WIDTH/5, settings.HEIGHT/3), settings.CHAINING_PRICE, 
                                     settings.GAME.player_stats.buy_chaining, lambda: settings.GAME.player_stats.chaining)
        self.upgrade_buttons = [explosive_button, chaining_button]

        self.return_method = return_method # method to call to exit shop

        self.gold_font = pygame.font.Font(None, settings.SHOP_GOLD_FONT_SIZE) # font for gold text
    
    def exit_shop(self) -> None:
        """exits the shop"""
        dbms.save_progress()
        self.return_method()
    
    def update(self) -> None:
        """updates and draws the shop"""
        super().update()

        # DRAW GOLD UNDER HEADING
        gold_text = self.gold_font.render(f"{tools.comma_number(settings.GAME.player_stats.gold)} gold", True, 
                                          'white')
        gold_container = gold_text.get_rect().inflate(settings.SHOP_GOLD_PADDING, settings.SHOP_GOLD_PADDING)
        gold_border = gold_container.inflate(settings.HEADING_BORDER_SIZE*2, settings.HEADING_BORDER_SIZE*2)
        gold_container.midtop = self.heading_box.midbottom                 # position rects
        gold_border.center = gold_container.center
        gold_rect = gold_text.get_rect(center=gold_container.center)
        pygame.draw.rect(self.screen, settings.DARK_BROWN, gold_border)    # draw images
        pygame.draw.rect(self.screen, settings.LIGHT_BROWN, gold_container)
        self.screen.blit(gold_text, gold_rect)

        # UPGRADE BUTTONS
        for button in self.upgrade_buttons:
            button.update()