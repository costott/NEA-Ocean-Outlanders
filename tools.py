import pygame
import math

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

def scaled_image(path: str, scale: float) -> pygame.Surface:
    """returns a scaled image of the provided image"""
    image = pygame.image.load(path).convert_alpha()   # get image
    return pygame.transform.rotozoom(image, 0, scale) # scale + return image

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

def draw_filled_arc(surface: pygame.Surface, colour: pygame.Color, center_position: tuple[float, float], radius: float,
                    start_angle: float, stop_angle: float, width: float = 1) -> None:
    """draw filled arc between 2 angle points
    \n0 = north, angle goes anticlockwise"""
    angle_diff = stop_angle - start_angle # difference between angles
    # MAKE SURE 0 < ANGLE_DIFF < 360
    while angle_diff < 0:
        angle_diff += 360
    while angle_diff > 360: 
        angle_diff -= 360
    if angle_diff < 1: return # have to have at least 2 angles to plot (0 and 1)

    angle_step = 0.5 # angle between adjacent points
    points, inner_points = [], []
    for step in range(int(angle_diff/angle_step)):
        angle = start_angle + step*angle_step                    # angle of current point
        angle_vector = pygame.math.Vector2(0, -1).rotate(-angle) # unit vector for current angle

        points.append(center_position + radius*angle_vector)
        inner_points.append(center_position + (radius-width)*angle_vector)
    pygame.draw.polygon(surface, colour, points + inner_points[::-1])