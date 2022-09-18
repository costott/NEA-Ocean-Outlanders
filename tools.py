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

def hms(time: float) -> str:
    """converts time into hours:minutes:seconds"""
    time = int(time)
    time_hours = time // 3600
    time_minutes = (time - time_hours*3600) // 60
    time_seconds = round(time - (time_hours*3600+time_minutes*60))
    return f"{time_hours:2}:{time_minutes:2}:{time_seconds:2}".replace(" ", "0")