import sys

import arcade
from arcade.window_commands import run

from ForestKnight.game import ForestKnight


def print_game_info():
    game_version = "0.3"
    game_state = "Alpha"
    arcade_version = arcade.__version__
    python_version = sys.version
    developer = "Arafat Khan"
    last_commit = "May 22nd, 2021"

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
    game = ForestKnight()
    game.setup()
    run()


if __name__ == "__main__":
    print_game_info()
    main()
