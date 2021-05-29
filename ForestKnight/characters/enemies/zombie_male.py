"""
Module that defines the Male Zombie enemy in the game. It contains all the code
and logic for the movement and attack mechanism of the Male Zombie
"""

from ForestKnight.characters.enemies.enemy import Enemy
from ForestKnight.constants import ZOMBIE_MALE_IMAGES_DIR, ZOMBIE_VELOCITY


class ZombieMale(Enemy):
    """Main Class containing the code of the Male Zombie"""

    def __init__(self, pos_x: float, pos_y: float) -> None:
        super().__init__(pos_x, pos_y, images_dir=ZOMBIE_MALE_IMAGES_DIR)

        # Zombie's Stats
        self.health = 30
        self.attack_points = 2
        self.speed = ZOMBIE_VELOCITY

        # Controlling auto-movement
        self.movement_range_start = self.center_x
        self.movement_range_end = 630
        self.movement_range = self.movement_range_end - self.movement_range_start
