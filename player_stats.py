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
    
    def stat_upgrade_info(self, name: str, stat: float, percent_increase: float, unit_price: float) -> tuple[str, float, float, int]:
        """returns name of stat current stat, how much to upgrade, cost of upgrade"""
        return (name, f"{float(stat):.2f}", f"{stat*percent_increase:.2f}", int(stat*percent_increase*unit_price))
    
    def hp_upgrade(self) -> tuple[str, float, float, int]:
        """returns name, stat, increase, price of hp upgrade"""
        return self.stat_upgrade_info("HP", self.hp, settings.HP_PERCENT_INCREASE, settings.HP_UNIT_PRICE)

    def buy_hp(self) -> None:
        """buys more hp"""
        price = int(self.hp*settings.HP_PERCENT_INCREASE*settings.HP_UNIT_PRICE)
        if self.gold < price: return

        self.hp += self.hp*settings.HP_PERCENT_INCREASE
        self.gold -= price

    def dmg_upgrade(self) -> tuple[str, float, float, int]:
        """returns name, stat, increase, price of dmg upgrade"""
        return self.stat_upgrade_info("DMG", self.damage, settings.DMG_PERCENT_INCREASE, settings.DMG_UNIT_PRICE)
        
    def buy_dmg(self) -> None:
        """buys more damage"""
        price = int(self.damage*settings.DMG_PERCENT_INCREASE*settings.DMG_UNIT_PRICE)
        if self.gold < price: return

        self.damage += self.damage*settings.DMG_PERCENT_INCREASE
        self.gold -= price

    def spd_upgrade(self) -> tuple[str, float, float, int]:
        """returns name, stat, increase, price of spd upgrade"""
        return self.stat_upgrade_info("SPD", self.speed, settings.SPEED_PERCENT_INCREASE, settings.SPEED_UNIT_PRICE)
    
    def buy_spd(self) -> None:
        """buys more spd"""
        price = int(self.speed*settings.SPEED_PERCENT_INCREASE*settings.SPEED_UNIT_PRICE)
        if self.gold < price: return

        self.speed += self.speed*settings.SPEED_PERCENT_INCREASE
        self.gold -= price