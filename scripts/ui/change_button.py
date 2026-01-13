import arcade
from typing import List, Union, Optional, Sequence
from pyglet.graphics import Batch

Number = Union[int, float]


class ChangeButton:
    def __init__(
            self,
            values: Sequence[str],
            start_x: Number,
            start_y: Number,
            *,
            font_size: Number = 12,
            color: arcade.color.Color = arcade.color.WHITE,
            width: Optional[Number] = None,
            align: str = "center",
            anchor_x: str = "center",
            anchor_y: str = "center",
            bold: bool = False,
            italic: bool = False,
            font_name: Union[str, List[str]] = ("calibri", "arial"),
            multiline: bool = False,
            rotation: Number = 0.0,
            batch: Optional[Batch] = None,
    ):
        self.values = list(values)
        self._index = 0
        self.spacing = font_size * 2.0
        self.font_size = font_size
        self.start_x = start_x
        self.start_y = start_y

        self._text_params = {
            'font_size': font_size, 'color': color, 'width': width,
            'align': align, 'anchor_x': anchor_x, 'anchor_y': anchor_y,
            'bold': bold, 'italic': italic, 'font_name': font_name,
            'multiline': multiline, 'rotation': rotation, 'batch': batch
        }

        self._create_elements()

    @property
    def value(self) -> str:
        return self.values[self._index]

    @value.setter
    def value(self, new_value: str) -> None:
        self._index = self.values.index(new_value)
        self._create_elements()


    def _create_elements(self) -> None:
        approx_w_left = self.font_size * 0.8
        approx_w_value = self.font_size * 4
        approx_w_right = self.font_size * 0.8
        total_approx = approx_w_left + self.spacing + approx_w_value + self.spacing + approx_w_right

        left_x = self.start_x - total_approx / 2 + approx_w_left / 2
        value_x = self.start_x - total_approx / 2 + approx_w_left + self.spacing + approx_w_value / 2
        right_x = self.start_x + total_approx / 2 - approx_w_right / 2

        # ← Стрелки статичные
        self.arrow_left = arcade.Text(
            "<", left_x, self.start_y,
            font_size=self.font_size, color=self._text_params['color'],
            align="center", anchor_x="center", anchor_y=self._text_params['anchor_y'],
            batch=self._text_params['batch']
        )

        self.arrow_right = arcade.Text(
            ">", right_x, self.start_y,
            font_size=self.font_size, color=self._text_params['color'],
            align="center", anchor_x="center", anchor_y=self._text_params['anchor_y'],
            batch=self._text_params['batch']
        )

        self.text_value = arcade.Text(
            self.value, value_x, self.start_y,
            **self._text_params
        )

    def draw(self) -> None:
        self.arrow_left.draw()
        self.text_value.draw()
        self.arrow_right.draw()

    def next(self) -> None:
        self._index = (self._index + 1) % len(self.values)
        self._create_elements()

    def prev(self) -> None:
        self._index = (self._index - 1) % len(self.values)
        self._create_elements()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> bool:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return False

        if (self.arrow_left.left <= x <= self.arrow_left.right and
                self.arrow_left.bottom <= y <= self.arrow_left.top):
            self.prev()
            return True

        if (self.arrow_right.left <= x <= self.arrow_right.right and
                self.arrow_right.bottom <= y <= self.arrow_right.top):
            self.next()
            return True

        return False
