import arcade
from arcade.sound import load_sound
from ForestKnight.constants import (
    AUDIO_DIR,
    CHARACTER_SCALE,
    KNIGHT_FACE_LEFT,
    KNIGHT_FACE_RIGHT,
    KNIGHT_IMAGES_DIR,
    KNIGHT_X,
    KNIGHT_Y,
    UPDATES_PER_FRAME,
)
from ForestKnight.helper_functions import load_texture_pair, load_textures


class Knight(arcade.AnimatedWalkingSprite):
    def __init__(self):
        super().__init__()

        # Knight postion and scaling
        self.center_x = KNIGHT_X
        self.center_y = KNIGHT_Y
        self.scale = CHARACTER_SCALE

        # Sprites and Animation
        self.textures = []

        self.stand_textures = []
        self.stand_left_textures = []
        self.stand_right_textures = []

        self.walk_textures = []
        self.walk_right_textures = []
        self.walk_left_textures = []

        self.attack_textures = []
        self.attack_left_textures = []
        self.attack_right_textures = []

        self.dying_textures = []
        self.dying_right_textures = []
        self.dying_left_textures = []

        idle_textures = load_texture_pair(f"{KNIGHT_IMAGES_DIR}/Idle (1).png")
        self.stand_right_textures.append(idle_textures[0])
        self.stand_left_textures.append(idle_textures[1])
        self.stand_textures = self.stand_right_textures + self.stand_left_textures

        for texture_right, texture_left in load_textures(
            f"{KNIGHT_IMAGES_DIR}/Run (<asset_count>).png", 10
        ):
            self.walk_right_textures.append(texture_right)
            self.walk_left_textures.append(texture_left)
        self.walk_textures = self.walk_right_textures + self.walk_left_textures

        for attack_right, attack_left in load_textures(
            f"{KNIGHT_IMAGES_DIR}/Attack (<asset_count>).png", 10
        ):
            self.attack_right_textures.append(attack_right)
            self.attack_left_textures.append(attack_left)
        self.attack_textures = self.attack_right_textures + self.attack_left_textures

        for dying_right, dying_left in load_textures(
            f"{KNIGHT_IMAGES_DIR}/Dead (<asset_count>).png", 10
        ):
            self.dying_right_textures.append(dying_right)
            self.dying_left_textures.append(dying_left)
        self.dying_textures = self.dying_right_textures + self.dying_left_textures

        self.textures = (
            self.stand_textures
            + self.walk_textures
            + self.attack_textures
            + self.dying_textures
        )

        self.texture = self.stand_right_textures[0]

        # Sounds related to the Knight
        self.jump_sound = None
        self.run_sound = None
        self.attack_sound = None

        # Variables to control animation and sound speeds
        self.sound_frame_counter = 0
        self.texture_frame_counter = 0

        # Variables to keep track of the Knight's states
        self.is_attacking = False
        self.is_dying = False

        # Knight's stats
        self.score = 0
        self.health = 50

    def setup_sounds(self):
        self.jump_sound = load_sound(f"{AUDIO_DIR}/jump3.wav")
        self.run_sound = load_sound(f"{AUDIO_DIR}/footstep01.ogg")
        self.attack_sound = load_sound(f"{AUDIO_DIR}/knifeSlice2.ogg")

    def attack(self):
        """Method containing the animation and texture logic to make the Knight do an attack animation"""
        self.texture_frame_counter += 1
        # Attack right and left textures are of equal length so it doesn't matter whose len we use
        if (
            self.texture_frame_counter
            >= len(self.attack_right_textures) * UPDATES_PER_FRAME
        ):
            self.texture_frame_counter = 0

        if self.state == KNIGHT_FACE_RIGHT:
            self.texture = self.attack_right_textures[
                self.texture_frame_counter // UPDATES_PER_FRAME
            ]
        elif self.state == KNIGHT_FACE_LEFT:
            self.texture = self.attack_left_textures[
                self.texture_frame_counter // UPDATES_PER_FRAME
            ]

        # Playing attacking sound
        self.sound_frame_counter += 1
        if self.sound_frame_counter > 30:
            self.sound_frame_counter = 0
            self.attack_sound.play(volume=0.2)

    def die(self):
        """Method that contains the animation texture for the Knight's dying"""
        self.texture_frame_counter += 1
        if (
            self.texture_frame_counter
            >= len(self.dying_right_textures) * UPDATES_PER_FRAME
        ):
            self.texture_frame_counter = 0
            self.is_dying = False

        if self.state == KNIGHT_FACE_RIGHT:
            self.texture = self.dying_right_textures[
                self.texture_frame_counter // UPDATES_PER_FRAME
            ]
        elif self.state == KNIGHT_FACE_LEFT:
            self.texture = self.dying_left_textures[
                self.texture_frame_counter // UPDATES_PER_FRAME
            ]

    def update_animation(self, delta_time: float):
        # Playing Knight walking sound
        if self.change_x > 0 or self.change_x < 0:
            self.sound_frame_counter += 1
            if self.sound_frame_counter > 15:
                self.sound_frame_counter = 0
                self.run_sound.play(volume=0.2)

        # Restrict Knight from falling off the left edge
        if self.left < 0:
            self.left = 0

        return super().update_animation(delta_time=delta_time)
