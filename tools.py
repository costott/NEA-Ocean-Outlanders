import pygame

import settings

def get_fps() -> float:
    """returns the current fps of the game"""
    fps = settings.GAME.clock.get_fps()
    return fps if fps != 0 else 999999