import arcade

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
os.chdir(BASE_DIR)

from game import ForestKnight

def print_game_info():
    game_version = "0.3.1"
    arcade_version = arcade.__version__
    developer = "Arafat Khan"
    last_commit = "September 9th, 2020"

    print(f"Game version running: {game_version}")
    print(f"Arcade version: {arcade_version}")
    print("\n")
    print(f"Game is made by {developer}")
    print(f"Code was last committed to GitHub: {last_commit}")

def main():
    game = ForestKnight()
    game.setup(1)

    print_game_info()

    arcade.run()


if __name__ == "__main__":
    main()
