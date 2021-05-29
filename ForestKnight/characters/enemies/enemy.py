"""
There will be two variations of the Zombie enemy in the game.
The first one will be a male and the second one will be a female zombie.
While both of them will feature different properties like speed, health, attack points, etc. They
will all a lot of commonalities. This module will contain the generic class Zombie that those two
sprites will inherit from.
"""

from arcade.sprite_list import check_for_collision
from ForestKnight.characters.character import Character
from ForestKnight.characters.player.knight import Knight
from ForestKnight.constants import ENEMY_SCALE


class Enemy(Character):
    def __init__(self, pos_x: float, pos_y: float, images_dir: str):
        super().__init__(pos_x=pos_x, pos_y=pos_y)

        self.images_dir = images_dir

        # Zombie positions and scaling
        self.center_x = pos_x
        self.center_y = pos_y
        self.scale = ENEMY_SCALE

        # Setting up textures
        self.setup_textures(texture_path=self.images_dir, movement_type="Walk")

        # Setting up Zombie stats -- Override as needed
        self.health = None
        self.attack_points = None
        self.speed = None

        # Controlling movement
        self.movement_range_start = None
        self.movement_range_end = None
        self.movement_range = None

    def detect_knight(self, knight: Knight) -> None:
        """
        Method that will calculate if the Knight is near the enemy. If it is, the enemy moves toward it
        and starts attacking the Knight. 
        """

        y_diff = abs(self.center_y - knight.center_y)
        x_diff = knight.center_x - self.center_x

        if y_diff > 0 and y_diff < 10:
            if x_diff > 0:
                knight_loc = "in front"
            elif x_diff < 0:
                knight_loc = "behind"

            colliding = check_for_collision(self, knight)

            if not colliding:
                # We'll only move the enemy if the Knight and enemy are not colliding
                if knight_loc == "in front":
                    self_new_pos = self.center_x + x_diff
                    if self_new_pos <= self.movement_range_end:
                        self.change_x = self.speed
                    else:
                        self.change_x = 0

                elif knight_loc == "behind":
                    self_new_pos = self.center_x - x_diff
                    if self_new_pos >= self.movement_range_start:
                        self.change_x = -(self.speed)
                    else:
                        self.change_x = 0

            else:
                self.change_x = 0
                self.attack()
        else:
            self.change_x = 0
