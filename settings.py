# screen dimensions, set by main.py
WIDTH = 0
HEIGHT = 0

TARGET_FPS = 200 # how many times the game is aiming to update every second

GAME = None        # holds the game object for easy access
current_run = None # holds current run for easy access

# COLOURS
LIGHT_BROWN = "#B47B41"
LIGHT_BROWN_HOVER = "#D49455"
BROWN = "#8d6333"
DARK_BROWN = "#6F4D28"
LIGHT_BLUE = "#6B93B8"
LIGHT_BLUE_HOVER = "#7DA5CA"
DARK_BLUE = "#46627A"
WHITE = "#d8e3ed"
RED = "#ff1100"

# BUTTONS
BUTTON_GROW = 1.1               # multiplies the button size for maximum growth size
BUTTON_GROW_SPEED = 2           # amount of pixels buttons grow/shrink per frame
BUTTON_TEXT_COLOUR = 'white'    # colour of every button's text
BUTTON_BORDER_SIZE = 5          # size (in pixels) of the border around buttons

# HEADING MENU
BAR_HEIGHT = 80         # height of top bar
HEADING_BORDER_SIZE = 5 # border width of heading and top bar borders
HEADING_TEXT_SIZE = 100 # size of the heading text

# START MENU
START_MENU_BG_SCROLL_SPEED = 64 # pixels scrolled per second

# END MENU
END_MENU_HIGHSCORE_GAP = 200    # gap between stat and highscore
END_MENU_BAR_GAP = 20           # gap between bars
END_MENU_BAR_BORDER_WIDTH = 5   # border width of bars
END_MENU_PADDING = 10           # padding between bar edge and stat
END_MENU_BAR_RADIUS = 15        # border radius of bars

# BOAT
BOAT_SCALE = 1              # multiplier for the boat image size
BOAT_MAX_ANGLE_SPEED = 20   # maximum speed the boat can turn in pixels/second
BOAT_BASE_SPEED = 50        # absolute speed of the boat in pixels/second

# PLAYER BOAT
PB_ANGLE_INP_ACCEL = BOAT_MAX_ANGLE_SPEED/3 # how much the angle velocity can change per second
PB_INP_ACCEL = BOAT_BASE_SPEED/3            # how much the speed can change per second
PB_SAIL_HIDDEN_ALPHA = 63                   # transparency of sails when in switching state
PB_STATE_SWITCH_TIME = 0.5                  # amount of seconds it takes to switch state
PB_FEATURE_MAX_SIZE_GROW = 5                # maximum amount of pixels the image can grow
PB_FEATURE_GROW_SPEED = 1                   # pixels feauture image grows/shrinks per frame
PB_BASE_SPEED = BOAT_BASE_SPEED             # starting speed of player boat
PB_BASE_DAMAGE = 20                         # starting damage of player boat
PB_BASE_HP = 200                            # starting hp of player boat

# ENEMY BOAT
ENEMY_SHOOT_DISTANCE = 400               # base distance away from player (pixels) enemy can shoot from
ENEMY_MIN_SHOOT_TIME = 5                 # minimum time enemies must wait between shots in seconds
ENEMY_MAX_SHOOT_TIME = 20                # maximum time enemies must wait between shots in seconds
ENEMY_ACCELERATION = BOAT_BASE_SPEED/1.5 # change in speed per second
ENEMY_BASE_HP = 100                      # starting HP of enemies
ENEMY_BASE_DMG = 10                      # starting damage of enemies
ENEMY_BASE_SPD = BOAT_BASE_SPEED         # starting speed of enemies
ENEMY_GOLD_CHANCE = 40                   # % chance for enemy to drop gold
MIN_ENEMY_GOLD_AMOUNT = 1                # minimum gold drop when enemy drops gold
MAX_ENEMY_GOLD_AMOUNT = 3                # maximum gold drop when enemy drops gold
ENEMY_HP_CHANCE = 10                     # % chance for enemy kill to give player hp
ENEMY_HP_REGEN = 10                      # how much hp enemy kills give the player

# ENEMY SPAWNING
START_WAVE_NUM = 10          # amount of enemies in wave 1
WAVE_BREAK_TIME = 10         # amount of seconds between waves
MIN_SPAWN_TIME = 2           # minimum amount of seconds between enemy spawns
MAX_SPAWN_TIME = 4           # maximum amount of seconds between enemy spawns
MAX_SPAWN_DIVIDE = 3         # divides total enemies to spawn to get maximum enemies to spawn per spawn
MIN_SPAWN_DISTANCE = 700     # minimum distance (pixels) enemies can spawn
MAX_SPAWN_DISTANCE = 1000    # maximum distance (pixels) enemies can spawn
WAVE_ENEMY_INCREASE = 1      # amount of extra enemies per wave
ENEMY_HP_ADD = 20            # how much enemy hp increases per wave
ENEMY_DMG_ADD = 1            # how much enemy damage increases per wave
ENEMY_SPD_ADD =  0.1         # how much enemy speed increases per wave

# CANNONBALL
CANNONBALL_SPEED = 100 # absolute speed of cannonball in pixels/second

# HUD
BAR_RADIUS = 7                  # radius of rects on HUD
CROSSHAIR_SCALE = 0.7           # scale up the crosshair image
ENEMY_HEALTH_BAR_WIDTH = 100    # pixel width of enemy health bar
ENEMY_HEATH_BAR_HEIGHT = 10     # pixel height of enemy health bar
ENEMY_HEALTH_BAR_OFFSET = 5     # pixels above enemy
HUD_INFO_FONT_SIZE = 40         # size of font for text on HUD
HUD_PADDING = 15                # pixel padding between text on HUD

# MAP
MAIN_MAP_IMAGE = "map/map.png"  # location of the main map image
PIECE_SIZE = 64                 # width+height in pixels of map piece

# PORTS
PORT_IMAGE = "map/port.png"     # location of the port image
PORT_RADIUS = 300               # radius around port where player can interact with it
PORT_RING_MIN_RAD = 50          # minimum radius of ring around port on HUD
PORT_RING_MAX_RAD = 100         # maximum radius of ring around port on HUD
PORT_RING_SPEED = 50            # change in radius of ring around port on HUD per second
PORT_RING_WIDTH = 5             # width of ring around port on HUD
PORT_Y_OFFSET = 40              # how high up the text prompt for the port is above the port