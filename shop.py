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

        self.price_font = pygame.font.Font(None, 60) # font for price text
        self.coin_image = pygame.image.load("assets/coin.png").convert_alpha()
        self.coin_image = pygame.transform.rotozoom(self.coin_image, 0, 0.5)
        self.coin_rect = self.coin_image.get_rect()

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

        # get text and rect of price
        self.price_text = self.price_font.render(f"{self.price}", True, 'white')
        self.price_text_rect = self.price_text.get_rect()

        # put the price text in the correct centre of the box
        combined_rect = pygame.Rect(0,0,self.price_text_rect.width+self.coin_rect.width,
                                    self.coin_rect.height)
        combined_rect.center = self.price_rect.center
        self.price_text_rect.midleft = combined_rect.midleft
        self.coin_rect.midright = combined_rect.midright
        self.coin_rect.y -= 3
        self.coin_rect.x += 5
    
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
        self.screen.blit(self.coin_image, self.coin_rect)

class SingleBuyShopButton(ShopButton):
    """shop button that can only be bought once"""
    def __init__(self, center_pos: tuple[float, float], image: pygame.Surface, price: int, action, check_bought):
        super().__init__(center_pos, price, action)

        self.image = image
        self.image_rect = self.image.get_rect(center=((self.back_rect.right+self.price_rect.right)/2, 
                                              self.back_rect.centery))

        self.check_bought = check_bought # method which checks if the upgrade's already bought
    
    def update(self) -> None:
        """called once per frame"""
        if not self.check_bought():
            super().update() # normal shop button functionality if not bought yet
            self.image_rect = self.image.get_rect(center=((self.back_rect.right+self.price_rect.right)/2, 
                                              self.back_rect.centery))
            self.screen.blit(self.image, self.image_rect)
            return           # next code is for when the upgrade's bought
        
        if self.size.x > self.unhover_size.x: # size hasn't decreased back to unhover
            self.mouse_interact()             # decrease size when mouse leaves button
            self.make_rects()                 # remake rects+price as size may change
            self.image_rect = self.image.get_rect(center=((self.back_rect.right+self.price_rect.right)/2, 
                                              self.back_rect.centery))
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
        self.screen.blit(self.image, self.image_rect)

class StatShopButton(ShopButton):
    """shop button for stats"""
    def __init__(self, center_pos: tuple[float, float], upgrade_info, buy_action, stat_colour: pygame.Color, 
                 stat_border_colour: pygame.Color):
        self.upgrade_info = upgrade_info # method which returns information about the upgrade
        self.buy_action = buy_action     # method which buys the upgrade
        super().__init__(center_pos, self.upgrade_info()[3], self.upgrade_action) # initialise StatButton

        self.stat_colour = stat_colour               # colour of bar to show current stat
        self.stat_border_colour = stat_border_colour # colour of border of bar above

        self.current_stat_font = pygame.font.Font(None, 80) # font for the stat+upgrade on the buton
        self.current_stat = self.upgrade_info()[1]          # gets the current stat amount
    
    def upgrade_action(self) -> None:
        """what happens when the button's pressed"""
        self.buy_action()                          # buy the upgrade
        self.current_stat = self.upgrade_info()[1] # get the new stat number
        self.price = self.upgrade_info()[3]        # get the new price

    def make_stat(self) -> None:
        """makes the stat bar above button"""
        self.stat_rect = self.back_rect.copy()  # rect of bar to show current stat
        self.stat_rect.midbottom = self.back_rect.center
        self.stat_border_rect = self.stat_rect.inflate(settings.SHOP_BUTTON_BORDER_WIDTH, 
                                                       settings.SHOP_BUTTON_BORDER_WIDTH)
        # text to show current stat
        self.stat_text = self.current_stat_font.render(str(self.current_stat), True, "white") 
        self.stat_text_rect = self.stat_text.get_rect(center = (self.stat_rect.centerx, 
                                                                self.stat_rect.top+self.stat_rect.height/4))
    
    def make_upgrade(self) -> None:
        """makes the text to show how much the stat's upgraded"""
        # middle of non-price part of the button
        middle = (self.price_rect.right + (self.back_rect.width-self.price_rect.width)/2, self.back_rect.centery)

        # displays how much the upgrade will do
        self.stat_add = self.current_stat_font.render(f"+{self.upgrade_info()[2]}", True, "white")
        self.stat_add_rect = self.stat_add.get_rect(midbottom = middle)
        self.stat_name = self.current_stat_font.render(str(self.upgrade_info()[0]), True, "white")
        self.stat_name_rect = self.stat_name.get_rect(midtop = middle)

    def update(self) -> None:
        """called once per frame"""
        self.make_stat()    # remake the bar in case the button changes size
        self.make_upgrade() # remake the upgrade information in case the button changes size
        
        # draw stat bar to screen
        pygame.draw.rect(self.screen, self.stat_border_colour, self.stat_border_rect, border_radius=settings.SHOP_BUTTON_BORDER_RADIUS)
        pygame.draw.rect(self.screen, self.stat_colour, self.stat_rect, border_radius=settings.SHOP_BUTTON_BORDER_RADIUS)
        self.screen.blit(self.stat_text, self.stat_text_rect)

        super().update() # make rest of shop button

        # draw text to show how much the stat will be upgraded
        self.screen.blit(self.stat_add, self.stat_add_rect)
        self.screen.blit(self.stat_name, self.stat_name_rect)

