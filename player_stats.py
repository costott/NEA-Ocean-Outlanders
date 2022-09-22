import settings

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
    
    def buy_explosive(self) -> None:
        """buy the explosive cannonball"""
        # player has enough gold and doesn't have it yet
        if self.gold < settings.EXPLOSIVE_PRICE or self.explosive:
            return
        
        self.gold -= settings.EXPLOSIVE_PRICE # spend gold
        self.explosive = True                 # unlock cannonball
    
    def buy_chaining(self) -> None:
        """buy the chaining cannonball"""
        # player has enough gold and doesn't have it yet
        if self.gold < settings.CHAINING_PRICE or self.chaining:
            return
        
        self.gold -= settings.CHAINING_PRICE # spend gold
        self.chaining = True                 # unlock cannonball