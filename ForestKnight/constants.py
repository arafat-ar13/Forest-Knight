""" Python file containing all the constants used throughout the game - all in one file """

# Game window dimensions and title
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
GAME_TITLE = "Forest Knight"

# Constants to hold to path to common directories
IMAGES_DIR = "assets/images"
AUDIO_DIR = "assets/audio"
KNIGHT_IMAGES_DIR = "assets/images/player/knight"
# Enemies
NINJA_IMAGES_DIR = "assets/images/enemies/ninja"
ZOMBIE_FEMALE_IMAGES_DIR = "assets/images/zombie_female"
ZOMBIE_MALE_IMAGES_DIR = "assets/images/zombie_male"

# Scaling
TILE_SCALE = 0.5
CHARACTER_SCALE = 0.16

# Player scrolling
# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

# Gravity
GRAVITY = 1

# Knight moving velocity and other constants
KNIGHT_SPEED = 9
KNIGHT_JUMP_SPEED = 19
KNIGHT_FACE_RIGHT = 0
KNIGHT_FACE_LEFT = 1

# Constant to control the speed of Knight animation. Increase the value to slow down animation speed
UPDATES_PER_FRAME = 4