import sqlite3
import hashlib
import os

from player_stats import PlayerStats
import settings

class DBMS:
    """database management system"""
    def __init__(self):
        # make database if it doesn't exist
        if not os.path.exists(settings.DATABASE_LOCATION):
            self.open_connection() # create database
            self.close_connection()

        self.create_tables()
    
    def open_connection(self) -> None:
        """opens database connection to start transaction"""
        self.connect = sqlite3.connect("ocean_outlanders.db")
        self.cursor = self.connect.cursor()

    def close_connection(self) -> None:
        """closes database connection to complete transaction"""
        self.cursor.close()
        self.connect.close()
    
    def create_tables(self) -> None:
        """creates User and Upgrade tables if they aren't already created"""
        self.open_connection()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS User (username TEXT, pass_hash TEXT, gold REAL, 
        high_time REAL, high_wave INT)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Upgrade (upgrade_id TEXT, username TEXT, hp REAL, 
        dmg REAL, speed REAL, explosive INT, chaining INT)""")
        self.close_connection()
    
    def user_exists(self, username: str) -> bool:
        """checks if a user already exists in the database"""
        # user doesn't exist if database doesn't
        if not os.path.exists(settings.DATABASE_LOCATION): return False

        self.open_connection()
        self.cursor.execute("SELECT username FROM User WHERE username = ?", (username,)) # get user with same username
        user_in_db = len(self.cursor.fetchall()) > 0
        self.close_connection()
        return user_in_db # returns if a user exists
    
    def sign_up(self, username: str, password_unhashed: str) -> None:
        """creates new user account"""
        if self.user_exists(username): return # make sure user doesn't exist

        password_hashed = hashlib.sha256(password_unhashed.encode()).hexdigest() # hash password
        self.open_connection()
        self.cursor.execute("""INSERT INTO User (username, pass_hash, gold, high_time, high_wave) VALUES 
        (?, ?, 0, 0, 0)""", (username, password_hashed)) # set base stats in User table
        self.cursor.execute("""INSERT INTO Upgrade (upgrade_id, username, hp, dmg, speed, explosive, chaining) 
        VALUES (?, ?, ?, ?, ?, 0, 0)""", (f"{username}0", username, settings.PB_BASE_HP, settings.PB_BASE_DAMAGE, 
        settings.PB_BASE_SPEED))                         # set base stats in Upgrade table
        self.connect.commit()
        self.close_connection()

        self.load_progress(username)
    
    def sign_in(self, username: str, password_unhashed: str) -> bool:
        """checks if user credentials are valid"""
        if not self.user_exists(username): return False # make sure user exists

        password_hashed = hashlib.sha256(password_unhashed.encode()).hexdigest() # hash password

        self.open_connection()
        self.cursor.execute("SELECT pass_hash FROM User WHERE username = ?", (username,))
        password_match = password_hashed == self.cursor.fetchall()[0][0] # check if passwords match
        self.close_connection()
        return password_match

    def load_progress(self, username: str) -> None:
        """puts player stats from database into new PlayerStats object"""
        self.open_connection()
        self.cursor.execute("SELECT gold, high_time, high_wave FROM User WHERE username = ?", (username,))
        gold, high_time, high_wave = self.cursor.fetchall()[0]
        self.cursor.execute("SELECT hp, dmg, speed, explosive, chaining FROM Upgrade WHERE username = ?", (username,))
        hp, dmg, speed, explosive, chaining = self.cursor.fetchall()[0]
        self.close_connection()

        settings.GAME.player_stats = PlayerStats(username, gold, hp, dmg, speed, high_time, high_wave, explosive, chaining)
    
    def save_progress(self) -> None:
        """puts player stats from PlayerStats object into database"""
        player_stats = settings.GAME.player_stats

        self.open_connection()
        self.cursor.execute("UPDATE User SET gold = ?, high_time = ?, high_wave = ? WHERE username = ?", 
            (player_stats.gold, player_stats.highscore_time, player_stats.highscore_wave, player_stats.username))
        self.cursor.execute("""UPDATE Upgrade SET hp = ?, dmg = ?, speed = ?, explosive = ?, chaining = ? 
        WHERE username = ?""", (player_stats.hp, player_stats.damage, player_stats.speed, player_stats.explosive, 
                                player_stats.chaining, player_stats.username))
        self.connect.commit()
        self.close_connection()

dbms = DBMS()