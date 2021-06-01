"""
This file contains all the code that is needed for all the different screens used in the game.
KnightForestView is the only exception screen that is not located here and is in the the game.py file 
"""

import arcade
import arcade.gui
from arcade.draw_commands import draw_lrtb_rectangle_filled
from arcade.gui import UIManager
from arcade.gui.elements.image_button import UIImageButton
from arcade.texture import load_texture
from arcade.window_commands import start_render

from ForestKnight.constants import (
    DEVELOPER,
    FONTS_DIR,
    GAME_VERSION,
    IMAGES_DIR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from ForestKnight.game_saving_utility import create_data_dir, load_game
from ForestKnight.gui import Label, LinkButton, ViewChangingButton


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


class View(arcade.View):
    """Custom `arcade.View` subclass that will contain commonly used attributes. Inherit from this to access them."""

    def __init__(self):
        super().__init__()

        # Initializing UI Manager
        self.ui_manager = UIManager()

        # Setting up button textures
        self.up_button = load_texture(f"{IMAGES_DIR}/gui/up_button.png")
        self.down_button = load_texture(f"{IMAGES_DIR}/gui/down_button.png")
        self.right_button = load_texture(f"{IMAGES_DIR}/gui/right_button.png")
        self.left_button = load_texture(f"{IMAGES_DIR}/gui/left_button.png")
        self.space_bar = load_texture(f"{IMAGES_DIR}/gui/space_bar.png")
        self.lime_button = load_texture(f"{IMAGES_DIR}/gui/lime_button.png")

        # Setting up 'unpressed' textures of those buttons
        self.up_button_unpressed = load_texture(
            f"{IMAGES_DIR}/gui/up_button_unpressed.png"
        )
        self.down_button_unpressed = load_texture(
            f"{IMAGES_DIR}/gui/down_button_unpressed.png"
        )
        self.right_button_unpressed = load_texture(
            f"{IMAGES_DIR}/gui/right_button_unpressed.png"
        )
        self.left_button_unpressed = load_texture(
            f"{IMAGES_DIR}/gui/left_button_unpressed.png"
        )
        self.space_bar_unpressed = load_texture(
            f"{IMAGES_DIR}/gui/space_bar_unpressed.png"
        )

        # Setting up our background
        self.background = load_texture(
            f"{IMAGES_DIR}/backgrounds/backgroundColorForest.png"
        )

    def on_show(self):
        """This is run once when we switch to this view"""

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        return super().on_show()

    def on_hide_view(self):
        """This in run once when we move away from this view"""

        self.ui_manager.unregister_handlers()

        return super().on_hide_view()


class TitleView(View):
    """
    Displays a title screen and prompts the user to begin the game.
    Provides a way to show instructions, credits and start the game.
    """

    def __init__(self, game_view: arcade.View, *args):
        super().__init__()

        self.game_view = game_view

    def on_show(self):
        self.ui_manager.purge_ui_elements()

        # Adding 'Game Start' button
        start_button = self.lime_button
        button = ViewChangingButton(
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
            on_top_of_button=True,
            parent_button=button,
        )
        self.ui_manager.add_ui_element(label)

        # Adding 'Instructions' button
        instructions_button = self.lime_button
        button = ViewChangingButton(
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
            on_top_of_button=True,
            parent_button=button,
        )
        self.ui_manager.add_ui_element(label)

        # Adding 'Credits' button
        credits_button = self.lime_button
        button = ViewChangingButton(
            center_x=SCREEN_WIDTH // 2,
            center_y=100,
            normal_texture=credits_button,
            onclick_view=CreditsView,
            game_view=self.game_view,
            window=self.window,
        )
        self.ui_manager.add_ui_element(button)

        # Adding 'Credits' label
        label = Label(
            "Credits",
            center_x=SCREEN_WIDTH // 2,
            center_y=100,
            color=arcade.color.FIRE_ENGINE_RED,
            on_top_of_button=True,
            parent_button=button,
        )
        self.ui_manager.add_ui_element(label)

        return super().on_show()

    def on_draw(self):
        """Draw anything on the screen"""
        start_render()

        arcade.draw_texture_rectangle(
            (SCREEN_WIDTH // 2),
            (SCREEN_HEIGHT // 2),
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.background,
        )

        # Drawing game name
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


class InstructionsView(View):
    """
    The view that shows all the ways this game can be played
    and what keys are required to do different operatoins
    """

    def __init__(self, game_view: arcade.View, *args):
        super().__init__()

        self.game_view = game_view

        # Store a semitransparent color to use as an overlay
        self.fill_color = arcade.make_transparent_color(
            arcade.color.WHITE, transparency=150
        )

    def on_show(self):
        """Code that is run when this view is activated"""

        # Adding a 'back button' that allows to close this view
        back_button = self.left_button
        button = ViewChangingButton(
            center_x=50,
            center_y=50,
            normal_texture=back_button,
            onclick_view=TitleView,
            game_view=self.game_view,
            window=self.window,
            width=50,
            height=50,
        )
        self.ui_manager.add_ui_element(button)

        # Creating a dictionary of the four arrow keys so that they can be created easily with a loop
        self.movement_butts: dict[int, dict] = {
            arcade.key.UP: {
                "normal_texture": self.up_button_unpressed,
                "hovered_texture": self.up_button,
                "coords": (210, 480),
            },
            arcade.key.DOWN: {
                "normal_texture": self.down_button_unpressed,
                "hovered_texture": self.down_button,
                "coords": (210, 380),
            },
            arcade.key.LEFT: {
                "normal_texture": self.left_button_unpressed,
                "hovered_texture": self.left_button,
                "coords": (110, 380),
            },
            arcade.key.RIGHT: {
                "normal_texture": self.right_button_unpressed,
                "hovered_texture": self.right_button,
                "coords": (310, 380),
            },
        }

        self.butt_dict = {}

        for butt_type in self.movement_butts.keys():
            button = UIImageButton(
                normal_texture=self.movement_butts.get(butt_type).get("normal_texture"),
                hover_texture=self.movement_butts.get(butt_type).get("hovered_texture"),
                center_x=self.movement_butts.get(butt_type).get("coords")[0],
                center_y=self.movement_butts.get(butt_type).get("coords")[1],
            )
            button.scale = 0.5
            self.butt_dict[butt_type] = button
            self.ui_manager.add_ui_element(button)

        space_bar = UIImageButton(
            normal_texture=self.space_bar_unpressed,
            hover_texture=self.space_bar,
            center_x=780,
            center_y=420,
        )
        space_bar.scale = 0.5
        self.butt_dict[arcade.key.SPACE] = space_bar
        self.ui_manager.add_ui_element(space_bar)

        return super().on_show()

    def on_key_press(self, symbol: int, modifiers: int):
        """Illuminate each button when the corresponding arrow key is pressed"""
        for butt_type in self.movement_butts.keys():
            if symbol == butt_type:
                butt: UIImageButton = self.butt_dict.get(butt_type)
                butt.on_hover()

        if symbol == arcade.key.SPACE:
            butt: UIImageButton = self.butt_dict.get(symbol)
            butt.on_hover()

        return super().on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        """Stop illuminating the button when the corresponding arrow key is released"""
        for butt_type in self.movement_butts.keys():
            if symbol == butt_type:
                butt: UIImageButton = self.butt_dict.get(butt_type)
                butt.on_unhover()

        if symbol == arcade.key.SPACE:
            butt: UIImageButton = self.butt_dict.get(symbol)
            butt.on_unhover()

        return super().on_key_release(symbol, modifiers)

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

        # Blur the background
        draw_lrtb_rectangle_filled(
            left=self.game_view.view_left,
            right=self.game_view.view_left + SCREEN_WIDTH,
            top=self.game_view.view_bottom + SCREEN_HEIGHT,
            bottom=self.game_view.view_bottom,
            color=self.fill_color,
        )

        # Drawing Instructions for Knight Movement and Jump
        arcade.draw_text(
            "Knight Movement",
            start_x=25,
            start_y=550,
            color=arcade.color.CHINESE_VIOLET,
            font_size=50,
            font_name=f"{FONTS_DIR}/FirstJob.ttf",
        )

        # Drawing instructions for Knight's attack
        arcade.draw_text(
            "Knight Attack",
            start_x=580,
            start_y=550,
            color=arcade.color.CHINESE_VIOLET,
            font_size=50,
            font_name=f"{FONTS_DIR}/FirstJob.ttf",
        )

        # Drawing a small hint
        arcade.draw_text(
            "*Press corresponding keys to see some light",
            start_x=540,
            start_y=50,
            color=arcade.color.BLUE_SAPPHIRE,
            font_size=17,
            font_name=f"{FONTS_DIR}/Wooden Log.ttf",
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


class LoadingView(View):
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


class CreditsView(View):
    """
    View that gives information about who made the game and stuff like that
    """

    def __init__(self, game_view: arcade.View, *args):
        super().__init__()

        self.game_view = game_view

        self.python_logo = load_texture(f"{IMAGES_DIR}/python_powered.png")

        # Store a semitransparent color to use as an overlay
        self.fill_color = arcade.make_transparent_color(
            arcade.color.WHITE, transparency=150
        )

    def on_show(self):
        """Code that is run only once when this view is shown"""

        # Adding a 'back button' that allows to close this view
        back_button = self.left_button
        button = ViewChangingButton(
            center_x=50,
            center_y=50,
            normal_texture=back_button,
            onclick_view=TitleView,
            game_view=self.game_view,
            window=self.window,
            width=50,
            height=50,
        )
        self.ui_manager.add_ui_element(button)

        # Adding 'About Me' button
        about_me = self.lime_button
        button = LinkButton(
            center_x=(SCREEN_WIDTH // 2) - 150,
            center_y=(SCREEN_HEIGHT // 2) - 50,
            normal_texture=about_me,
            link="https://arafat-ar13.github.io",
        )
        self.ui_manager.add_ui_element(button)

        # Adding 'About Me' label
        label = Label(
            center_x=(SCREEN_WIDTH // 2) - 150,
            center_y=(SCREEN_HEIGHT // 2) - 50,
            text="About Me",
            on_top_of_button=True,
            parent_button=button,
            color=arcade.color.FIRE_ENGINE_RED,
        )
        self.ui_manager.add_ui_element(label)

        # Adding 'GitHub Repository' button
        github_repo = self.lime_button
        button = LinkButton(
            center_x=(SCREEN_WIDTH // 2) + 150,
            center_y=(SCREEN_HEIGHT // 2) - 50,
            normal_texture=github_repo,
            link="https://github.com/arafat-ar13/Forest-Knight",
        )
        self.ui_manager.add_ui_element(button)

        # Adding 'GitHub Repository' label
        label = Label(
            center_x=(SCREEN_WIDTH // 2) + 150,
            center_y=(SCREEN_HEIGHT // 2) - 50,
            text="Game Code",
            on_top_of_button=True,
            parent_button=button,
            color=arcade.color.FIRE_ENGINE_RED,
        )
        self.ui_manager.add_ui_element(label)

        # Adding a link to the Python official website with pride!
        python_button = LinkButton(
            center_x=(SCREEN_WIDTH // 2) - 200 + 580,
            center_y=(SCREEN_HEIGHT // 2) - 280,
            normal_texture=self.python_logo,
            link="https://python.org",
        )
        python_button.scale = 0.2
        self.ui_manager.add_ui_element(python_button)

        return super().on_show()

    def on_draw(self):
        """Draws anything to the screen"""
        start_render()

        # Drawing the background image
        arcade.draw_texture_rectangle(
            (SCREEN_WIDTH // 2),
            (SCREEN_HEIGHT // 2),
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.background,
        )

        # Blur the background
        draw_lrtb_rectangle_filled(
            left=self.game_view.view_left,
            right=self.game_view.view_left + SCREEN_WIDTH,
            top=self.game_view.view_bottom + SCREEN_HEIGHT,
            bottom=self.game_view.view_bottom,
            color=self.fill_color,
        )

        # --- Drawing our credits ---
        arcade.draw_text(
            f"Game Version: {GAME_VERSION}",
            start_x=(SCREEN_WIDTH // 2) - 150,
            start_y=(SCREEN_HEIGHT // 2) + 200,
            color=arcade.color.BRICK_RED,
            font_name=f"{FONTS_DIR}/FrostbiteBossFight.ttf",
            font_size=35,
        )

        arcade.draw_text(
            f"Game made by: {DEVELOPER}",
            start_x=(SCREEN_WIDTH // 2) - 250,
            start_y=(SCREEN_HEIGHT // 2) + 150,
            color=arcade.color.BRICK_RED,
            font_name=f"{FONTS_DIR}/FrostbiteBossFight.ttf",
            font_size=35,
        )

        arcade.draw_text(
            f"Game is made using the Python Arcade Library",
            start_x=(SCREEN_WIDTH // 2) - 350,
            start_y=(SCREEN_HEIGHT // 2) + 100,
            color=arcade.color.BRICK_RED,
            font_name=f"{FONTS_DIR}/FrostbiteBossFight.ttf",
            font_size=35,
        )

        return super().on_draw()
