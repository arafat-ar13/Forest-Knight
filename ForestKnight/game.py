import os

import arcade

from characters.player.knight import Knight
from constants import *
from level_loader import level_loader


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)

        # Player sprite
        self.player_list = None
        self.player = None

        # Other sprites
        self.platforms = None
        self.foregrounds = None
        self.backgrounds = None
        self.ladders = None
        self.dont_touch = None

        # Sounds
        self.background_music = None

        # Background_image
        self.background_image = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Our simple Physics Engine
        self.physics_engine = None

    def setup(self, level):
        """ 
        Method that takes a level number and tries to load it
        This method also is used for setting up the game quickly and efficiently
        """

        # Setting up Player sprite
        self.player_list = arcade.SpriteList()
        self.player = Knight()
        self.player_list.append(self.player)

        # Setting up other sprites
        loaded_sprites = level_loader(level)

        self.platforms = loaded_sprites["Platforms"]
        self.foregrounds = loaded_sprites["Foregrounds"]
        self.backgrounds = loaded_sprites["Backgrounds"]
        self.ladders = loaded_sprites["Ladders"]
        self.dont_touch = loaded_sprites["Dont-Touch"]

        # Loading and playing our background music
        self.background_music = arcade.load_sound(f"{AUDIO_DIR}/backgroundMusic2.mp3")
        self.background_music.play(volume=0.05)

        # Loading and setting our background image for specified level
        if level == 1:
            self.background_image = arcade.load_texture(f"{IMAGES_DIR}/backgrounds/BG.png")

        # Setting up the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.platforms, gravity_constant=GRAVITY, ladders=self.ladders)

    def on_key_press(self, key, modifiers):
        """ Controls player movement when a key is pressed """
        if key == arcade.key.W or key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player.change_y = KNIGHT_JUMP_SPEED
                self.player.jump_sound.play()
            elif self.physics_engine.is_on_ladder():
                self.player.change_y = KNIGHT_SPEED
        elif key == arcade.key.S or key == arcade.key.DOWN:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = -KNIGHT_SPEED
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.player.change_x = KNIGHT_SPEED
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.player.change_x = -KNIGHT_SPEED
        elif key == arcade.key.SPACE:
            self.player.is_attacking = True

    def on_key_release(self, key, modifiers):
        """ Stops the player's movement when a key is released """
        if key == arcade.key.W or key == arcade.key.UP:
            self.player.change_y = 0
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.player.change_x = 0
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.player.change_x = 0
        elif key == arcade.key.SPACE:
            self.player.is_attacking = False

    def on_update(self, dt):
        """ Contains all the game loop and logic code """
        self.physics_engine.update()
        self.player.update_animation()

        # Has our background music ended? Well, play it again duh
        if self.background_music.get_stream_position() == 0:
            self.background_music.play()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport
        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def on_draw(self):
        arcade.start_render()

        # Drawing our loaded background images and setting it
        arcade.draw_texture_rectangle((SCREEN_WIDTH // 2) + self.view_left, (SCREEN_HEIGHT // 2) + self.view_bottom,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background_image)

        self.platforms.draw()
        self.backgrounds.draw()
        self.ladders.draw()
        self.player_list.draw()
        self.dont_touch.draw()
        self.foregrounds.draw()
