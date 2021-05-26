"""
Module containing a number of different functions that will be used to facilitate various game tasks.
"""

import arcade
from arcade.sprite_list import SpriteList
from arcade.texture import Texture
from arcade.tilemap import process_layer, read_tmx

from ForestKnight.constants import TILE_SCALE
from ForestKnight.game_saving_utility import load_collectibles


def load_texture_pair(filename: str) -> list[Texture]:
    """Will load a pair of texture images, one flipped horizontally"""
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True),
    ]


def load_textures(filename: str, asset_count: int) -> list[Texture]:
    """
    Load bunch of pairs of textures using this function.
    Make sure to include "<asset_count>" in the filename to loop over
    """
    textures = []
    for count in range(1, asset_count + 1):
        new_filename = filename.replace("<asset_count>", str(count))
        texture = load_texture_pair(new_filename)
        textures.append(texture)

    return textures


def level_loader(
    level: int, collectibles_pos: list[tuple[float, float]]
) -> dict[str, SpriteList]:
    """
    A function that will load the given level from the base levels directory.
    It will return a dictionary of loaded layers of the given level
    Also, the function takes a list of tuples of the positions of the collectibles that shouldn't be loaded
    """
    level_name = f"levels/level{level}.tmx"

    platforms_layer_name = "Platforms"
    foreground_layer_name = "Foregrounds"
    background_layer_name = "Backgrounds"
    ladders_layer_name = "Ladders"
    dont_touch_layer_name = "Don't-Touch"
    collectibles_layer_name = "Collectibles"

    level = read_tmx(level_name)

    # Setting up Platforms layer
    platforms = process_layer(
        map_object=level,
        layer_name=platforms_layer_name,
        scaling=TILE_SCALE,
        use_spatial_hash=True,
    )

    # Setting up Foregrounds layer
    foregrounds = process_layer(
        map_object=level,
        layer_name=foreground_layer_name,
        scaling=TILE_SCALE,
        use_spatial_hash=True,
    )

    # Setting up Backgrounds layer
    backgrounds = process_layer(
        map_object=level,
        layer_name=background_layer_name,
        scaling=TILE_SCALE,
        use_spatial_hash=True,
    )

    # Setting up Ladders layer
    ladders = process_layer(
        map_object=level,
        layer_name=ladders_layer_name,
        scaling=TILE_SCALE,
        use_spatial_hash=True,
    )
    # Setting up Dont-Touch layer
    dont_touch = process_layer(
        map_object=level,
        layer_name=dont_touch_layer_name,
        scaling=TILE_SCALE,
        use_spatial_hash=True,
    )

    # Setting up the Collectibles layer
    collectibles = process_layer(
        map_object=level,
        layer_name=collectibles_layer_name,
        scaling=TILE_SCALE,
        use_spatial_hash=True,
    )

    collectibles = load_collectibles(collectibles, collectibles_pos)

    loaded_layers_dict = {
        "Platforms": platforms,
        "Foregrounds": foregrounds,
        "Backgrounds": backgrounds,
        "Ladders": ladders,
        "Dont-Touch": dont_touch,
        "Collectibles": collectibles,
    }

    return loaded_layers_dict
