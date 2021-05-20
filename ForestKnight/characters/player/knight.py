import arcade
from arcade.sound import load_sound
from ForestKnight.constants import AUDIO_DIR, CHARACTER_SCALE, KNIGHT_IMAGES_DIR
from ForestKnight.helper_functions import load_texture_pair, load_textures


class Knight(arcade.AnimatedWalkingSprite):
    def __init__(self):
        super().__init__()

        # Knight postion and scaling
        self.center_x = 124
        self.center_y = 124
        self.scale = CHARACTER_SCALE
        self.face_right = True
        self.face_left = False

        # Sprites and Animation
        self.all_textures = []
        self.stand_left_textures = []
        self.stand_right_textures = []
        self.walk_right_textures = []
        self.walk_left_textures = []
        self.attack_left_textures = []
        self.attack_right_textures = []

        idle_textures = load_texture_pair(f"{KNIGHT_IMAGES_DIR}/Idle (1).png")
        self.stand_right_textures.append(idle_textures[0])
        self.stand_left_textures.append(idle_textures[1])

        self.all_textures.extend(self.stand_right_textures)
        self.all_textures.extend(self.stand_left_textures)

        for texture_right, texture_left in load_textures(f"{KNIGHT_IMAGES_DIR}/Run (<asset_count>).png", 10):
            self.walk_right_textures.append(texture_right)
            self.walk_left_textures.append(texture_left)

        for attack_right, attack_left in load_textures(f"{KNIGHT_IMAGES_DIR}/Attack (<asset_count>).png", 10):
            self.attack_right_textures.append(attack_right)
            self.attack_left_textures.append(attack_left)

        for texture1, texture2, texture3, texture4 in zip(self.walk_right_textures, self.walk_left_textures, self.attack_right_textures, self.attack_left_textures):
            self.all_textures.append(texture1)
            self.all_textures.append(texture2)
            self.all_textures.append(texture3)
            self.all_textures.append(texture4)

        # Used for slowing down the frames when playing animation sound
        self.sound_frame_counter = 0

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

        return super().update_animation(delta_time=delta_time)
