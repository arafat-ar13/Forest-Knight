"""This module is the "Game Saving Utility" for this game"""

import os
import shelve

from ForestKnight.constants import SAVED_DATA_DIR


def create_data_dir():
    """Function to make sure that the saved data directory exists"""
    if not os.path.exists(f"{SAVED_DATA_DIR}/"):
        os.mkdir(f"{SAVED_DATA_DIR}/")


def save_game(data):
    """
    Send a dictionary of data to be saved. Like:
    data["level"] = 1
    data["knight_health"] = 35
    data["knight_position"] = (x_val, y_val)
    """
    saved_data = shelve.open(f"{SAVED_DATA_DIR}/saved_game_data")

    for key, value in data.items():
        saved_data[key] = value

    saved_data.close()

    print("Gave saved successfully!")


def load_game():
    """
    Function that will be called everytime before starting the game to load saved data
    """
    saved_data = shelve.open(f"{SAVED_DATA_DIR}/saved_game_data")

    loaded_data = {}

    for key, value in saved_data.items():
        loaded_data[key] = value

    saved_data.close()

    print("Game loaded successfully!")

    return loaded_data
