"""
Module that defines the Male Zombie enemy in the game. It contains all the code
and logic for the movement and attack mechanism of the Male Zombie
"""

from ForestKnight.characters.enemies.zombie import Zombie
from ForestKnight.constants import ZOMBIE_MALE_IMAGES_DIR


class ZombieMale(Zombie):
    """Main Class containing the code of the Male Zombie"""

    def __init__(self, pos_x: float, pos_y: float) -> None:
        super().__init__(pos_x, pos_y, images_dir=ZOMBIE_MALE_IMAGES_DIR)
