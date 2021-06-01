""" All the constants used throughout the game - all in one file """

# Game window dimensions and title
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
GAME_TITLE = "Forest Knight"
GAME_VERSION = "0.7.9"
DEVELOPER = "Arafat Khan"

# Constants to hold to path to common directories
IMAGES_DIR = "assets/images"
AUDIO_DIR = "assets/audio"
FONTS_DIR = "assets/fonts"
KNIGHT_IMAGES_DIR = "assets/images/player/knight"
NINJA_IMAGES_DIR = "assets/images/enemies/ninja"
ZOMBIE_FEMALE_IMAGES_DIR = "assets/images/enemies/zombie_female"
ZOMBIE_MALE_IMAGES_DIR = "assets/images/enemies/zombie_male"

# Scaling
TILE_SCALE = 0.5
CHARACTER_SCALE = 0.16
ENEMY_SCALE = 0.2

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
KNIGHT_JUMP_SPEED = 13
KNIGHT_X = 124
KNIGHT_Y = 241

# Control the speed of Knight animation. Increase value to slow down animation
UPDATES_PER_FRAME = 3

# Directory of where the game data is stored
SAVED_DATA_DIR = "saved_game_data"

# Enemy constants
ZOMBIE_VELOCITY = 3
ZOMBIE_MALE_LEVEL_1_POSITIONS = [(290.0, 430.25)]

# Other constants
FACE_RIGHT = 1
FACE_LEFT = 2