import arcade

from game import GameWindow

def main():
    game = GameWindow()
    game.setup(1)

    arcade.run()


if __name__ == "__main__":
    main()
