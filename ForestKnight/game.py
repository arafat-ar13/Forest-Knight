"""
Primary game file that contains most of the logic of this game.
"""

import arcade
from arcade.physics_engines import PhysicsEnginePlatformer
from arcade.sound import load_sound
from arcade.sprite_list import SpriteList, check_for_collision_with_list
from arcade.window_commands import start_render

from ForestKnight.characters.enemies.zombie_male import ZombieMale
from ForestKnight.characters.player.knight import Knight
from ForestKnight.constants import (
    AUDIO_DIR,
    BOTTOM_VIEWPORT_MARGIN,
    GRAVITY,
    IMAGES_DIR,
    KNIGHT_X,
    KNIGHT_Y,
    LEFT_VIEWPORT_MARGIN,
    RIGHT_VIEWPORT_MARGIN,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TOP_VIEWPORT_MARGIN,
    ZOMBIE_MALE_LEVEL_1_POSITIONS,
)
from ForestKnight.game_saving_utility import save_game
from ForestKnight.helper_functions import level_loader
from ForestKnight.screens import PauseView


class ForestKnightView(arcade.View):
    """
    The main View class that runs the actual game code.
    """

    def __init__(self):
        super().__init__()

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Sprites
        self.knight = None
        self.character_sprites = None
        self.enemy_sprites = None
        self.platforms = None
        self.foregrounds = None
        self.backgrounds = None
        self.ladders = None
        self.dont_touch = None
        self.collectibles = None
        self.collectibles_to_omit = None

        # Sounds
        self.collectible_sound = None
        self.gameover_sound = None

        # Images
        self.background_image = None

        # Physics Engine
        self.physics_engine = None

        # Level
        self.level = None

    def setup(self, level: int, load_game: bool = False, loaded_game_data: dict = None):
        """
        Method that sets up the given level of the game.
        It also calls other setup methods used in the game.
        Send `load_game_data` only if the game is being loaded from the hard disk
        """
        self.character_sprites = SpriteList()
        self.enemy_sprites = SpriteList()

        self.collectibles_to_omit = []

        self.level = level

        self.setup_sprites(self.level)
        self.setup_characters()

        # We'll only load the game if this is NOT the first time playing it
        if load_game:
            self.load_game_data(loaded_game_data)

        self.update_viewport()
        self.setup_physics_engine()
        self.setup_sounds()
        self.setup_images()

    def setup_sprites(self, level: int):
        """Method that sets up all the Sprites (except for Knight and other Enemies)"""
        loaded_sprites = level_loader(level, self.collectibles_to_omit)

        self.platforms = loaded_sprites["Platforms"]
        self.foregrounds = loaded_sprites["Foregrounds"]
        self.backgrounds = loaded_sprites["Backgrounds"]
        self.ladders = loaded_sprites["Ladders"]
        self.dont_touch = loaded_sprites["Dont-Touch"]
        self.collectibles = loaded_sprites["Collectibles"]

    def setup_characters(self):
        """Method to set up the Knight and other Enemies"""
        self.knight = Knight(pos_x=KNIGHT_X, pos_y=KNIGHT_Y)
        self.character_sprites.append(self.knight)
        self.character_sprites.preload_textures(self.knight.textures)

        for pos in ZOMBIE_MALE_LEVEL_1_POSITIONS:
            pos_x = pos[0]
            pos_y = pos[1]

            enemy = ZombieMale(pos_x, pos_y)
            self.enemy_sprites.append(enemy)

        for enemy in self.enemy_sprites:
            self.enemy_sprites.preload_textures(enemy.textures)

    def setup_physics_engine(self):
        """Method to set up arcade.PhysicsEnginePlatformer"""
        self.physics_engine = PhysicsEnginePlatformer(
            self.knight, self.platforms, gravity_constant=GRAVITY, ladders=self.ladders
        )

    def setup_sounds(self):
        """Method that loads all the sounds required in the game"""
        self.collectible_sound = load_sound(f"{AUDIO_DIR}/coin1.wav")
        self.gameover_sound = load_sound(f"{AUDIO_DIR}/lose1.wav")
        self.background_music = load_sound(f"{AUDIO_DIR}/backgroundMusic2.mp3")

        # We'll play the background music during initial setup
        # self.background_play = Sound.play(self.background_music, volume=0.2)

        self.knight.setup_sounds()

    def setup_images(self, level: int = 1):
        """Method to set up background image of the current level"""
        if level == 1:
            self.background_image = arcade.load_texture(
                f"{IMAGES_DIR}/backgrounds/BG.png"
            )

    def on_key_press(self, symbol: int, modifiers: int):
        """Method that handles what happens when a key is pressed down"""
        # Knight movement and attack
        if symbol == arcade.key.RIGHT:
            self.knight.change_x = self.knight.speed

        elif symbol == arcade.key.LEFT:
            self.knight.change_x = -(self.knight.speed)

        elif symbol == arcade.key.UP:
            if (
                self.physics_engine.can_jump()
                and not self.physics_engine.is_on_ladder()
            ):
                self.knight.change_y = self.knight.jump_speed
                self.knight.jump_sound.play()
            elif self.physics_engine.is_on_ladder():
                self.knight.change_y = self.knight.speed

        elif symbol == arcade.key.DOWN:
            if self.physics_engine.is_on_ladder():
                self.knight.change_y = -(self.knight.speed)

        elif symbol == arcade.key.SPACE:
            self.knight.is_attacking = True

        if symbol in [
            arcade.key.DOWN,
            arcade.key.LEFT,
            arcade.key.RIGHT,
        ]:
            self.knight.is_moving = True

        # Other key-based actions
        if symbol == arcade.key.Q:
            arcade.close_window()

        if symbol == arcade.key.P:
            self.pause()

        if symbol == arcade.key.G:
            self.gen_game_data()

        if symbol == arcade.key.V:
            print(self.knight.position)

        return super().on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        """Method that handles what happens when a key is released"""
        if symbol == arcade.key.RIGHT:
            self.knight.change_x = 0

        elif symbol == arcade.key.LEFT:
            self.knight.change_x = 0

        elif (
            symbol in [arcade.key.UP, arcade.key.DOWN]
            and self.physics_engine.is_on_ladder()
        ):
            self.knight.change_y = 0

        elif symbol == arcade.key.SPACE:
            self.knight.is_attacking = False

        if symbol in [
            arcade.key.DOWN,
            arcade.key.LEFT,
            arcade.key.RIGHT,
        ]:
            self.knight.is_moving = False

        return super().on_key_release(symbol, modifiers)

    def pause(self):
        """Method that will bring up a screen that pauses the game"""
        pause_view = PauseView(self)
        self.window.show_view(pause_view)

    def gen_game_data(self):
        """
        Method that generates all the values that need to be saved
        and then calls the function from the game saving utility for the data
        to be actually saved on the hard disk
        """
        level = self.level
        health = self.knight.health
        score = self.knight.score
        pos = self.knight.position
        cur_texture = self.knight.texture
        knight_state = self.knight.state
        collectibles_to_omit = self.collectibles_to_omit

        data_dict = {
            "level": level,
            "health": health,
            "score": score,
            "position": pos,
            "texture": cur_texture,
            "knight_state": knight_state,
            "collectibles_to_omit": collectibles_to_omit,
        }

        # Calling function from gave saving utility
        save_game(data=data_dict)

    def load_game_data(self, data: dict):
        """
        Method that takes all the data from the loader function from the game saving utility and correctly sets up the game.
        This method will only be called if the game is NOT being run for the first time
        """
        self.knight.health = data["health"]
        self.knight.position = data["position"]
        self.knight.state = data["knight_state"]
        self.knight.score = data["score"]
        self.knight.texture = data["texture"]
        self.collectibles_to_omit = data["collectibles_to_omit"]

    def update_viewport(self):
        """Method that manages and updates the viewport according to where the Knight is"""

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

    def on_update(self, delta_time: float):
        """Method that is the main game loop and contains most game logic"""
        self.character_sprites.update_animation()
        self.character_sprites.update()
        self.enemy_sprites.update_animation()
        self.enemy_sprites.update()
        self.physics_engine.update()

        if self.knight.is_dying:
            self.knight.die()

        if self.knight.is_attacking:
            self.knight.attack()

        if (
            not self.knight.is_moving
            and not self.knight.is_attacking
            and not self.knight.is_dying
        ):
            self.knight.idle_animation()

        # Managing viewport
        self.update_viewport()

        # Collecting coins logic
        coins_collected = check_for_collision_with_list(self.knight, self.collectibles)
        for coin in coins_collected:
            self.collectibles_to_omit.append(coin.position)
            coin.kill()
            self.knight.score += 1
            self.collectible_sound.play()

        for enemy in self.enemy_sprites:
            # Enemies will always be on the lookout for the Knight
            enemy.detect_knight(self.knight)

        return super().on_update(delta_time)

    def on_draw(self):
        """
        We actually have to draw to the display to show anything on the screen.
        This method handles all the drawing in the game
        """
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
        self.enemy_sprites.draw()
        self.dont_touch.draw()
        self.foregrounds.draw()

        # Drawing the Knight's stats
        arcade.draw_text(
            f"Score: {self.knight.score}",
            self.view_left,
            self.view_bottom + 15,
            arcade.color.CHROME_YELLOW,
            15,
        )

        arcade.draw_text(
            f"Health: {self.knight.health}",
            self.view_left,
            self.view_bottom,
            arcade.color.ROSE_RED,
            15,
        )

        return super().on_draw()
