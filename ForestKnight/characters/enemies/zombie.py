"""
There will be two variations of the Zombie enemy in the game.
The first one will be a male and the second one will be a female zombie.
While both of them will feature different properties like speed, health, attack points, etc. They
will all a lot of commonalities. This module will contain the generic class Zombie that those two
sprites will inherit from.
"""

from ForestKnight.characters.character import Character
from ForestKnight.constants import CHARACTER_SCALE


class Zombie(Character):
    def __init__(self, pos_x: float, pos_y: float, images_dir: str):
        super().__init__(pos_x=pos_x, pos_y=pos_y)

        self.images_dir = images_dir

        # Zombie positions and scaling
        self.center_x = pos_x
        self.center_y = pos_y
        self.scale = CHARACTER_SCALE

        # Setting up textures
        self.setup_textures(texture_path=self.images_dir, movement_type="Walk")

        # Setting up Zombie stats -- Override as needed
        self.health = None
        self.attack_points = None
        self.speed = None
