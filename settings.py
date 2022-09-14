# screen dimensions, set by main.py
WIDTH = 0
HEIGHT = 0

TARGET_FPS = 200 # how many times the game is aiming to update every second

GAME = None        # holds the game object for easy access
current_run = None # holds current run for easy access

# COLOURS
LIGHT_BROWN = "#B47B41"
BROWN = "#8d6333"
DARK_BROWN = "#6F4D28"
LIGHT_BLUE = "#6B93B8"
LIGHT_BLUE_HOVER = "#7DA5CA"
DARK_BLUE = "#46627A"
WHITE = "#d8e3ed"

# BUTTONS
BUTTON_GROW = 1.1               # multiplies the button size for maximum growth size
BUTTON_GROW_SPEED = 2           # amount of pixels buttons grow/shrink per frame
BUTTON_TEXT_COLOUR = 'white'    # colour of every button's text
BUTTON_BORDER_SIZE = 5          # size (in pixels) of the border around buttons

# HEADING MENU
BAR_HEIGHT = 80         # height of top bar
HEADING_BORDER_SIZE = 5 # border width of heading and top bar borders
HEADING_TEXT_SIZE = 100 # size of the heading text

# BOAT
BOAT_SCALE = 1              # multiplier for the boat image size
BOAT_MAX_ANGLE_SPEED = 20   # maximum speed the boat can turn in pixels/second
BOAT_BASE_SPEED = 50        # absolute speed of the boat in pixels/second

# PLAYER BOAT
PB_ANGLE_INP_ACCEL = BOAT_MAX_ANGLE_SPEED/3 # how much the angle velocity can change per second
PB_INP_ACCEL = BOAT_BASE_SPEED/3            # how much the speed can change per second

# CANNONBALL
CANNONBALL_SPEED = 100 # absolute speed of cannonball in pixels/second

# HUD
BAR_RADIUS = 7      # radius of rects on HUD
CROSSHAIR_SCALE = 0.7 # scale up the crosshair image