class Shop(HeadingMenu):
    """shop menu to upgrade player stats"""
    def __init__(self, return_method):
        back_button = Button("back", (settings.WIDTH/10, settings.HEIGHT/15), 25,
            (settings.WIDTH/2, settings.HEIGHT-0.55*settings.HEIGHT/7.2),
            settings.LIGHT_BROWN, settings.LIGHT_BROWN_HOVER, settings.DARK_BROWN, self.exit_shop)
        super().__init__([back_button], "SHOP")

        # upgrade buttons
        explosive_image = tools.scaled_image("assets/exploded_cannonball.png", settings.SHOP_CANNONBALL_SCALE)
        chaining_image = tools.scaled_image("assets/lightning_cannonball.png", settings.SHOP_CANNONBALL_SCALE)
        explosive_button = SingleBuyShopButton((settings.WIDTH/6, settings.HEIGHT/3.6), explosive_image, 
                            settings.EXPLOSIVE_PRICE, settings.GAME.player_stats.buy_explosive, 
                            lambda: settings.GAME.player_stats.explosive)
        chaining_button = SingleBuyShopButton((settings.WIDTH/1.2, settings.HEIGHT/3.6), chaining_image, 
                            settings.CHAINING_PRICE, settings.GAME.player_stats.buy_chaining, 
                            lambda: settings.GAME.player_stats.chaining)
        hp_button = StatShopButton((settings.WIDTH/6, settings.HEIGHT/1.44), settings.GAME.player_stats.hp_upgrade, 
                            settings.GAME.player_stats.buy_hp, settings.RED, settings.DARK_RED)
        dmg_button  = StatShopButton((settings.WIDTH/2, settings.HEIGHT/1.44), settings.GAME.player_stats.dmg_upgrade,
                            settings.GAME.player_stats.buy_dmg, settings.YELLOW, settings.DARK_YELLOW)
        spd_button = StatShopButton((settings.WIDTH/1.2, settings.HEIGHT/1.44), settings.GAME.player_stats.spd_upgrade,
                            settings.GAME.player_stats.buy_spd, settings.GREEN, settings.DARK_GREEN)
        self.upgrade_buttons = [explosive_button, chaining_button, hp_button, dmg_button, spd_button]

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
        # box for gold to be on
        gold_container = gold_text.get_rect().inflate(settings.SHOP_GOLD_PADDING, settings.SHOP_GOLD_PADDING)
        # border around box
        gold_border = gold_container.inflate(settings.HEADING_BORDER_SIZE*2, settings.HEADING_BORDER_SIZE*2)

        # position rects
        gold_container.midtop = self.heading_box.midbottom                 
        gold_border.center = gold_container.center
        gold_rect = gold_text.get_rect(center=gold_container.center)

        # draw images
        pygame.draw.rect(self.screen, settings.DARK_BROWN, gold_border)
        pygame.draw.rect(self.screen, settings.LIGHT_BROWN, gold_container)
        self.screen.blit(gold_text, gold_rect)

        # UPGRADE BUTTONS
        for button in self.upgrade_buttons:
            button.update()