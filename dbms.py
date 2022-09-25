import sqlite3
import hashlib
import os

from player_stats import PlayerStats
import settings
import tools

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
    
    def get_top_3_wave(self) -> list[tuple[str, int]]:
        """returns the usernames and top waves of the top 3 players"""
        self.open_connection()
        self.cursor.execute("SELECT username, high_wave FROM User ORDER BY high_wave DESC LIMIT 3")
        players = self.cursor.fetchall()
        self.close_connection()
        return players
    
    def get_neighbour_wave(self) -> list[list[int, str, int]]:
        """returns the places, usernames and top waves of the current user and their neighbours"""
        # get all the players and their highest wave
        self.open_connection()
        self.cursor.execute("SELECT username, high_wave FROM User ORDER BY high_wave DESC")
        all_players = self.cursor.fetchall()
        self.close_connection()

        # linear search to find player
        player_i = None
        for i, player in enumerate(all_players): 
            if player[0] == settings.GAME.player_stats.username: 
                player_i = i
                break
        
        # get the players
        above_player, current_player, below_player = None, None, None
        if player_i > 0:                  # player isn't the top of the leaderboard (index 0)
            above_player = [player_i] + list(all_players[player_i-1])
        current_player = [player_i+1] + list(all_players[player_i])
        if player_i < len(all_players)-1: # player isn't the bottom of the leaderboard
            below_player = [player_i+2] + list(all_players[player_i+1])
        
        return [above_player, current_player, below_player]
    
    def get_top_3_time(self) -> list[tuple[str, str]]:
        """returns the usernames and top times of the top 3 players"""
        self.open_connection()
        self.cursor.execute("SELECT username, high_time FROM User ORDER BY high_time DESC LIMIT 3")
        players = self.cursor.fetchall()
        self.close_connection()
        # convert player's time to h:m:s
        return [(player[0], tools.hms(player[1])) for player in players]

    def get_neighbour_time(self) -> list[list[int, str, str]]:
        """returns the places, usernames and top times of the current user and their neighbours"""
        # get all the players and their highest wave
        self.open_connection()
        self.cursor.execute("SELECT username, high_time FROM User ORDER BY high_time DESC")
        all_players = self.cursor.fetchall()
        self.close_connection()

        # linear search to find player
        player_i = None
        for i, player in enumerate(all_players): 
            if player[0] == settings.GAME.player_stats.username: 
                player_i = i
                break
        
        # get the players
        above_player, current_player, below_player = None, None, None
        if player_i > 0:                  # player isn't the top of the leaderboard (index 0)
            above_player = [player_i, all_players[player_i-1][0], tools.hms(all_players[player_i-1][1])]
        current_player = [player_i+1, all_players[player_i][0], tools.hms(all_players[player_i][1])]
        if player_i < len(all_players)-1: # player isn't the bottom of the leaderboard
            below_player = [player_i+2, all_players[player_i+1][0], tools.hms(all_players[player_i+1][1])]
        
        return [above_player, current_player, below_player]   

dbms = DBMS()