import sys

import arcade
from arcade.window_commands import run

from ForestKnight.game import ForestKnight
from ForestKnight.game_saving_utility import create_data_dir, load_game


def print_game_info():
    game_version = "0.5"
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

    # Checking if the data directory exists or not. If not, create one
    create_data_dir()

    # Trying to load from a save file
    loaded_data = load_game()
    try:
        # Since 'level' is always saved we try to retrive it first
        level = loaded_data["level"]
        first_time = False
    except:
        # If we're unable to retrieve it, it means the game is being run for the first time
        level = 1
        first_time = True

    if first_time:
        game.setup(level=level)
        print("Game running for the first time")
    else:
        game.setup(level=level, load_game=True, loaded_game_data=loaded_data)

    run()


if __name__ == "__main__":
    print_game_info()
    main()
