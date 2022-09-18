import pygame

from menu import HeadingMenu, Button
import settings
import tools

class EndMenu(HeadingMenu):
    def __init__(self, heading: str) -> None:
        quick_restart_button = Button("quick restart", (settings.WIDTH/5, settings.HEIGHT/7), 50, 
            (settings.WIDTH/2-settings.WIDTH/5, settings.HEIGHT-settings.HEIGHT/7), settings.LIGHT_BLUE, 
            settings.LIGHT_BLUE_HOVER, settings.DARK_BLUE, settings.GAME.main_menu.start_run)
        main_menu_button = Button("main menu", (settings.WIDTH/5, settings.HEIGHT/7), 50, 
            (settings.WIDTH/2+settings.WIDTH/5, settings.HEIGHT-settings.HEIGHT/7), settings.LIGHT_BLUE, 
            settings.LIGHT_BLUE_HOVER, settings.DARK_BLUE, settings.GAME.main_menu.return_main_menu)

        super().__init__([quick_restart_button, main_menu_button], heading) # initialise heading menu

        font = pygame.font.Font(None, 45) # font for stats

        # STATS TEXT
        self.run_time = font.render(tools.hms(settings.current_run.time), True, settings.WHITE)
        self.highscore_time = font.render(f"highscore: {tools.hms(settings.GAME.player_stats.highscore_time)}", 
                                          True, settings.WHITE)

        self.run_wave = font.render(f"wave {settings.current_run.enemy_spawner.current_wave}", True, settings.WHITE)
        self.highscore_wave = font.render(f"highscore: {settings.GAME.player_stats.highscore_wave}", 
                                          True, settings.WHITE)

        self.run_gold = font.render(f"{settings.current_run.gold} gold", True, settings.WHITE)
        self.run_kills = font.render(f"{settings.current_run.kills} kills", True, settings.WHITE)

        # bars for the stats to go in
        self.large_bar = pygame.Rect(0,0,settings.WIDTH/2,settings.HEIGHT/12)
        self.large_bar.centerx = settings.WIDTH/2
        self.small_bar = pygame.Rect(0,0,self.large_bar.width/2, self.large_bar.height)
        self.small_bar.centerx = settings.WIDTH/2

    def update(self) -> None:
        """called once per frame"""
        super().update() # update heading menu

        self.draw_large_bar(1.5*(self.large_bar.height+settings.END_MENU_BAR_GAP), self.run_time, self.highscore_time)   
        self.draw_large_bar(0.5*(self.large_bar.height+settings.END_MENU_BAR_GAP), self.run_wave, self.highscore_wave)    
        self.draw_small_bar(0.5*(self.large_bar.height+settings.END_MENU_BAR_GAP), self.run_gold) 
        self.draw_small_bar(1.5*(self.large_bar.height+settings.END_MENU_BAR_GAP), self.run_kills) 
    
    def draw_large_bar(self, y_offset: float, run_stat_text: pygame.Surface, highscore_text: pygame.Surface) -> None:
        """draw large bar for given stat to screen"""
        # get rects
        run_stat_rect = run_stat_text.get_rect()
        highscore_rect = highscore_text.get_rect()

        # position and draw bar
        self.large_bar.centery = settings.HEIGHT/2 - y_offset
        pygame.draw.rect(self.screen, settings.LIGHT_BROWN, self.large_bar, border_radius=settings.END_MENU_BAR_RADIUS)
        pygame.draw.rect(self.screen, settings.DARK_BROWN, self.large_bar.inflate(settings.END_MENU_BAR_BORDER_WIDTH, 
            settings.END_MENU_BAR_BORDER_WIDTH), width=settings.END_MENU_BAR_BORDER_WIDTH, border_radius=settings.END_MENU_BAR_RADIUS)
        
        # position and draw stat+highscore
        run_stat_rect.midleft = self.large_bar.midleft
        run_stat_rect.left += settings.END_MENU_PADDING
        self.screen.blit(run_stat_text, run_stat_rect)
        highscore_rect.midleft = self.large_bar.center
        self.screen.blit(highscore_text, highscore_rect)
    
    def draw_small_bar(self, y_offset: float, run_stat_text: pygame.Surface) -> None:
        """draw small bar for given stat to screen"""
        # get rect
        run_stat_rect = run_stat_text.get_rect()

        # position and draw bar
        self.small_bar.centery = settings.HEIGHT/2 + y_offset
        pygame.draw.rect(self.screen, settings.LIGHT_BROWN, self.small_bar, border_radius=settings.END_MENU_BAR_RADIUS)
        pygame.draw.rect(self.screen, settings.DARK_BROWN, self.small_bar.inflate(settings.END_MENU_BAR_BORDER_WIDTH, 
            settings.END_MENU_BAR_BORDER_WIDTH), width=settings.END_MENU_BAR_BORDER_WIDTH, border_radius=settings.END_MENU_BAR_RADIUS)
        
        # position and draw stat
        run_stat_rect.center = self.small_bar.center
        self.screen.blit(run_stat_text, run_stat_rect)