""" Module containing a number of different functions """

import arcade


def load_texture_pair(filename):
    """Will load a pair of texture images, one flipped horizontally"""
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True),
    ]


def load_textures(filename, asset_count):
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
