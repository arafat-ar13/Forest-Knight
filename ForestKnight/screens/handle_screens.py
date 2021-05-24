import arcade
from ForestKnight.game import ForestKnightView
from ForestKnight.game_saving_utility import create_data_dir, load_game


def load_game_screen(window: arcade.Window):
    game_view = ForestKnightView()
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
        game_view.setup(level=level)
        print("Game running for the first time")
    else:
        game_view.setup(level=level, load_game=True, loaded_game_data=loaded_data)

    window.show_view(game_view)


def load_pause_screen(window: arcade.Window):
    pass


def load_instructions_screen(window: arcade.Window):
    pass
