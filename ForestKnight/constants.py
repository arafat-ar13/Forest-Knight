""" All the constants used throughout the game - all in one file """

# Game window dimensions and title
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
GAME_TITLE = "Forest Knight"

# Constants to hold to path to common directories
IMAGES_DIR = "assets/images"
AUDIO_DIR = "assets/audio"
KNIGHT_IMAGES_DIR = "assets/images/player/knight"
NINJA_IMAGES_DIR = "assets/images/enemies/ninja"
ZOMBIE_FEMALE_IMAGES_DIR = "assets/images/enemies/zombie_female"
ZOMBIE_MALE_IMAGES_DIR = "assets/images/enemies/zombie_male"

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

# Knight constants
KNIGHT_SPEED = 4
KNIGHT_JUMP_SPEED = 12.5
KNIGHT_FACE_RIGHT = 1
KNIGHT_FACE_LEFT = 2
KNIGHT_X = 124
KNIGHT_Y = 124

# Control the speed of Knight animation. Increase value to slow down animation
UPDATES_PER_FRAME = 4

# Directory of where the game data is stored
SAVED_DATA_DIR = "saved_game_data"

# Enemy constants
ZOMBIE_VELOCITY = 2.5
