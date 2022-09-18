class PlayerStats:
    """holds the stats for the player boat"""
    def __init__(self, hp: float, damage: float, speed: float):
        self.hp = hp
        self.damage = damage
        self.speed = speed

        self.highscore_time = 0
        self.highscore_wave = 0