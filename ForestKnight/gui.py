"""Module that contains the GUI elements used in the game"""

import webbrowser

import arcade
from arcade.gui.elements.image_button import UIImageButton
from arcade.gui.elements.label import UILabel

from ForestKnight.game_saving_utility import new_game, save_game


class ViewChangingButton(UIImageButton):
    """
    Custom Button implemented inherited from `arcade.gui.elements.image_button.UIImageButton`.
    This Button will take a number of arguments like what the next view is, the game view and the window
    and then switch to the next view.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scale = 0.5

        self.onclick_view: arcade.View = kwargs.get("onclick_view")
        self.game_view: arcade.View = kwargs.get("game_view")
        self.window: arcade.Window = kwargs.get("window")

        self.new_game: bool = kwargs.get("new_game")

        self.delete_sprites: bool = kwargs.get("delete_sprites")

    def on_click(self):
        """
        When this button is pressed, show the view that was passed during initialization
        """

        if self.new_game:
            new_game()

        if self.delete_sprites:
            self.game_view.delete_all_sprites()

        view = self.onclick_view(self.game_view, self.window)
        self.window.show_view(view)

        return super().on_click()


class LinkButton(UIImageButton):
    """Button that will open a link when pressed"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.link = kwargs.get("link")
        self.scale = 0.5

    def on_click(self):
        webbrowser.open(self.link)

        return super().on_click()


class GameSavingButton(UIImageButton):
    """Button that is used to save the game state"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.game_view: arcade.View = kwargs.get("game_view")
        self.viewport_coords = kwargs.get("viewport_coords")

    def on_click(self):
        """Save the game state to the hard disk"""

        level = self.game_view.level
        health = self.game_view.knight.health
        score = self.game_view.knight.score
        pos = self.game_view.knight.position
        cur_texture = self.game_view.knight.texture
        knight_state = self.game_view.knight.state
        collectibles_to_omit = self.game_view.collectibles_to_omit
        viewport_coords = self.viewport_coords

        data_dict = {
            "level": level,
            "health": health,
            "score": score,
            "position": pos,
            "texture": cur_texture,
            "knight_state": knight_state,
            "collectibles_to_omit": collectibles_to_omit,
            "viewport_coords": viewport_coords,
        }

        # Calling function from gave saving utility
        save_game(data=data_dict)

        return super().on_click()


class Label(UILabel):
    """
    Displays label on the screen
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.color = kwargs.get("color")
        self.on_top_of_button: bool = kwargs.get("on_top_of_button")
        self.parent_button: UIImageButton = kwargs.get("parent_button")

    def on_click(self):

        # If this label is on top of a button, call the button's `on_click` method instead
        # Parent button's `on_click` method will not be called if `on_top_of_button` is false
        if self.on_top_of_button:
            self.parent_button.on_click()

        return super().on_click()


class ExitButton(UIImageButton):
    """
    Button for exiting the game
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_click(self):
        """Exit the game and close the window"""

        arcade.close_window()

        return super().on_click()
