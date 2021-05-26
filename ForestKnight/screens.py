"""
This file contains all the code that is needed for all the different screens used in the game.
Currently the screens are:

Title View that appears first in the game
Instructions View that comes up when 'I' is pressed from the Title View
Pause View that comes up by pressing P when the game is actually being played
Loading View that shows up whenever a significant amount of time is taken to make computations

KnightForestView is the only exception screen that is not located here and is in the the game.py file 
"""

import arcade
from arcade.draw_commands import draw_lrtb_rectangle_filled
from arcade.texture import load_texture
from arcade.window_commands import start_render

from ForestKnight.constants import IMAGES_DIR, SCREEN_HEIGHT, SCREEN_WIDTH
from ForestKnight.game_saving_utility import create_data_dir, load_game


def load_game_screen(window: arcade.Window, game_view: arcade.View):
    gameview = game_view
    # Checking if the data directory exists or not. If not, create one
    create_data_dir()

    # Trying to load from a save file
    loaded_data = load_game()
    try:
        # Since 'level' is always saved we try to retrive it first
        level = loaded_data["level"]
        first_time = False
    except:
        # If we're unable to retrieve it, it means the game is being run for the first time
        level = 1
        first_time = True

    if first_time:
        gameview.setup(level=level)
        print("Game running for the first time")
    else:
        gameview.setup(level=level, load_game=True, loaded_game_data=loaded_data)

    window.show_view(gameview)


class TitleView(arcade.View):
    """
    Displays a title screen and prompts the user to begin the game.
    Provides a way to show instructions and start the game.
    """

    def __init__(self, game_view: arcade.View):
        super().__init__()

        self.game_view = game_view

        self.background = load_texture(
            f"{IMAGES_DIR}/backgrounds/backgroundColorGrass.png"
        )
        self.play_button = load_texture(f"{IMAGES_DIR}/gui/play_button.png")

        # Set our display timer
        self.display_timer = 2.0

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
            loading_view = LoadingView(self.window, self.game_view)
            self.window.show_view(loading_view)

        elif symbol == arcade.key.I:
            instructions_view = InstructionsView(self.game_view)
            self.window.show_view(instructions_view)

        return super().on_key_press(symbol, modifiers)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(
            (SCREEN_WIDTH // 2),
            (SCREEN_HEIGHT // 2),
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.background,
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


class InstructionsView(arcade.View):
    def __init__(self, game_view: arcade.View):
        super().__init__()

        self.game_view = game_view

        # Setting up button textures
        self.up_button = load_texture(f"{IMAGES_DIR}/gui/up_button.png")
        self.right_button = load_texture(f"{IMAGES_DIR}/gui/right_button.png")
        self.left_button = load_texture(f"{IMAGES_DIR}/gui/left_button.png")
        self.space_bar = load_texture(f"{IMAGES_DIR}/gui/space_bar.png")

        self.background = load_texture(
            f"{IMAGES_DIR}/backgrounds/backgroundColorGrass.png"
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            title_view = TitleView(self.game_view)
            self.window.show_view(title_view)

        return super().on_key_press(symbol, modifiers)

    def on_draw(self):
        start_render()

        # Drawing the background image
        arcade.draw_texture_rectangle(
            (SCREEN_WIDTH // 2),
            (SCREEN_HEIGHT // 2),
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.background,
        )

        # Drawing Instructions for Knight Movement and Jump
        arcade.draw_text(
            "Knight Movement and Jump",
            start_x=25,
            start_y=550,
            color=arcade.color.CHINESE_VIOLET,
            font_size=20,
        )
        arcade.draw_texture_rectangle(
            center_x=165, center_y=450, width=50, height=50, texture=self.right_button
        )  # Right arrow
        arcade.draw_texture_rectangle(
            center_x=140, center_y=500, width=50, height=50, texture=self.up_button
        )  # Up arrow
        arcade.draw_texture_rectangle(
            center_x=115, center_y=450, width=50, height=50, texture=self.left_button
        )  # Left arrow

        # Drawing instructions for Knight's attack
        arcade.draw_text(
            "Attack enemies",
            start_x=780,
            start_y=550,
            color=arcade.color.CHINESE_VIOLET,
            font_size=20,
        )
        arcade.draw_texture_rectangle(
            center_x=855, center_y=480, width=100, height=50, texture=self.space_bar
        )  # Space Bar

        # Go back to Title Screen
        arcade.draw_text(
            "Press Esc to go back",
            start_x=320,
            start_y=20,
            color=arcade.color.CHINESE_VIOLET,
            font_size=35,
        )

        return super().on_draw()


class PauseView(arcade.View):
    def __init__(self, game_view: arcade.View):
        super().__init__()

        self.game_view = game_view

        # Store a semitransparent color to use as an overlay
        self.fill_color = arcade.make_transparent_color(
            arcade.color.WHITE, transparency=150
        )

    def on_draw(self):

        self.game_view.on_draw()

        # Now create a filled rect that covers the current viewport
        # We get the viewport size from the game view
        draw_lrtb_rectangle_filled(
            left=self.game_view.view_left,
            right=self.game_view.view_left + SCREEN_WIDTH,
            top=self.game_view.view_bottom + SCREEN_HEIGHT,
            bottom=self.game_view.view_bottom,
            color=self.fill_color,
        )

        # Now show the Pause text
        arcade.draw_text(
            "PAUSED P TO CONTINUE",
            start_x=self.game_view.view_left + 180,
            start_y=self.game_view.view_bottom + 300,
            color=arcade.color.INDIGO,
            font_size=40,
        )

        return super().on_draw()

    def on_key_press(self, symbol, modifiers):

        if symbol == arcade.key.P:
            self.game_view.knight.change_x = 0
            self.game_view.knight.change_y = 0
            self.window.show_view(self.game_view)

        return super().on_key_press(symbol, modifiers)


class LoadingView(arcade.View):
    def __init__(self, window: arcade.Window, game_view: arcade.View):
        super().__init__()

        self.window = window
        self.game_view = game_view

        self.timer = 0.1
        self.should_update = True

    def on_draw(self):

        start_render()

        arcade.draw_text(
            "Loading...",
            start_x=385,
            start_y=300,
            color=arcade.color.BLUE_SAPPHIRE,
            font_size=50,
        )

        return super().on_draw()

    def on_update(self, delta_time):
        if self.should_update:
            self.timer -= delta_time

            if self.timer < 0:
                load_game_screen(self.window, self.game_view)
                self.should_update = False

        return super().on_update(delta_time)
