"""
Containing containing the code for the generic class Character. Inherit from this class whenever creating a new Sprite
"""

import arcade
from ForestKnight.constants import (
    CHARACTER_SCALE,
    FACE_LEFT,
    FACE_RIGHT,
    UPDATES_PER_FRAME,
)
from ForestKnight.helper_functions import load_texture_pair, load_textures


class Character(arcade.AnimatedWalkingSprite):
    """
    Generic Character class based on `arcade.AnimatedWalkingSprite` that all characters - Knight, Zombie and Ninja - will inherit from.
    This makes reduction is code while still having no functionality decreases.
    Add and override methods and attributes as needed
    """

    def __init__(self, pos_x: float, pos_y: float) -> None:
        super().__init__(self)

        # Position and Scaling
        self.center_x = pos_x
        self.center_y = pos_y
        self.scale = CHARACTER_SCALE

        # Sprites and Animation
        self.textures = []

        self.stand_textures = []
        self.stand_left_textures = []
        self.stand_right_textures = []

        self.idle_textures = []
        self.idle_right_textures = []
        self.idle_left_textures = []

        self.walk_textures = []
        self.walk_right_textures = []
        self.walk_left_textures = []

        self.attack_textures = []
        self.attack_left_textures = []
        self.attack_right_textures = []

        self.dying_textures = []
        self.dying_right_textures = []
        self.dying_left_textures = []

        # Variables to control animation and sound speeds
        self.texture_frame_counter = 0

    def setup_textures(self, texture_path: str, movement_type: str) -> None:
        """
        Method that will take a texture path and setup all the base textures
        that the characters have. This method will setup:

        Standing textures
        Idle textures
        Walking textures
        Attack textures
        Dying textures

        Don't override this method. To add custom textures (textures not already setup by this method),
        do it directly in the `__init__` method of the class that inherits from this base class.

        movement_type param: Send 'Walk' or 'Run' based on what the sprite's default movement will be.
        If a character has both Running and Walking textures, set up any one you desire through this method, either
        Run or Walk textures. If running textures are set up by this method, set up walking textures through a custom method.
        Or vice versa.
        """

        # Setting up standing textures
        stand_textures = load_texture_pair(f"{texture_path}/Idle (1).png")
        self.stand_right_textures.append(stand_textures[0])
        self.stand_left_textures.append(stand_textures[1])
        self.stand_textures = self.stand_right_textures + self.stand_left_textures

        # Setting up idle textures
        for idle_right, idle_left in load_textures(
            f"{texture_path}/Idle (<asset_count>).png", 10
        ):
            self.idle_right_textures.append(idle_right)
            self.idle_left_textures.append(idle_left)
        self.idle_textures = self.idle_right_textures + self.idle_left_textures

        # Setting up walking/running textures
        for walk_right, walk_left in load_textures(
            f"{texture_path}/{movement_type} (<asset_count>).png", 10
        ):
            self.walk_right_textures.append(walk_right)
            self.walk_left_textures.append(walk_left)
        self.walk_textures = self.walk_right_textures + self.walk_left_textures

        # Setting up attack textures
        for attack_right, attack_left in load_textures(
            f"{texture_path}/Attack (<asset_count>).png", 10
        ):
            self.attack_right_textures.append(attack_right)
            self.attack_left_textures.append(attack_left)
        self.attack_textures = self.attack_right_textures + self.attack_left_textures

        # Setting up dying textures
        for dying_right, dying_left in load_textures(
            f"{texture_path}/Dead (<asset_count>).png", 10
        ):
            self.dying_right_textures.append(dying_right)
            self.dying_left_textures.append(dying_left)
        self.dying_textures = self.dying_right_textures + self.dying_left_textures

        # Finally wrapping up texture setup
        self.textures = (
            self.stand_textures
            + self.idle_textures
            + self.walk_textures
            + self.attack_textures
            + self.dying_textures
        )

        self.texture = self.idle_textures[0]

    def idle_animation(self):
        """
        Method that contains the animation texture for when the Knight is standing idle
        """
        idle_fps = UPDATES_PER_FRAME + 1

        self.texture_frame_counter += 1
        if self.texture_frame_counter >= len(self.idle_right_textures) * idle_fps:
            self.texture_frame_counter = 0

        if self.state == FACE_RIGHT:
            self.texture = self.idle_right_textures[
                self.texture_frame_counter // idle_fps
            ]
        elif self.state == FACE_LEFT:
            self.texture = self.idle_left_textures[
                self.texture_frame_counter // idle_fps
            ]

    def attack(self):
        """
        Method containing the animation and texture logic to make the Knight do an attack animation.
        Override this method for custom functionalities like adding sounds when the texture is occuring.
        """
        self.texture_frame_counter += 1
        # Attack right and left textures are of equal length so it doesn't matter whose len we use
        if (
            self.texture_frame_counter
            >= len(self.attack_right_textures) * UPDATES_PER_FRAME
        ):
            self.texture_frame_counter = 0

        if self.state == FACE_RIGHT:
            self.texture = self.attack_right_textures[
                self.texture_frame_counter // UPDATES_PER_FRAME
            ]
        elif self.state == FACE_LEFT:
            self.texture = self.attack_left_textures[
                self.texture_frame_counter // UPDATES_PER_FRAME
            ]

    def die(self):
        """
        Method that contains the animation texture for the Knight's dying.
        Override this method for custom functionalities like adding sounds when the texture is occuring.
        """
        self.texture_frame_counter += 1
        if (
            self.texture_frame_counter
            >= len(self.dying_right_textures) * UPDATES_PER_FRAME
        ):
            self.texture_frame_counter = 0
            self.is_dying = False

        if self.state == FACE_RIGHT:
            self.texture = self.dying_right_textures[
                self.texture_frame_counter // UPDATES_PER_FRAME
            ]
        elif self.state == FACE_LEFT:
            self.texture = self.dying_left_textures[
                self.texture_frame_counter // UPDATES_PER_FRAME
            ]
