import arcade

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
os.chdir(BASE_DIR)

from game import GameWindow

def main():
    game = GameWindow()
    game.setup(1)

    arcade.run()


if __name__ == "__main__":
    main()
