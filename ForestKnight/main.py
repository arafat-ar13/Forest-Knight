import os
import sys

import arcade

import gamesaver
from game import ForestKnight

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
os.chdir(BASE_DIR)


def print_game_info():
    game_version = "0.5.1-beta"
    arcade_version = arcade.__version__
    python_version = sys.version
    developer = "Arafat Khan"
    last_commit = "September 12th, 2020"

    print("\n")
    print(f"Game version running: {game_version}")
    print(f"Arcade version: {arcade_version}")
    print(f"Python version: {python_version}")
    print(f"Game is made by {developer}")
    print(f"Code was last committed to GitHub: {last_commit}")
    print("\n")


def main():
    # Initialize the game
    game = ForestKnight()

    # Setting up the game with loaded and data
    gamesaver.create_data_dir()
    loaded_data = gamesaver.load_game()
    try:
        # Since 'level' is always, saved, if we're unable to retrieve it, then the game is being run for the first time
        level = loaded_data["level"]
        first_time = False
    except:
        level = 1
        first_time = True

    game.setup(level)

    if not first_time:
        # We actually want to load the game if this is not the first time
        game.load_game(loaded_data)

    arcade.run()


if __name__ == "__main__":
    print_game_info()
    main()
