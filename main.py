import sys

import arcade
from arcade.window_commands import run

from ForestKnight.constants import GAME_TITLE, SCREEN_HEIGHT, SCREEN_WIDTH
from ForestKnight.game import ForestKnightView
from ForestKnight.screens import TitleView


def print_game_info():
    game_version = "0.7"
    game_state = "Alpha"
    arcade_version = arcade.__version__
    python_version = sys.version
    developer = "Arafat Khan"
    last_commit = "May 27th, 2021"

    print("\n")
    print("Welcome to Forest Knight!")
    print(f"Game version running: {game_version}")
    print(f"Game is current in {game_state} stages")
    print(f"Arcade version: {arcade_version}")
    print(f"Python version: {python_version}")
    print(f"Game is made by {developer}")
    print(f"Code was last committed to GitHub: {last_commit}")
    print("\n")


def main():
    window = arcade.Window(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=GAME_TITLE)
    game = ForestKnightView()
    title_view = TitleView(game)
    window.show_view(title_view)

    run()


if __name__ == "__main__":
    print_game_info()
    main()
