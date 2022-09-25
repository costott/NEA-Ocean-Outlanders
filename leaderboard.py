import pygame

from menu import HeadingMenu, Button
from dbms import dbms
import settings
import tools

class LeaderboardPlace:
    """individual placement/player on the leaderboard"""
    def __init__(self, number: int, username: str, value: str, center_pos: tuple[float, float]):
        self.screen = pygame.display.get_surface() # screen for easy access

        # make all the bars for the text to go into
        self.main_bar = pygame.Rect(0,0,settings.WIDTH/settings.LEADERBOARD_PLACE_WIDTH_SCALE,
                                    settings.HEIGHT/settings.LEADERBOARD_PLACE_HEIGHT_SCALE)
        self.main_bar.center = center_pos
        self.number_bar = pygame.Rect(0,0,self.main_bar.width/settings.LEADERBORD_PLACE_NUMBER_WIDTH_SCALE,
                                      self.main_bar.height) # bar for the number in leaderboard
        self.number_bar.midleft = self.main_bar.midleft # put left of number bar at left of main bar
        self.value_bar = pygame.Rect(0,0,self.main_bar.width/settings.LEADERBOARD_PLACE_VALUE_WIDTH_SCALE,
                                     self.main_bar.height)  # bar for highscore of player
        self.value_bar.midright = self.main_bar.midright # put right of highscore at right of main bar

        # change colours if the place is for the current player
        if username == settings.GAME.player_stats.username:
            self.main_colour = "white"
            self.username_colour = settings.DARK_BLUE
        else:
            self.main_colour = settings.LIGHT_BLUE
            self.username_colour = "white"

        # make all the text
        place_font = pygame.font.Font(None, 45)
        self.number_text = place_font.render(str(number), True, "white") # number of place on leaderboard
        # put number of place in centre of the number bar
        self.number_text_rect = self.number_text.get_rect(center=self.number_bar.center)
        self.username_text = place_font.render(username, True, self.username_colour) # username of player
        # put username in the middle of the number and highscore bars (centre of visible part of the main bar)
        self.username_text_rect = self.username_text.get_rect(center=((self.number_bar.right+self.value_bar.left)/2,
                                                                       self.main_bar.centery))
        self.value_text = place_font.render(value, True, "white") # value/stat of their highscore
        # put highscore in centre of the value bar
        self.value_text_rect = self.value_text.get_rect(center=self.value_bar.center)

        # colour the place bar for the top 3 (gold, silver, bronze)
        if number == 1: self.place_colour = settings.GOLD
        elif number == 2: self.place_colour = settings.SILVER
        elif number == 3: self.place_colour = settings.BRONZE
        else: self.place_colour = settings.LIGHT_BROWN
    
    def update(self) -> None:
        """called once per frame"""
        # draw bars
        pygame.draw.rect(self.screen, self.main_colour, self.main_bar, 
                         border_radius=settings.LEADERBOARD_PLACE_RADIUS) # main bar
        pygame.draw.rect(self.screen, settings.DARK_BLUE, self.main_bar, width=settings.HEADING_BORDER_SIZE, 
                         border_radius=settings.LEADERBOARD_PLACE_RADIUS) # main bar border
        pygame.draw.rect(self.screen, self.place_colour, self.number_bar, 
                         border_radius=settings.LEADERBOARD_PLACE_RADIUS) # leaderboard position bar
        pygame.draw.rect(self.screen, settings.DARK_BROWN, self.number_bar, width=settings.HEADING_BORDER_SIZE, 
                         border_radius=settings.LEADERBOARD_PLACE_RADIUS) # leaderboard position bar border
        pygame.draw.rect(self.screen, settings.LIGHT_BLUE, self.value_bar, 
                         border_radius=settings.LEADERBOARD_PLACE_RADIUS) # value bar
        pygame.draw.rect(self.screen, "white", self.value_bar, width=settings.HEADING_BORDER_SIZE, 
                         border_radius=settings.LEADERBOARD_PLACE_RADIUS) # value bar border

        # draw text
        self.screen.blit(self.number_text, self.number_text_rect)
        self.screen.blit(self.username_text, self.username_text_rect)
        self.screen.blit(self.value_text, self.value_text_rect)

