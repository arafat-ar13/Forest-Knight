"""
Welcome to Forest Knight! Fight through horrific enemies while collection coins!
This file is capable to running the entire game. Just run this file to start the game
"""

import sys

import arcade
from arcade.window_commands import run

from ForestKnight.constants import GAME_TITLE, SCREEN_HEIGHT, SCREEN_WIDTH
from ForestKnight.game import ForestKnightView
from ForestKnight.screens import TitleView


def print_game_info():
    """
    Function that prints basic information about the game to the terminal.
    It's terminal-based for now. The information may be displayed directly inside the game GUI in the future.
    """
    game_version = "0.7.5"
    game_state = "Alpha"
    arcade_version = arcade.__version__
    python_version = sys.version
    developer = "Arafat Khan"
    last_commit = "May 29th, 2021"

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
