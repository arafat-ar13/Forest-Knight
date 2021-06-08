""" 
Python file containing some basic information about the game
"""

import sys

import arcade

GAME_TITLE = "Forest Knight"
DEVELOPER = "Arafat Khan"
GAME_STAGE = "Beta"
GAME_VERSION = "0.7.95"
ARCADE_VERSION = arcade.__version__
PYTHON_VERSION = sys.version
LAST_COMMIT = "June 9th, 2021"


def print_game_info():
    """
    Function that prints basic information about the game to the terminal.
    """

    print("\n")
    print("Welcome to Forest Knight!")
    print(f"Game version running: {GAME_VERSION}")
    print(f"Game is current in {GAME_STAGE} stages")
    print(f"Arcade version: {ARCADE_VERSION}")
    print(f"Python version: {PYTHON_VERSION}")
    print(f"Game is made by {DEVELOPER}")
    print(f"Code was last committed to GitHub: {LAST_COMMIT}")
    print("\n")
