"""This module is the "Game Saving Utility" for this game"""

import os
import shelve
import shutil

import arcade
from arcade.sprite_list import SpriteList

from ForestKnight.constants import SAVED_DATA_DIR


def create_data_dir():
    """Function to make sure that the saved data directory exists"""
    if not os.path.exists(f"{SAVED_DATA_DIR}/"):
        os.mkdir(f"{SAVED_DATA_DIR}/")


def new_game() -> None:
    """
    Function that deletes existing save files and starts a new game
    """
    shutil.rmtree(f"{SAVED_DATA_DIR}/")

    print("Existing game data deleted")


def save_game(data: dict):
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


def load_game() -> dict:
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


def first_time() -> bool:
    """
    Function that checks if the game is being run for the first time or not
    """
    ft = True

    data = load_game()

    if os.path.exists(f"{SAVED_DATA_DIR}/"):
        if data.get("level") is not None:
            # Since 'level' is ALWAYS saved, if None is returned
            # it means that no save has yet been made and if None is
            # not returned, it means that saves have been made previously
            ft = False

    return ft


def load_game_screen(window: arcade.Window, gameview: arcade.View):
    """
    Function that loads the actual game screen after reading available data from the saved file
    """

    # Checking if the data directory exists or not. If not, create one
    create_data_dir()

    # Trying to load from a save file
    loaded_data = load_game()

    if first_time():
        level = 1
        gameview.setup(level=level)
        print("Game running for the first time")
    else:
        level = loaded_data.get("level")
        gameview.setup(level=level, load_game=True, loaded_game_data=loaded_data)

    window.show_view(gameview)


def load_collectibles(
    collectibles: SpriteList, collectibles_to_remove_pos: list[tuple[float, float]]
) -> SpriteList:
    """
    Function that will determine which collectibles (coins, flags, etc.) were already collected during previous gameplays.
    After that, it will remove them from the collectibles SpriteList so that they won't be drawn anymore
    and return a new SpriteList containing only the collectibles which are to be loaded
    """
    loaded_collectibles = SpriteList()

    if collectibles_to_remove_pos:
        for collectible in collectibles:
            if collectible.position not in collectibles_to_remove_pos:
                loaded_collectibles.append(collectible)
    else:
        loaded_collectibles = collectibles

    return loaded_collectibles