class Leaderboard(HeadingMenu):
    """leaderboard menu to compare player performance"""
    def __init__(self, return_method):
        back_button = Button("back", (settings.WIDTH/10, settings.HEIGHT/15), 25,
            (settings.WIDTH/2, settings.HEIGHT-0.55*settings.HEIGHT/7.2),
            settings.LIGHT_BROWN, settings.LIGHT_BROWN_HOVER, settings.DARK_BROWN, return_method)
        super().__init__([back_button], "LEADERBOARD")

        leaderboard_heading_font = pygame.font.Font(None, 60) # font for the leaderboard headings

        # box+text for the top wave
        self.top_wave_box = pygame.Rect(settings.LEADERBORD_HEADING_PADDING,
                             settings.BAR_HEIGHT+settings.LEADERBORD_HEADING_PADDING,
                             (self.heading_box.left-2*settings.LEADERBORD_HEADING_PADDING),
                             (self.heading_box.bottom-settings.BAR_HEIGHT-2*settings.LEADERBORD_HEADING_PADDING))
        self.top_wave_text = leaderboard_heading_font.render("TOP WAVE", True, "white")
        self.top_wave_text_rect = self.top_wave_text.get_rect(center=self.top_wave_box.center)

        # box+text for the top time
        self.top_time_box = self.top_wave_box.copy()
        self.top_time_box.left = self.heading_box.right + settings.LEADERBORD_HEADING_PADDING
        self.top_time_text = leaderboard_heading_font.render("TOP TIME", True, "white")
        self.top_time_text_rect = self.top_time_text.get_rect(center=self.top_time_box.center)

        self.make_leaderboard_places()
    
    def make_leaderboard_places(self) -> None:
        """make the wave and time leaderboards"""
        self.leaderboard_places = [] # holds all leaderboard placed to be displayed
        # wave leaderboard
        self.get_leaderboard(dbms.get_top_3_wave(), dbms.get_neighbour_wave(), settings.WAVE_PLACE_CENTERX_SCALE)
        # time leaderboard
        self.get_leaderboard(dbms.get_top_3_time(), dbms.get_neighbour_time(), settings.TIME_PLACE_CENTERX_SCALE)
    
    def get_leaderboard(self, top_3: list[tuple], neighbours: list[list], x_scale: float) -> None:
        """gets all the places to be displayed on the given leaderboard"""
        x = settings.WIDTH/x_scale # center x values for all leaderboard places

        # make leaderboard places for the top 3
        for i, place in enumerate(top_3):
            y = settings.HEIGHT/settings.LEADERBOARD_PLACE_START_CENTERY_SCALE + i*(settings.HEIGHT/
                    settings.LEADBOARD_PLACE_GAP_CENTERY_SCALE) # get the place to the correct position
            self.leaderboard_places.append(LeaderboardPlace(i+1, place[0], str(place[1]), (x,y)))
        # fill in the gaps if there's not 3 players for the top 3
        for i in range(3-len(top_3)):
            y = settings.HEIGHT/settings.LEADERBOARD_PLACE_START_CENTERY_SCALE + (len(top_3)+i)*(settings.HEIGHT/
                    settings.LEADBOARD_PLACE_GAP_CENTERY_SCALE)
            self.leaderboard_places.append(LeaderboardPlace(len(top_3)+i+1, "---", "---", (x,y)))
        
        # make the places for the 3 'neighbour' places
        for i, place in enumerate(neighbours):
            y = settings.HEIGHT/settings.LEADERBOARD_PLACE_START_CENTERY_SCALE + (
                settings.HEIGHT/settings.LEADERBOARD_GROUP_GAP_SCALE) + (
                i+3)*(settings.HEIGHT/settings.LEADBOARD_PLACE_GAP_CENTERY_SCALE) # position place
            if place != None:
                self.leaderboard_places.append(LeaderboardPlace(place[0], place[1], str(place[2]), (x,y)))
            else: # no player in leaderboard for this position
                self.leaderboard_places.append(LeaderboardPlace("-", "---", "---", (x,y)))

    def update(self) -> None:
        """called once per frame"""
        super().update() # update heading menu

        # draw top wave heading
        pygame.draw.rect(self.screen, settings.LIGHT_BROWN, self.top_wave_box, 
                         border_radius=settings.LEADERBOARD_HEADING_RADIUS)
        pygame.draw.rect(self.screen, settings.DARK_BROWN, self.top_wave_box, 
                         width=settings.HEADING_BORDER_SIZE, border_radius=settings.LEADERBOARD_HEADING_RADIUS)
        self.screen.blit(self.top_wave_text, self.top_wave_text_rect)

        # draw top time heading
        pygame.draw.rect(self.screen, settings.LIGHT_BROWN, self.top_time_box, 
                         border_radius=settings.LEADERBOARD_HEADING_RADIUS)
        pygame.draw.rect(self.screen, settings.DARK_BROWN, self.top_time_box, 
                         width=settings.HEADING_BORDER_SIZE, border_radius=settings.LEADERBOARD_HEADING_RADIUS)
        self.screen.blit(self.top_time_text, self.top_time_text_rect)

        # draw line between the 2 parts of the leaderboard
        y = settings.HEIGHT/settings.LEADERBOARD_PLACE_START_CENTERY_SCALE + (
            settings.HEIGHT/settings.LEADERBOARD_GROUP_GAP_SCALE) + 2.25*(
            settings.HEIGHT/settings.LEADBOARD_PLACE_GAP_CENTERY_SCALE)
        # line for the wave leaderboard
        pygame.draw.line(self.screen, settings.DARK_BLUE, (self.leaderboard_places[0].main_bar.left,y), 
                         (self.leaderboard_places[0].main_bar.right,y), settings.HEADING_BORDER_SIZE)
        # line for the time leaderboard
        pygame.draw.line(self.screen, settings.DARK_BLUE, (self.leaderboard_places[6].main_bar.left,y), 
                         (self.leaderboard_places[6].main_bar.right,y), settings.HEADING_BORDER_SIZE)

        # draw leaderboard places
        for place in self.leaderboard_places:
            place.update()