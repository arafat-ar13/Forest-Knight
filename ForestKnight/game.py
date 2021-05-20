import arcade
from arcade.sprite_list import SpriteList
from arcade.window_commands import start_render

from ForestKnight.characters.player.knight import Knight
from ForestKnight.constants import (GAME_TITLE, IMAGES_DIR, SCREEN_HEIGHT,
                                    SCREEN_WIDTH)
from ForestKnight.level_loader import level_loader


class ForestKnight(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)

    def setup(self):
        self.character_sprites = SpriteList()

        self.setup_sprites()
        self.setup_characters()
        self.setup_sounds()
        self.setup_images()

    def setup_sprites(self):
        """ Method that sets up all the Sprites (except for Player and Enemies) """
        loaded_sprites = level_loader(1)

        self.platforms = loaded_sprites["Platforms"]
        self.foregrounds = loaded_sprites["Foregrounds"]
        self.backgrounds = loaded_sprites["Backgrounds"]
        self.ladders = loaded_sprites["Ladders"]
        self.dont_touch = loaded_sprites["Dont-Touch"]
        self.collectibles = loaded_sprites["Collectibles"]

    def setup_characters(self):
        """ Method to set up the Knight and other Enemies """
        self.knight = Knight()
        self.character_sprites.append(self.knight)
        self.character_sprites.preload_textures(self.knight.all_textures)

    def setup_sounds(self):
        pass

    def setup_images(self):
        self.background_image = arcade.load_texture(
            f"{IMAGES_DIR}/backgrounds/BG.png"
        )

    def on_update(self, delta_time):
        self.character_sprites.update()
        self.character_sprites.update_animation()

    def on_draw(self):
        start_render()

        self.platforms.draw()
        self.backgrounds.draw()
        self.ladders.draw()
        self.collectibles.draw()
        self.character_sprites.draw()
        self.dont_touch.draw()
        self.foregrounds.draw()
