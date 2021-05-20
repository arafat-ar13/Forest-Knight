""" Module that loads a given level of the game"""

from ForestKnight.constants import TILE_SCALE
import arcade


def level_loader(level):
    """
    A function that will load the given level from the base levels directory.
    It will return a dictionary of loaded layers of the given level
    """
    level_name = f"levels/level{level}.tmx"

    platforms_layer_name = "Platforms"
    foreground_layer_name = "Foregrounds"
    background_layer_name = "Backgrounds"
    ladders_layer_name = "Ladders"
    dont_touch_layer_name = "Don't-Touch"
    collectibles_layer_name = "Collectibles"

    level = arcade.tilemap.read_tmx(level_name)

    # Setting up Platforms layer
    platforms = arcade.tilemap.process_layer(
        map_object=level,
        layer_name=platforms_layer_name,
        scaling=TILE_SCALE,
        use_spatial_hash=True,
    )

    # Setting up Foregrounds layer
    foregrounds = arcade.tilemap.process_layer(
        map_object=level,
        layer_name=foreground_layer_name,
        scaling=TILE_SCALE,
        use_spatial_hash=True,
    )

    # Setting up Backgrounds layer
    backgrounds = arcade.tilemap.process_layer(
        map_object=level,
        layer_name=background_layer_name,
        scaling=TILE_SCALE,
        use_spatial_hash=True,
    )

    # Setting up Ladders layer
    ladders = arcade.tilemap.process_layer(
        map_object=level,
        layer_name=ladders_layer_name,
        scaling=TILE_SCALE,
        use_spatial_hash=True,
    )
    # Setting up Dont-Touch layer
    dont_touch = arcade.tilemap.process_layer(
        map_object=level,
        layer_name=dont_touch_layer_name,
        scaling=TILE_SCALE,
        use_spatial_hash=True,
    )

    # Setting up the Collectibles layer
    collectibles = arcade.tilemap.process_layer(
        map_object=level,
        layer_name=collectibles_layer_name,
        scaling=TILE_SCALE,
        use_spatial_hash=True,
    )

    loaded_layers_dict = {
        "Platforms": platforms,
        "Foregrounds": foregrounds,
        "Backgrounds": backgrounds,
        "Ladders": ladders,
        "Dont-Touch": dont_touch,
        "Collectibles": collectibles,
    }

    return loaded_layers_dict
