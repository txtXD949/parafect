import arcade


class PlayerSprite(arcade.Sprite):
    def __init__(self, player_class=None):
        super().__init__()

        self.textures = [
            arcade.load_texture()
        ]

        self.player_class = player_class

        self.animation_timer = 0
        self.texture_ind = 0

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        ...

