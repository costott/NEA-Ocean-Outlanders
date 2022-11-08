import pygame

from map_piece import MapPiece
import settings
import tools

class Port(MapPiece):
    """port on the map that allows the player to end the run"""
    def __init__(self, groups: list[pygame.sprite.Group], topleft: tuple):
        super().__init__(groups, topleft, pygame.image.load(settings.PORT_IMAGE).convert_alpha())

        self.centre = pygame.math.Vector2(self.rect.center) # vector of centre of port

        self.player_in_range = False # stores whether the player's in range of the port

        self.ring_radius = settings.PORT_RING_MIN_RAD # current radius of ring for HUD
        self.increasing = True                        # current direction of radius change
    
    def update(self) -> None:
        """called once per frame"""
        self.change_ring_radius()

        # checks if the player is in range
        self.player_in_range = settings.current_run.player_boat.pos.distance_to(self.centre) <= settings.PORT_RADIUS
        if self.player_in_range: self.player_input()

    def player_input(self) -> None:
        """completes the run if E is pressed"""
        if pygame.key.get_pressed()[pygame.K_e]: 
            settings.GAME.main_menu.complete_run()
        
    def change_ring_radius(self) -> None:
        """changes radius of ring around dock for HUD"""
        if self.increasing: # increase ring radius
            self.ring_radius += settings.PORT_RING_SPEED * 1/tools.get_fps()

            if self.ring_radius >= settings.PORT_RING_MAX_RAD: # at maximum - start decreasing
                self.ring_radius = settings.PORT_RING_MAX_RAD
                self.increasing = False
        elif not self.increasing: # decrease ring radius
            self.ring_radius -= settings.PORT_RING_SPEED * 1/tools.get_fps()

            if self.ring_radius <= settings.PORT_RING_MIN_RAD: # at minimum - start increasing
                self.ring_radius = settings.PORT_RING_MIN_RAD
                self.increasing = True