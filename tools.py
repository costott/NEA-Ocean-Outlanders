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

def comma_number(number: float) -> str:
    """returns a number with commas to split thousands, millions etc"""
    number = int(number) # ignore decimals
    reversed_num = str(number)[::-1] # reverse number
    comma_number = ""
    for i, digit in enumerate(reversed_num):
        if i % 3 == 0 and i != 0: # add comma every 3 numbers
            comma_number += ","
        comma_number += digit
    return comma_number[::-1]