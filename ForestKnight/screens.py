"""
This file contains all the code that is needed for all the different screens used in the game.
KnightForestView is the only exception screen that is not located here and is in the the game.py file 
"""

import arcade
import arcade.gui
from arcade.draw_commands import draw_lrtb_rectangle_filled
from arcade.gui import UIManager
from arcade.texture import load_texture
from arcade.window_commands import start_render

from ForestKnight.constants import FONTS_DIR, GAME_VERSION, IMAGES_DIR, SCREEN_HEIGHT, SCREEN_WIDTH
from ForestKnight.game_saving_utility import create_data_dir, load_game
from ForestKnight.gui import Button, Label


def load_game_screen(window: arcade.Window, game_view: arcade.View):
    """
    Function that loads the actual game screen after reading available data from the saved file
    """
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

    def __init__(self, game_view: arcade.View, *args):
        super().__init__()

        self.game_view = game_view

        # Initializing UI Manager
        self.ui_manager = UIManager()

        self.background = load_texture(
            f"{IMAGES_DIR}/backgrounds/backgroundColorForest.png"
        )
        self.play_button = load_texture(f"{IMAGES_DIR}/gui/play_button.png")

    def on_show(self):
        """This is run once when we switch to this view"""

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        self.ui_manager.purge_ui_elements()

        # Adding 'Game Start' button
        start_button = load_texture(f"{IMAGES_DIR}/gui/lime_button.png")
        button = Button(
            center_x=SCREEN_WIDTH // 2,
            center_y=280,
            normal_texture=start_button,
            onclick_view=LoadingView,
            game_view=self.game_view,
            window=self.window,
        )
        self.ui_manager.add_ui_element(button)

        # Adding 'Game Start' label
        label = Label(
            "Start Game",
            center_x=SCREEN_WIDTH // 2,
            center_y=280,
            color=arcade.color.FIRE_ENGINE_RED,
            parent_button=button,
        )
        self.ui_manager.add_ui_element(label)

        # Adding 'Instructions' button
        instructions_button = load_texture(f"{IMAGES_DIR}/gui/lime_button.png")
        button = Button(
            center_x=SCREEN_WIDTH // 2,
            center_y=190,
            normal_texture=instructions_button,
            onclick_view=InstructionsView,
            game_view=self.game_view,
            window=self.window,
        )
        self.ui_manager.add_ui_element(button)

        # Adding 'Instructions' label
        label = Label(
            "Instructions",
            center_x=SCREEN_WIDTH // 2,
            center_y=190,
            color=arcade.color.FIRE_ENGINE_RED,
            parent_button=button,
        )
        self.ui_manager.add_ui_element(label)

        return super().on_show()

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

        return super().on_hide_view()

    def on_draw(self):
        """Draw anything on the screen"""
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
            start_y=SCREEN_HEIGHT - 100,
            color=arcade.color.CHINESE_VIOLET,
            font_name=f"{FONTS_DIR}/WarPriestRegular.ttf",
            font_size=50,
            anchor_x="center",
        )

        # Drawing game version
        arcade.draw_text(
            f"Version: {GAME_VERSION}",
            start_x=20,
            start_y=20,
            font_name=f"{FONTS_DIR}/Wooden Log.ttf",
            font_size=20,
            color=arcade.color.ELECTRIC_GREEN,
        )

        return super().on_draw()


class InstructionsView(arcade.View):
    """
    The view that shows all the ways this game can be played
    and what keys are required to do different operatoins
    """

    def __init__(self, game_view: arcade.View, *args):
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

    def on_key_press(self, symbol: int, modifiers: int):
        """
        Code that allows escaping from the Instructions View when the Escape key is pressed
        """
        if symbol == arcade.key.ESCAPE:
            title_view = TitleView(self.game_view)
            self.window.show_view(title_view)

        return super().on_key_press(symbol, modifiers)

    def on_draw(self):
        """Draw instructions on the screen"""
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
    """
    View that shows up only in `ForestKnightView` to pause the game when 'P' is pressed
    """

    def __init__(self, game_view: arcade.View):
        super().__init__()

        self.game_view = game_view

        # Store a semitransparent color to use as an overlay
        self.fill_color = arcade.make_transparent_color(
            arcade.color.WHITE, transparency=150
        )

    def on_draw(self):
        """Draw the 'Paused' text on the screen"""

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
        """Switch off PauseView by again pressing 'P'"""

        if symbol == arcade.key.P:
            self.game_view.knight.change_x = 0
            self.game_view.knight.change_y = 0
            self.window.show_view(self.game_view)

        return super().on_key_press(symbol, modifiers)


class LoadingView(arcade.View):
    """
    Loading View that shows up whenever a significant amount of time is taken to make computations
    """

    def __init__(self, game_view: arcade.View, window: arcade.Window):
        super().__init__()

        self.game_view = game_view
        self.window = window

        self.timer = 0.1
        self.should_update = True

    def on_draw(self):
        """Draw the loading text on the screen"""

        start_render()

        arcade.draw_text(
            "Loading...",
            start_x=385,
            start_y=300,
            color=arcade.color.BLUE_SAPPHIRE,
            font_size=50,
        )

        return super().on_draw()

    def on_update(self, delta_time: float):
        """Wait a tiny bit of time before proceeding to the next view"""

        if self.should_update:
            self.timer -= delta_time

            if self.timer < 0:
                load_game_screen(self.window, self.game_view)
                self.should_update = False

        return super().on_update(delta_time)
