import arcade
from ForestKnight.constants import CHARACTER_SCALE, KNIGHT_IMAGES_DIR
from ForestKnight.helper_functions import load_texture_pair, load_textures


class Knight(arcade.AnimatedWalkingSprite):
    def __init__(self):
        super().__init__()

        # Knight postion and scaling
        self.center_x = 124
        self.center_y = 124
        self.scale = CHARACTER_SCALE

        # Sprites and Animation
        self.all_textures = []
        self.stand_left_textures = []
        self.stand_right_textures = []
        self.walk_right_textures = []
        self.walk_left_textures = []

        idle_textures = load_texture_pair(f"{KNIGHT_IMAGES_DIR}/Idle (1).png")
        self.stand_right_textures.append(idle_textures[0])
        self.stand_left_textures.append(idle_textures[1])

        self.all_textures.extend(self.stand_right_textures)
        self.all_textures.extend(self.stand_left_textures)

        for texture_right, texture_left in load_textures(f"{KNIGHT_IMAGES_DIR}/Run (<asset_count>).png", 10):
            self.walk_right_textures.append(texture_right)
            self.walk_left_textures.append(texture_left)

        for texture1, texture2 in zip(self.walk_right_textures, self.walk_left_textures):
            self.all_textures.append(texture1)
            self.all_textures.append(texture2)
