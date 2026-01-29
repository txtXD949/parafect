import arcade


class ItemRow(arcade.gui.UIWidget):
    """Полоса с предметом в списке"""

    def __init__(self, width=350, height=40):
        super().__init__(width=width, height=height)

        self._x = 0
        self._y = 0
        self.item_id = ""
        self.name = ""
        self.price = 0
        self.is_selected = False
        self.text_label = None

    def setup(self, item_id, name, price, x, y):
        self.item_id = item_id
        self.name = name
        self.price = price
        self._x = x
        self._y = y

        # UILabel
        self.text_label = arcade.gui.UILabel(
            text=f'  {name} - {price}$',
            font_name='Courier New',
            font_size=16,
            text_color=arcade.color.LIGHT_GRAY,
            width=self.width,
            height=self.height
        )
        self.text_label.center_x = x + self.width // 2
        self.text_label.top = y

    @property
    def left(self):
        return self._x

    @property
    def right(self):
        return self._x + self.width

    @property
    def top(self):
        return self._y

    @property
    def bottom(self):
        return self._y - self.height

    def draw(self):
        if not self.text_label:
            return

        # Фон
        if self.is_selected:
            color = arcade.color.BLACK
        else:
            color = (40, 40, 40)

        arcade.draw_lrtb_rectangle_filled(
            self.left,
            self.right,
            self.top,
            self.bottom,
            color
        )

        # Текст
        self.text_label.draw()

    def check_mouse_press(self, x, y):
        return self.left <= x <= self.right and self.bottom <= y <= self.top
