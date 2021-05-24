"""Code that defines the title view"""
import arcade
from arcade.texture import load_texture
from ForestKnight.constants import IMAGES_DIR, SCREEN_HEIGHT, SCREEN_WIDTH
from ForestKnight.screens.handle_screens import (
    load_game_screen,
    load_instructions_screen,
)


class TitleView(arcade.View):
    """
    Displays a title screen and prompts the user to begin the game.
    Provides a way to show instructions and start the game.
    """

    def __init__(self):
        super().__init__()

        self.title_image = load_texture(
            f"{IMAGES_DIR}/backgrounds/backgroundColorGrass.png"
        )
        self.play_button = load_texture(f"{IMAGES_DIR}/gui/play_button.png")

        # Set our display timer
        self.display_timer = 3.0

        # Options to start game or show instructions
        self.show_start_game = False
        self.show_instructions = False

    def on_show(self):
        """This is run once when we switch to this view"""

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        return super().on_show()

    def on_update(self, delta_time):
        # First, count down the time
        self.display_timer -= delta_time

        # If the timer has run out, we toggle the instructions and 'start game'
        if self.display_timer < 0:
            self.show_start_game = (
                not self.show_start_game
            )  # Toggle whether to show the 'start game' option
            self.show_instructions = (
                not self.show_instructions
            )  # Toggle whether to show the instructions option
            self.display_timer = (
                1.0  # And reset the timer so the instructions flash slowly
            )

        return super().on_update(delta_time)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            load_game_screen(self.window)

        elif symbol == arcade.key.I:
            load_instructions_screen(self.window)

        return super().on_key_press(symbol, modifiers)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(
            (SCREEN_WIDTH // 2),
            (SCREEN_HEIGHT // 2),
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.title_image,
        )

        arcade.draw_text(
            "Welcome to Forest Knight",
            start_x=SCREEN_WIDTH // 2,
            start_y=SCREEN_HEIGHT // 2,
            color=arcade.color.CHINESE_VIOLET,
            font_size=50,
            anchor_x="center",
        )

        if self.show_start_game:
            arcade.draw_text(
                "Enter to Start Game",
                start_x=SCREEN_WIDTH // 2,
                start_y=220,
                color=arcade.color.INDIGO,
                font_size=40,
                anchor_x="center",
            )

        if self.show_instructions:
            arcade.draw_text(
                "Press 'I' for instructions",
                start_x=SCREEN_WIDTH // 2,
                start_y=150,
                color=arcade.color.INDIGO,
                font_size=40,
                anchor_x="center",
            )

        return super().on_draw()
