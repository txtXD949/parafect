import arcade


class Paper(arcade.View):
    COLORS = [
        arcade.color.BLACK,
        arcade.color.GRAY,
    ]

    def __init__(self, width, height, game):
        super().__init__()
        self.background_texture = arcade.load_texture('././assets/images/bg/paper.png')

    def setup(self):
        self.camera = arcade.Camera2D(
            projection=arcade.rect.XYWH(0, 0, 800, 600),
            position=(400, 300)
        )

    def on_draw(self):
        self.clear()

        self.camera.use()
        arcade.draw_texture_rect(self.background_texture, arcade.rect.LBWH(0, 0, 800, 600))
