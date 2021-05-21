import arcade
from arcade.physics_engines import PhysicsEnginePlatformer
from arcade.sound import load_sound
from arcade.sprite_list import SpriteList, check_for_collision_with_list
from arcade.window_commands import start_render

from ForestKnight.characters.player.knight import Knight
from ForestKnight.constants import (AUDIO_DIR, BOTTOM_VIEWPORT_MARGIN,
                                    GAME_TITLE, GRAVITY, IMAGES_DIR,
                                    KNIGHT_JUMP_SPEED, KNIGHT_SPEED,
                                    LEFT_VIEWPORT_MARGIN,
                                    RIGHT_VIEWPORT_MARGIN, SCREEN_HEIGHT,
                                    SCREEN_WIDTH, TOP_VIEWPORT_MARGIN)
from ForestKnight.helper_functions import level_loader


class ForestKnight(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
        self.character_sprites = SpriteList()

        self.setup_sprites()
        self.setup_characters()
        self.setup_physics_engine()
        self.setup_sounds()
        self.setup_images()

    def setup_sprites(self):
        """ Method that sets up all the Sprites (except for Player and Enemies) """
        loaded_sprites = level_loader(1)

        self.platforms = loaded_sprites["Platforms"]
        self.foregrounds = loaded_sprites["Foregrounds"]
        self.backgrounds = loaded_sprites["Backgrounds"]
        self.ladders = loaded_sprites["Ladders"]
        self.dont_touch = loaded_sprites["Dont-Touch"]
        self.collectibles = loaded_sprites["Collectibles"]

    def setup_characters(self):
        """ Method to set up the Knight and other Enemies """
        self.knight = Knight()
        self.character_sprites.append(self.knight)
        self.character_sprites.preload_textures(self.knight.textures)

    def setup_physics_engine(self):
        self.physics_engine = PhysicsEnginePlatformer(
            self.knight, self.platforms, gravity_constant=GRAVITY, ladders=self.ladders
        )

    def setup_sounds(self):
        self.collectible_sound = load_sound(f"{AUDIO_DIR}/coin1.wav")
        self.gameover_sound = load_sound(f"{AUDIO_DIR}/lose1.wav")

        self.knight.setup_sounds()

    def setup_images(self):
        self.background_image = arcade.load_texture(
            f"{IMAGES_DIR}/backgrounds/BG.png"
        )

    def on_key_press(self, symbol, modifiers):
        # Knight movement and attack
        if symbol == arcade.key.RIGHT:
            self.knight.change_x = KNIGHT_SPEED

        elif symbol == arcade.key.LEFT:
            self.knight.change_x = -KNIGHT_SPEED

        elif symbol == arcade.key.UP:
            if self.physics_engine.can_jump() and not self.physics_engine.is_on_ladder():
                self.knight.change_y = KNIGHT_JUMP_SPEED
                self.knight.jump_sound.play()
            elif self.physics_engine.is_on_ladder():
                self.knight.change_y = KNIGHT_SPEED

        elif symbol == arcade.key.DOWN:
            if self.physics_engine.is_on_ladder():
                self.knight.change_y = -KNIGHT_SPEED

        elif symbol == arcade.key.SPACE:
            self.knight.is_attacking = True

        # Other key-based actions
        if symbol == arcade.key.Q:
            self.gameover_sound.play()
            arcade.close_window()

        if symbol == arcade.key.P:
            self.pause()

        return super().on_key_press(symbol, modifiers)

    def pause(self):
        """ Method that will bring up a screen that pauses the game """
        pass

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.RIGHT:
            self.knight.change_x = 0

        elif symbol == arcade.key.LEFT:
            self.knight.change_x = 0

        elif symbol in [arcade.key.UP, arcade.key.DOWN] and self.physics_engine.is_on_ladder():
            self.knight.change_y = 0

        elif symbol == arcade.key.SPACE:
            self.knight.is_attacking = False

        return super().on_key_release(symbol, modifiers)

    def update_viewport(self):
        """ --- Manage Scrolling --- """

        # Track if we need to change the viewport
        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.knight.left < left_boundary:
            self.view_left -= left_boundary - self.knight.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.knight.right > right_boundary:
            self.view_left += self.knight.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.knight.top > top_boundary:
            self.view_bottom += self.knight.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.knight.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.knight.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(
                self.view_left,
                SCREEN_WIDTH + self.view_left,
                self.view_bottom,
                SCREEN_HEIGHT + self.view_bottom,
            )

    def on_update(self, delta_time):
        self.character_sprites.update()
        self.character_sprites.update_animation()
        self.physics_engine.update()

        # Restrict Knight from falling off the left edge
        if self.knight.left < 0:
            self.knight.left = 0

        # Managing viewport
        self.update_viewport()

        # Collecting coins logic
        coins_collected = check_for_collision_with_list(
            self.knight, self.collectibles)
        for coin in coins_collected:
            coin.kill()
            self.knight.score += 1
            self.collectible_sound.play()

        return super().on_update(delta_time)

    def on_draw(self):
        start_render()

        # Drawing our loaded background images and setting it
        arcade.draw_texture_rectangle(
            (SCREEN_WIDTH // 2) + self.view_left,
            (SCREEN_HEIGHT // 2) + self.view_bottom,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.background_image,
        )

        self.platforms.draw()
        self.backgrounds.draw()
        self.ladders.draw()
        self.collectibles.draw()
        self.character_sprites.draw()
        self.dont_touch.draw()
        self.foregrounds.draw()

        return super().on_draw()
