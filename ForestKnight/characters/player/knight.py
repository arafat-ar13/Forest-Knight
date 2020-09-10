import sys

import arcade

from constants import (AUDIO_DIR, CHARACTER_SCALE, KNIGHT_FACE_LEFT,
                       KNIGHT_FACE_RIGHT, KNIGHT_IMAGES_DIR, UPDATES_PER_FRAME)
from helper_functions import load_texture_pair, load_textures

sys.path.append("..")


class Knight(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Knight postion and scaling
        self.center_x = 124
        self.center_y = 124
        self.scale = CHARACTER_SCALE

        self.all_textures = []

        # Loading all the different textures of the Knight
        self.idle_textures = load_textures(
            f"{KNIGHT_IMAGES_DIR}/Idle (<asset_count>).png", 10)
        self.walking_textures = load_textures(
            f"{KNIGHT_IMAGES_DIR}/Walk (<asset_count>).png", 10)
        self.running_textures = load_textures(
            f"{KNIGHT_IMAGES_DIR}/Run (<asset_count>).png", 10)
        self.jumping_textures = load_textures(
            f"{KNIGHT_IMAGES_DIR}/Jump (<asset_count>).png", 10)
        self.attack_textures = load_textures(
            f"{KNIGHT_IMAGES_DIR}/Attack (<asset_count>).png", 10)
        self.dying_textures = load_textures(
            f"{KNIGHT_IMAGES_DIR}/Dead (<asset_count>).png", 10)

        # Adding all the different textures to self.textures
        for textures in zip(self.idle_textures, self.walking_textures, self.running_textures, self.jumping_textures, self.attack_textures, self.dying_textures):
            for texture in textures:
                self.all_textures.extend(texture)

        # Variables to keep track of the direction the knight is facing
        # The default face direction would be right
        self.face_direction = KNIGHT_FACE_RIGHT

        # Variables to keep track of the state of the knight
        self.is_on_ladder = False
        self.is_attacking = False
        self.is_dead = False
        self.is_jumping = False

        # Initial Idle texture
        self.texture = self.idle_textures[0][0]

        # Used for flipping between image sequences
        self.cur_texture = 0
        # Used for slowing down the frames when playing animation sound
        self.sound_frame_counter = 0

        # Knight's gameplay stats
        self.health = 50
        self.score = 0
        self.level = None
        self.attack_points = None

        # Loading up different sounds of the Knight
        self.jump_sound = arcade.load_sound(f"{AUDIO_DIR}/jump1.wav")
        self.walk_sound = arcade.load_sound(f"{AUDIO_DIR}/footstep01.ogg")
        self.attack_sound = arcade.load_sound(f"{AUDIO_DIR}/knifeSlice2.ogg")
        self.hurt_sound = arcade.load_sound(f"{AUDIO_DIR}/hurt1.wav")

    def update_animation(self):
        """ Method that updates the animation of the Knight using the loaded textures """

        # First, let's figure out how the Knight moves and set it's face direction accordingly
        if self.change_x < 0 and self.face_direction == KNIGHT_FACE_RIGHT:
            self.face_direction = KNIGHT_FACE_LEFT
        elif self.change_x > 0 and self.face_direction == KNIGHT_FACE_LEFT:
            self.face_direction = KNIGHT_FACE_RIGHT

        # Walking animation
        if self.change_x > 0 or self.change_x < 0:
            self.cur_texture += 1
            if self.cur_texture >= len(self.walking_textures) * UPDATES_PER_FRAME:
                self.cur_texture = 0
            self.texture = self.walking_textures[self.cur_texture //
                                                 UPDATES_PER_FRAME][self.face_direction]

            # Playing walking sound
            self.sound_frame_counter += 1
            if self.sound_frame_counter > 15:
                self.sound_frame_counter = 0
                self.walk_sound.play(volume=0.2)

            return
        
        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.cur_texture += 1
            if self.cur_texture >= len(self.jumping_textures) * UPDATES_PER_FRAME:
                self.cur_texture = 0
            self.texture = self.jumping_textures[self.cur_texture //
                                                 UPDATES_PER_FRAME][self.face_direction]

            return

        # Attacking animation
        if self.is_attacking:
            self.cur_texture += 1
            if self.cur_texture >= len(self.attack_textures) * UPDATES_PER_FRAME:
                self.cur_texture = 0
            self.texture = self.attack_textures[self.cur_texture //
                                                UPDATES_PER_FRAME][self.face_direction]

            # Playing attacking sound
            self.sound_frame_counter += 1
            if self.sound_frame_counter > 30:
                self.sound_frame_counter = 0
                self.attack_sound.play(volume=0.2)

            return

        # Dying animation
        if self.is_dead:
            self.cur_texture += 1
            if self.cur_texture >= len(self.dying_textures) * UPDATES_PER_FRAME:
                self.cur_texture = 0
            self.texture = self.dying_textures[self.cur_texture // UPDATES_PER_FRAME][self.face_direction]

        # Idle animation
        if self.change_x == 0:
            self.cur_texture += 1
            if self.cur_texture >= len(self.idle_textures) * UPDATES_PER_FRAME:
                self.cur_texture = 0
            self.texture = self.idle_textures[self.cur_texture //
                                              UPDATES_PER_FRAME][self.face_direction]

            return
