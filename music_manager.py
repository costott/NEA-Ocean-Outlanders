import pygame

class MusicManager:
    """manages the music being played in the game"""
    def __init__(self):
        self.state = None # current music being played
    
    def menu_music(self) -> None:
        """start the menu music"""
        if self.state == "menu": return # don't start playing the menu music if it's already playing

        # load and play menu music
        pygame.mixer.music.load("sound/menu_music.mp3")
        pygame.mixer.music.play(-1)
        self.state = "menu"
    
    def run_music(self) -> None:
        """start the run music"""
        if self.state == "run": return # don't start playing the run music if it's already playing

        # load and play run music
        pygame.mixer.music.load("sound/run_music.mp3")
        pygame.mixer.music.play(-1)
        self.state = "run"

music_manager = MusicManager()