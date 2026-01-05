import arcade
from . import InteractiveLabel


class MarketButtons:
    def __init__(self, x, y, width, height, market_view):
        self.x = x
        self.y = y
        self.width = width
        self.height = 90
        self.market_view = market_view

        # Звуки
        self.hover_sound = arcade.load_sound('././assets/sounds/effects/hover.wav')
        self.click_sound = arcade.load_sound('././assets/sounds/effects/click.wav')

        # Кнопочки
        self.button_buy_item = None
        self.button_buy_all = None
        self.button_take_item = None
        self.button_remove_all = None

    def add_to_manager(self, manager):
        """Добавляем кнопки в UI Manager"""

        # Верхний ряд кнопок
        top_y = self.y - 100

        # $
        self.button_buy_item = InteractiveLabel(
            text='$',
            x=self.x + 10,
            y=top_y,
            width=120,
            height=35,
            font_size=12,
            font_name='Courier New',
            normal_color='#C8C8C8',
            hover_color='#FFF',
            active_color='#FFF',
            hover_sound=self.hover_sound,
            click_sound=self.click_sound
        )
        manager.add(self.button_buy_item)

        # $$
        self.button_buy_all = InteractiveLabel(
            text='$$',
            x=self.x + 140,
            y=top_y,
            width=120,
            height=35,
            font_size=12,
            font_name='Courier New',
            normal_color='#C8C8C8',
            hover_color='#FFF',
            active_color='#FFF',
            hover_sound=self.hover_sound,
            click_sound=self.click_sound
        )
        manager.add(self.button_buy_all)

        # Нижний ряд кнопок
        bottom_y = self.y - 135

        # Кнопка "^" (ВЗЯТЬ ПРЕДМЕТ)
        self.button_take_item = InteractiveLabel(
            text='^',
            x=self.x + 10,
            y=bottom_y,
            width=120,
            height=35,
            font_size=12,
            font_name='Courier New',
            normal_color='#C8C8C8',
            hover_color='#FFF',
            active_color='#FFF',
            hover_sound=self.hover_sound,
            click_sound=self.click_sound
        )
        manager.add(self.button_take_item)

        # ∨
        self.button_remove_selected = InteractiveLabel(
            text='∨',
            x=self.x + 140,
            y=bottom_y,
            width=120,
            height=35,
            font_size=12,
            font_name='Courier New',
            normal_color='#C8C8C8',
            hover_color='#FFF',
            active_color='#FFF',
            hover_sound=self.hover_sound,
            click_sound=self.click_sound
        )
        manager.add(self.button_remove_selected)

    def update_button_state(self):
        """Обновляем состояние кнопок"""
        has_selected = self.market_view.selected_item_id is not None

        if has_selected:
            self.button_buy_item.text_color = arcade.color.WHITE
            self.button_take_item.text_color = arcade.color.WHITE
        else:
            self.button_buy_item.text_color = arcade.color.Color.from_hex_string('#808080')
            self.button_take_item.text_color = arcade.color.Color.from_hex_string('#808080')

    def check_mouse_hover(self, x, y):
        """Проверяем наведение на кнопки"""
        self.button_buy_item.check_mouse_hover(x, y)
        self.button_buy_all.check_mouse_hover(x, y)
        self.button_take_item.check_mouse_hover(x, y)
        self.button_remove_selected.check_mouse_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика по кнопкам"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.button_buy_item.check_mouse_hover(x, y):
                self.button_buy_item.on_click()
                if self.button_buy_item._is_active:
                    self.market_view.buy_selected_item()

            elif self.button_buy_all.check_mouse_hover(x, y):
                self.button_buy_all.on_click()
                if self.button_buy_all._is_active:
                    self.market_view.buy_all_items()

            elif self.button_take_item.check_mouse_hover(x, y):
                self.button_take_item.on_click()
                if self.button_take_item._is_active:
                    self.market_view.take_selected_item()

            elif self.button_remove_selected.check_mouse_hover(x, y):
                self.button_remove_selected.on_click()
                if self.button_remove_selected._is_active:
                    self.market_view.remove_selected_item()
