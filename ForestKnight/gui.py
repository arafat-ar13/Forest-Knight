import arcade
from arcade.gui.elements.image_button import UIImageButton
from arcade.gui.elements.label import UILabel


class Button(UIImageButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scale = 0.5

        self.onclick_view: arcade.View = kwargs.get("onclick_view")
        self.game_view: arcade.View = kwargs.get("game_view")
        self.window: arcade.Window = kwargs.get("window")

    def on_click(self):
        view = self.onclick_view(self.game_view, self.window)
        self.window.show_view(view)

        return super().on_click()


class Label(UILabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.color = kwargs.get("color")
        self.parent_button: Button = kwargs.get("parent_button")

    def on_click(self):
        self.parent_button.on_click()

        return super().on_click()
