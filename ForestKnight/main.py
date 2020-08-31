import arcade

from constants import *


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)

        arcade.set_background_color(arcade.csscolor.ORANGE_RED)

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()

    def on_update(self, dt):
        pass


def main():
    game = GameWindow()
    game.setup()

    arcade.run()

if __name__ == "__main__":
    main()