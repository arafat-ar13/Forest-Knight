import arcade

class Knight(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.texture = arcade.load_texture("assets/images/player/knight/Idle (1).png")

        self.center_x = 124
        self.center_y = 124
        self.scale = 0.15