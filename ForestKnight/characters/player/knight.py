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
        self.stand_left_textures = []
        self.stand_right_textures = []
        self.walk_right_textures = []
        self.walk_left_textures = []
        self.attack_left_textures = []
        self.attack_right_textures = []

        idle_textures = load_texture_pair(f"{KNIGHT_IMAGES_DIR}/Idle (1).png")
        self.stand_right_textures.append(idle_textures[0])
        self.stand_left_textures.append(idle_textures[1])

        self.textures.extend(self.stand_right_textures)
        self.textures.extend(self.stand_left_textures)

        for texture_right, texture_left in load_textures(
            f"{KNIGHT_IMAGES_DIR}/Run (<asset_count>).png", 10
        ):
            self.walk_right_textures.append(texture_right)
            self.walk_left_textures.append(texture_left)

        for attack_right, attack_left in load_textures(
            f"{KNIGHT_IMAGES_DIR}/Attack (<asset_count>).png", 10
        ):
            self.attack_right_textures.append(attack_right)
            self.attack_left_textures.append(attack_left)

        for texture1, texture2, texture3, texture4 in zip(
            self.walk_right_textures,
            self.walk_left_textures,
            self.attack_right_textures,
            self.attack_left_textures,
        ):
            self.textures.append(texture1)
            self.textures.append(texture2)
            self.textures.append(texture3)
            self.textures.append(texture4)

        # Variables to control animation and sound speeds
        self.sound_frame_counter = 0
        self.texture_frame_counter = 0

        # Variables to keep track of the Knight's states
        self.is_attacking = False

        # Knight's stats
        self.score = 0
        self.health = 50

    def setup_sounds(self):
        self.jump_sound = load_sound(f"{AUDIO_DIR}/jump3.wav")
        self.run_sound = load_sound(f"{AUDIO_DIR}/footstep01.ogg")
        self.attack_sound = load_sound(f"{AUDIO_DIR}/knifeSlice2.ogg")

    def update_animation(self, delta_time: float):
        # Playing Knight walking sound
        if self.change_x > 0 or self.change_x < 0:
            self.sound_frame_counter += 1
            if self.sound_frame_counter > 15:
                self.sound_frame_counter = 0
                self.run_sound.play(volume=0.2)

        # Handling Knight's attack animations
        # if self.is_attacking:
        #     self.texture_frame_counter += 1
        #     # Attack right and left textures are of equal length so it doesn't matter whose len we use
        #     if self.texture_frame_counter >= len(self.attack_right_textures) * UPDATES_PER_FRAME:
        #         self.texture_frame_counter = 0
        #     if self.state == KNIGHT_FACE_RIGHT:
        #         self.texture = self.attack_right_textures[self.texture_frame_counter //
        #                                                   UPDATES_PER_FRAME]
        #     elif self.state == KNIGHT_FACE_LEFT:
        #         self.texture = self.attack_left_textures[self.texture_frame_counter //
        #                                                  UPDATES_PER_FRAME]

        return super().update_animation(delta_time=delta_time)
