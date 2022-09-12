import pygame

import settings
import tools

class HUD:
    """HUD on screen during run"""
    def __init__(self):
        self.screen = pygame.display.get_surface() # game screen for easy access
    
    def draw(self) -> None:
        """draw the HUD"""
        # draw main hud elements

        if settings.current_run.player_boat.state == "steering":
            self.steering_hud()
    
    def steering_hud(self) -> None:
        """draws steering bar onto the screen"""
        # create main bar
        bar = pygame.Rect(0,0,settings.WIDTH*0.6,settings.HEIGHT*0.04)
        bar.center = (settings.WIDTH/2, settings.HEIGHT-3*bar.height)
        inner_bar = tools.scaled_rect(bar, 0.95, 0.7)

        # create square to represent current angle velocity
        current_square = pygame.Rect(0,bar.top,bar.height,bar.height)
        current_square.centerx = bar.centerx - (bar.width/2-current_square.width/2)*(
                                                            settings.current_run.player_boat.angle_velocity/
                                                            settings.BOAT_MAX_ANGLE_SPEED)
        inner_current_square = tools.scaled_rect(current_square, 0.7, 0.7)

        # create square in middle of bar
        middle_square = current_square.copy()
        middle_square.center = bar.center
        inner_middle_square = tools.scaled_rect(middle_square, 0.7, 0.7)
        
        # draw all elements
        pygame.draw.rect(self.screen, settings.LIGHT_BROWN, bar, border_radius=5)
        pygame.draw.rect(self.screen, settings.BROWN, inner_bar, border_radius=5)

        pygame.draw.rect(self.screen, settings.BROWN, middle_square, border_radius=5)
        pygame.draw.rect(self.screen, settings.WHITE, inner_middle_square, border_radius=5)
        
        pygame.draw.rect(self.screen, settings.DARK_BLUE, current_square, border_radius=5)
        pygame.draw.rect(self.screen, settings.LIGHT_BLUE, inner_current_square, border_radius=5)