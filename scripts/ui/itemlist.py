import arcade


class ItemsList:
    """Список предметов (в маркете)"""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.items = []
        self.visible_items = []
        self.selected_item = None
        self.scroll_offset = 0
        self.max_scroll = 0

        self.is_dragging = False
        self.last_mouse_y = 0

    def add_item_to_manager(self, manager, item_id, name, price):
        """Добавить предмет в менеджер"""
        y_pos = self.y - 30 + self.scroll_offset - len(self.items) * 45

        total_height = 30 + len(self.items) * 45
        self.max_scroll = max(0, total_height - self.height + 30)

        # UILabel
        item_label = arcade.gui.UILabel(
            text=f'  {name} - {price}$',
            font_name='Courier New',
            font_size=16,
            text_color=arcade.color.LIGHT_GRAY,
            width=self.width,
            height=40
        )
        item_label.center_x = self.x + self.width // 2
        item_label.top = y_pos

        # Сохраняем данные
        item_label.item_id = item_id
        item_label.name = name
        item_label.price = price
        item_label.is_selected = False

        self.items.append(item_label)

    def update_visibility(self, manager):
        """Обновляем видимость элементов"""
        # Удаляем старые видимые элементы
        for item in self.visible_items:
            manager.remove(item)
        self.visible_items.clear()

        panel_top = self.y - 55 * self.scale
        panel_bottom = self.y - self.height + 20 * self.scale

        # Добавляем только видимые элементы
        for item in self.items:
            item_bottom = item.top - item.height
            item_top = item.top

            is_visible = (item_bottom < panel_top and
                          item_top > panel_bottom)

            if is_visible:
                manager.add(item)
                self.visible_items.append(item)

    def update_positions(self):
        """Обновляем позиции всех предметов"""
        for i, item in enumerate(self.items):
            y_pos = self.y - 30 + self.scroll_offset - i * 45
            item.top = y_pos

    def check_mouse_press(self, x, y):
        """Обрабатываем клик по списку"""
        if not (self.x <= x <= self.x + self.width and
                self.y - self.height <= y <= self.y):
            return None

        # Проверяем только видимые элементы
        for item in self.visible_items:
            if (item.left <= x <= item.right and
                    item.top - item.height <= y <= item.top):

                # Снимаем выделение
                if self.selected_item:
                    self.selected_item.text_color = arcade.color.LIGHT_GRAY
                    self.selected_item.is_selected = False

                # Выделяем новый
                item.text_color = arcade.color.WHITE
                item.is_selected = True
                self.selected_item = item

                try:
                    from ..sounds import CLICK_SOUND
                    from ..views.settings import SettingsManager
                    volume = SettingsManager.get_sound_volume(0.6)
                    arcade.play_sound(CLICK_SOUND, volume=volume)
                except Exception:
                    pass

                return item.item_id

        return

    def on_mouse_press(self, x, y, button, modifiers):
        if (self.x <= x <= self.x + self.width and
                self.y - self.height <= y <= self.y):
            self.is_dragging = True
            self.last_mouse_y = y

    def on_mouse_release(self, x, y, button, modifiers):
        self.is_dragging = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.is_dragging:
            self.scroll_offset -= dy

            # Ограничиваем скролл
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

            self.update_positions()

            self.last_mouse_y = y
            return True
        return False

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if (self.x <= x <= self.x + self.width and
                self.y - self.height <= y <= self.y):
            self.scroll_offset -= scroll_y * 20

            # Ограничиваем
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

            self.update_positions()
            return True
        return False

    def draw_background(self):
        """Рисуем фон контейнера"""
        arcade.draw_lrbt_rectangle_filled(
            left=self.x,
            right=self.x + self.width,
            bottom=self.y - self.height,
            top=self.y - 30,
            color=(30, 30, 30)
        )
