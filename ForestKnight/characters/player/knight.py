"""
Source code that handles everything about the main player of the game - The Knight
"""

from arcade.sound import load_sound
from ForestKnight.characters.character import Character
from ForestKnight.constants import (
    AUDIO_DIR,
    KNIGHT_IMAGES_DIR,
    KNIGHT_JUMP_SPEED,
    KNIGHT_SPEED,
)


class Knight(Character):
    """
    The class that defines the characteristics of The Knight and contains all the logic
    """

    def __init__(self, pos_x: float, pos_y: float):
        super().__init__(pos_x, pos_y)

        self.setup_textures(texture_path=KNIGHT_IMAGES_DIR, movement_type="Run")

        # Sounds related to the Knight
        self.jump_sound = None
        self.run_sound = None
        self.attack_sound = None

        # Variables to keep track of the Knight's states
        self.is_attacking = False
        self.is_dying = False
        self.is_moving = False

        # Knight's stats
        self.score = 0
        self.health = 50
        self.attack_points = 10
        self.speed = KNIGHT_SPEED
        self.jump_speed = KNIGHT_JUMP_SPEED

        # Variables to control Knight sound speeds
        self.sound_frame_counter = 0

    def setup_sounds(self):
        """Method to setup all the Knight-related sounds"""
        self.jump_sound = load_sound(f"{AUDIO_DIR}/jump3.wav")
        self.run_sound = load_sound(f"{AUDIO_DIR}/footstep01.ogg")
        self.attack_sound = load_sound(f"{AUDIO_DIR}/knifeSlice2.ogg")

    def attack(self):
        """Overriding parent attack method to add animation sound"""
        # Playing attacking sound
        self.sound_frame_counter += 1
        if self.sound_frame_counter > 30:
            self.sound_frame_counter = 0
            self.attack_sound.play(volume=0.2)

        return super().attack()

    def update_animation(self, delta_time: float):
        """Method that is called about 60 times every second to update the animation of the Knight"""
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
