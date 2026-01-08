import arcade


class MapBoard(arcade.View):
    def __init__(self, lobby=None):
        super().__init__()
        self.background_color = arcade.color.BLACK

        # Камера
        self.camera = arcade.Camera2D()

    def on_show_view(self) -> None:
        self.camera = arcade.Camera2D(
            projection=arcade.rect.XYWH(0, 0, 100, 100),
            position=(50, 50)
        )
        self.camera.viewport_width = self.width
        self.camera.viewport_height = self.height

    def on_draw(self) -> bool | None:
        self.clear()

        self.camera.use()

        # Линия в мировых координатах: от (0,0) до (100,100)
        # Будет растянута на ВЕСЬ ЭКРАН благодаря projection
        arcade.draw_line(0, 0, 100, 100, color=arcade.color.WHITE, line_width=2)

        # Точка в центре мира (50,50) - будет в центре экрана
        arcade.draw_circle_filled(50, 50, 10, arcade.color.RED)

        # Текст в разных углах мира
        arcade.draw_text("Левый низ (0,0)", 5, 5, arcade.color.GREEN, 12)
        arcade.draw_text("Правый верх (100,100)", 60, 90, arcade.color.GREEN, 12)

    def on_update(self, delta_time: float) -> bool | None:
        ...

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        print(x, y)
        print(self.camera.unproject((x, y)))
