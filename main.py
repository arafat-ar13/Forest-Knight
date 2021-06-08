"""
Welcome to Forest Knight! Fight through horrific enemies while collection coins!
This file is capable to running the entire game. Just run this file to start the game
"""

import arcade
from arcade.window_commands import run

from ForestKnight.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from ForestKnight.game import ForestKnightView
from ForestKnight.game_details import GAME_TITLE, print_game_info
from ForestKnight.screens import TitleView


def main():
    window = arcade.Window(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=GAME_TITLE)
    game = ForestKnightView()
    title_view = TitleView(game)
    window.show_view(title_view)

    run()


if __name__ == "__main__":
    print_game_info()
    main()
