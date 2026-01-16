import arcade
from pyglet.graphics import Batch


class GameLoading(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BLACK

        self.camera = None

        self.batch = None
        self.text = None

        self.timer = 0
        self.ind = 3

        self.closed = False

        self.setup()

    def setup(self):
        self.batch = Batch()
        self.text = arcade.Text(
            text='',
            x=400, y=280,
            color=arcade.color.WHITE,
            font_size=22,
            font_name='Courier New',
            anchor_x='center',
            anchor_y='center',
            batch=self.batch
        )

    def set_text(self):
        texts = ['.', '..', '...']

        if 0 < self.timer < 1.5:
            self.text.text = texts[0]
            return

        if 1.5 < self.timer < 3:
            self.text.text = texts[1]
            return

        if 3 < self.timer < 4.5:
            self.text.text = texts[2]
            return

        if self.timer > 4.5:
            self.timer = 0
            self.ind -= 1

    def on_update(self, delta_time: float) -> bool | None:
        if self.closed:
            return

        self.timer += delta_time

        self.set_text()

        if not self.ind:
            self.open_game()

    def on_draw(self) -> bool | None:
        self.clear()

        if self.closed:
            return

        self.batch.draw()

    def open_game(self):
        self.closed = True

        ...
