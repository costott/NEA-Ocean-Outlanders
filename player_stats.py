class PlayerStats:
    """holds the stats for the player boat"""
    def __init__(self, username: str, gold: float, hp: float, damage: float, speed: float, high_time: float, 
                 high_wave: int, explosive: int, chaining: int):
        self.username = username
        self.gold = gold

        self.hp = hp
        self.damage = damage
        self.speed = speed

        self.highscore_time = high_time
        self.highscore_wave = high_wave

        self.explosive = explosive
        self.chaining = chaining