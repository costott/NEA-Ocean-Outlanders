# screen dimensions, set by main.py
WIDTH = 0
HEIGHT = 0

TARGET_FPS = -1 # how many times the game is aiming to update every second

GAME = None        # holds the game object for easy access
current_run = None # holds current run for easy access

# COLOURS
LIGHT_BROWN = "#B47B41"
LIGHT_BROWN_HOVER = "#D49455"
BROWN = "#8d6333"
DARK_BROWN = "#6F4D28"
DARK_BROWN_HOVER = "#82613C"
LIGHT_BLUE = "#6B93B8"
LIGHT_BLUE_HOVER = "#7DA5CA"
DARK_BLUE = "#46627A"
DARK_BLUE_HOVER = "#5E7992"
WHITE = "#d8e3ed"
DARK_RED = "#760000"
RED = "#ff1100"
DARK_YELLOW = "#575F00"
YELLOW = "#CDDC21"
DARK_GREEN = "#006A19"
GREEN = "#00FF3C"
GOLD = "#E1B333"
SILVER = "#C8C6C4"
BRONZE = "#EA8B2D"

# BUTTONS
BUTTON_GROW = 1.1               # multiplies the button size for maximum growth size
BUTTON_GROW_SPEED = 1.5           # amount of pixels buttons grow/shrink per frame
BUTTON_TEXT_COLOUR = 'white'    # colour of every button's text
BUTTON_BORDER_SIZE = 5          # size (in pixels) of the border around buttons

# HEADING MENU
BAR_HEIGHT = 80         # height of top bar
HEADING_BORDER_SIZE = 5 # border width of heading and top bar borders
HEADING_TEXT_SIZE = 100 # size of the heading text

# START MENU
START_MENU_BG_SCROLL_SPEED = 64 # pixels scrolled per second

# DATABASE
DATABASE_LOCATION = "ocean_outlanders.db"

# LOGGING IN
MIN_USERNAME_LEN = 1   # minimum accepted username length
MAX_USERNAME_LEN = 12  # maximum accepted username length
MIN_PASSWORD_LEN = 4   # mininum accepted password length
MAX_PASSWORD_LEN = 60  # maximum accepted password length

# TEXT BOX
TEXT_BOX_WIDTH_SCALE = 1.5     # fraction of WIDTH of screen
TEXT_BOX_HEIGHT_SCALE = 10     # fraction of HEIGHT of screen
TEXT_BOX_BORDER_WIDTH = 10     # width of border around text box
TEXT_BOX_FONT_SIZE = 30        # font size of text box heading
TEXT_BOX_TEXT_OFFSET = 5       # y offset of text box heading
TEXT_BOX_INPUT_OFFSET = 5      # x offset of text in text box

# MAIN MENU
MAIN_MENU_BOAT_IMAGE1_LOCATION = "assets/boat_scene.png"  # image on the left of the main menu
MAIN_MENU_BOAT_IMAGE2_LOCATION = "assets/boat_scene2.png" # image on the right of the main menu
MAIN_MENU_BOAT_IMAGE_SCALE = 0.6                          # scale of images above

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
COLLIDE_SIZE = 100          # 'radius' of square chunk for boat collision

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

# EXPLOSIVE CANNONBALL
EXPLOSIVE_CANNONBALL_RADIUS = 200             # radius of range where boats will take damage  
EXPLOSIVE_CANNONBALL_DAMAGE_MULTIPLIER = 0.7  # multiplies current cannonball damage for explosion damage at centre
EXPLOSIVE_CANNONBALL_FALLOFF = 0.25           # multiplier of total damage at the edge of explosion

# EXPLOSION EFFECT
EXPLOSION_ANIMATION_SWITCH_TIME = 0.07 # time between explosion animatin frames
EXPLOSION_SCALE = 1.5                  # scale of original image

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

# SHOP
SHOP_GOLD_FONT_SIZE = 50        # font size of gold at top of shop
SHOP_GOLD_PADDING = 10          # space between gold text and box it's in
SHOP_BUTTON_WIDTH_SCALE = 3.5   # fraction of WIDTH of screen
SHOP_BUTTON_HEIGHT_SCALE = 4.25 # fraction of HEIGHT of screen
SHOP_BUTTON_BORDER_WIDTH = 10   # width of border around shop buttons
SHOP_BUTTON_BORDER_RADIUS = 30  # radius of shop buttons
SHOP_PRICE_WIDTH_SCALE = 2.5    # fraction of width of shop button

# UPGRADES
EXPLOSIVE_PRICE = 100         # price of explosive cannonball
CHAINING_PRICE = 250          # price of chaining cannonball
HP_UNIT_PRICE = 0.3           # amount of gold per 1 hp
HP_PERCENT_INCREASE = 0.1     # % increase of current speed to next upgrade
DMG_UNIT_PRICE = 4            # amount of gold per 1 damage 
DMG_PERCENT_INCREASE = 0.05   # % increase of current damage to next upgrade
SPEED_UNIT_PRICE = 10         # amount of gold per 1 speed
SPEED_PERCENT_INCREASE = 0.01 # % increase of current speed to next upgrade

# LEADERBOARD
LEADERBORD_HEADING_PADDING = 2              # gap between leaderboard heading and edge of heading/screen
LEADERBOARD_HEADING_RADIUS = 10             # radius of leaderboard heading box
LEADERBOARD_PLACE_WIDTH_SCALE = 2.7         # fraction of WIDTH of screen for full width of a leaderboard place
LEADERBOARD_PLACE_HEIGHT_SCALE = 12         # fraction of HEIGHT of screen for full height of a leaderboard place
LEADERBORD_PLACE_NUMBER_WIDTH_SCALE = 7.6   # fraction of width of main leaderboard place bar for the number bar
LEADERBOARD_PLACE_VALUE_WIDTH_SCALE = 2.5   # fraction of width of main leaderboar place bar for the value bar
LEADERBOARD_PLACE_RADIUS = 30               # radius of leadearboard place bar
LEADERBOARD_PLACE_START_CENTERY_SCALE = 3.4 # fraction of HEIGHT of screen for center y position of 1st place
LEADBOARD_PLACE_GAP_CENTERY_SCALE = 10.8    # fraction of HEIGHT of screen for y gaps between places
LEADERBOARD_GROUP_GAP_SCALE = 20            # fraction of HEIGHT of screen for gap between top 3 and neigbour places
WAVE_PLACE_CENTERX_SCALE = 4                # fraction of WIDTH of screen for center x position of wave places
TIME_PLACE_CENTERX_SCALE = 1.4              # fraction of WIDTH of screen for center x position of time places

# CONTROLS SCREEN
CONTROLS_IMAGE_LOCATION = "assets/controls.png" # location of controls image
CONTROLS_IMAGE_SCALE = 0.65                     # multiplier to scale controls image