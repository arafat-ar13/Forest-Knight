"""Module that contains the GUI elements used in the game"""

import webbrowser

import arcade
from arcade.gui.elements.image_button import UIImageButton
from arcade.gui.elements.label import UILabel


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

    def on_click(self):
        """ 
        When this button is pressed, show the view that was passed during initialization 
        """
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
