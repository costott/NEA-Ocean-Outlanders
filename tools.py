import pygame

import settings

def get_fps() -> float:
    """returns the current fps of the game"""
    fps = settings.GAME.clock.get_fps()
    return fps if fps != 0 else 999999

def scaled_rect(rect: pygame.Rect, width_scale: float, height_scale: float) -> pygame.Rect:
    """returns a scaled rect proportional to the given one"""
    scaled = rect.copy()
    scaled.width *= width_scale
    scaled.height *= height_scale
    scaled.center = rect.center
    return scaled