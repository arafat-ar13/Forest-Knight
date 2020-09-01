""" Script that loads a given level of the game"""

import arcade

from constants import TILE_SCALE


def level_loader(level):
    """ 
    A function that will load the given level from the base levels directory.
    It will always return a list of 5 layers:
    Platforms
    Foregrounds
    Backgrounds
    Ladders
    Don't-Touch
    """
    level_name = f"levels/level{level}.tmx"

    platforms_layer_name = "Platforms"
    foreground_layer_name = "Foregrounds"
    background_layer_name = "Backgrounds"
    ladders_layer_name = "Ladders"
    dont_touch_layer_name = "Don't-Touch"

    level = arcade.tilemap.read_tmx(level_name)

    # Setting up Platforms layer
    platforms = arcade.tilemap.process_layer(map_object=level,
                                             layer_name=platforms_layer_name,
                                             scaling=TILE_SCALE,
                                             use_spatial_hash=True)

    # Setting up Foregrounds layer
    foregrounds = arcade.tilemap.process_layer(map_object=level,
                                               layer_name=foreground_layer_name,
                                               scaling=TILE_SCALE,
                                               use_spatial_hash=True)

    # Setting up Backgrounds layer
    backgrounds = arcade.tilemap.process_layer(map_object=level,
                                               layer_name=background_layer_name,
                                               scaling=TILE_SCALE,
                                               use_spatial_hash=True)

    # Setting up Ladders layer
    ladders = arcade.tilemap.process_layer(map_object=level,
                                           layer_name=ladders_layer_name,
                                           scaling=TILE_SCALE,
                                           use_spatial_hash=True)
    # Setting up Ladders layer
    dont_touch = arcade.tilemap.process_layer(map_object=level,
                                              layer_name=dont_touch_layer_name,
                                              scaling=TILE_SCALE,
                                              use_spatial_hash=True)

    return [platforms, foregrounds, backgrounds, ladders, dont_touch]
