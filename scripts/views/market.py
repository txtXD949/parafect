import arcade


class MarketView(arcade.View):
    def __init__(self, balance=1000, lobby=None):
        super().__init__()

        self.player_balance = balance
        self.selected_item_id = None
        self.lobby = lobby

        # Камера для маркета
        self.camera = None

        # Размеры виртуального экрана (как в лобби)
        self.virtual_width = 800
        self.virtual_height = 600

    def on_show_view(self):
        # Инициализируем камеру
        self.camera = arcade.Camera2D()

        # Задаем виртуальные размеры
        self.camera.projection = arcade.rect.XYWH(
            0, 0,
            self.virtual_width,
            self.virtual_height
        )

        # Настраиваем вьюпорт под реальный размер окна
        self.camera.viewport_width = self.window.width
        self.camera.viewport_height = self.window.height

        # Позиционируем камеру
        self.camera.position = (
            self.virtual_width / 2,
            self.virtual_height / 2
        )

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # МАРКЕТ - используем виртуальные координаты
        market_label = arcade.gui.UILabel(
            text='МАРКЕТ',
            font_name='Courier New',
            font_size=36,
            text_color=arcade.color.WHITE,
            align='center'
        )
        market_label.center_x = 400  # виртуальные координаты
        market_label.top = 550
        self.manager.add(market_label)

        # Создаем ItemsList - используем виртуальные координаты
        from ..ui import ItemsList
        self.items_list = ItemsList(x=70, y=520, width=380, height=450)

        # Виджет информации о предмете - виртуальные координаты
        from ..ui import ItemInfoWidget
        self.item_info = ItemInfoWidget(
            x=460, y=520,
            width=270, height=320
        )
        self.item_info.add_to_manager(self.manager)

        # Кнопочки - виртуальные координаты
        from ..ui import MarketButtons
        self.market_buttons = MarketButtons(
            x=460, y=200,
            width=270, height=130,
            market_view=self
        )
        self.market_buttons.add_to_manager(self.manager)

        # Данные предметов
        from ..ui import ITEM_DATABASE
        self.items_data = ITEM_DATABASE.copy()

        items_to_show = [
            ('flash_light', 'ФОНАРИК', 150),
            ('emf', 'ЭМП', 200),
            ('uf', 'УФ-ФОНАРИК', 150),
            ('dict', 'ДИКТОФОН', 200),
            ('camera', 'ФОТОКАМЕРА', 300),
            ('term', 'ТЕРМОМЕТР', 150),
            ('mic', 'НАПРВЛЕННЫЙ МИКРОФОН', 200),
            ('book', 'БЛОКНОТ', 200),
            ('incense', 'БЛАГОВОНИЯ', 150),
            ('lighter', 'ЗАЖИГАЛКА', 50),
            ('pills', 'УСПОКОИТЕЛЬНОЕ', 150)
        ]

        for item_id, name, price in items_to_show:
            self.items_list.add_item_to_manager(self.manager, item_id, name, price)

        self.items_list.update_visibility(self.manager)

        # Устанавливаем первый предмет как выбранный
        if items_to_show:
            self.selected_item_id = items_to_show[0][0]
            self.item_info.update_info(self.items_data[self.selected_item_id])
            self.market_buttons.update_button_state()

    def on_draw(self):
        self.clear()

        # Используем камеру для всего рендеринга
        self.camera.use()

        # Внешняя рамка - виртуальные координаты
        arcade.draw_line(50, 550, 750, 550, arcade.color.WHITE, 2)
        arcade.draw_line(750, 550, 750, 50, arcade.color.WHITE, 2)
        arcade.draw_line(750, 50, 50, 50, arcade.color.WHITE, 2)
        arcade.draw_line(50, 50, 50, 550, arcade.color.WHITE, 2)

        # Внутренняя рамка
        arcade.draw_line(60, 540, 740, 540, arcade.color.WHITE, 1)
        arcade.draw_line(740, 540, 740, 60, arcade.color.WHITE, 1)
        arcade.draw_line(740, 60, 60, 60, arcade.color.WHITE, 1)
        arcade.draw_line(60, 60, 60, 540, arcade.color.WHITE, 1)

        # Компьютерный интерфейс
        x = 730
        y = 530

        # _
        arcade.draw_line(x - 80, y - 5, x - 90, y - 5, arcade.color.WHITE, 1)

        # □
        arcade.draw_line(x - 55, y - 15, x - 40, y - 15, arcade.color.WHITE, 1)
        arcade.draw_line(x - 55, y - 15, x - 55, y, arcade.color.WHITE, 1)
        arcade.draw_line(x - 55, y, x - 40, y, arcade.color.WHITE, 1)
        arcade.draw_line(x - 40, y, x - 40, y - 15, arcade.color.WHITE, 1)

        # X
        arcade.draw_line(x - 15, y, x - 5, y - 10, arcade.color.WHITE, 1)
        arcade.draw_line(x - 5, y, x - 15, y - 10, arcade.color.WHITE, 1)

        # Левая часть
        # Разделительная линия между левой и правой частями
        arcade.draw_line(450, 520, 450, 70, arcade.color.WHITE, 1)
        # Нижняя граница области товаров
        arcade.draw_line(70, 70, 450, 70, arcade.color.WHITE, 1)

        # Правая нижняя часть
        # Верхняя граница области кнопок
        arcade.draw_line(460, 150, 730, 150, arcade.color.WHITE, 1)
        # Нижняя граница области кнопок
        arcade.draw_line(460, 70, 730, 70, arcade.color.WHITE, 1)

        # Фон для списка предметов
        self.items_list.draw_background()

        # Фон для информации о предмете
        self.item_info.draw_background()

        # Спрайт предмета
        self.item_info.draw_image()

        # UI элементы рисуем без камеры (они уже в правильных координатах)
        self.manager.draw()

    def on_update(self, delta_time):
        """Обновление анимации кнопок"""
        # Анимация кнопок
        buttons = [
            self.market_buttons.button_buy_item,
            self.market_buttons.button_buy_all,
            self.market_buttons.button_take_item,
            self.market_buttons.button_remove_all
        ]

        for button in buttons:
            if button:
                button.on_update(delta_time)

    def on_resize(self, width: int, height: int):
        """Обработка изменения размера окна"""
        super().on_resize(width, height)

        if self.camera:
            # Обновляем вьюпорт камеры под новый размер окна
            self.camera.viewport_width = width
            self.camera.viewport_height = height

            # Пересчитываем позиционирование
            self.camera.position = (
                self.virtual_width / 2,
                self.virtual_height / 2
            )

    # Остальные методы остаются без изменений...
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.close_market()

    def on_mouse_motion(self, x, y, dx, dy):
        """Обработка движения мыши - конвертируем реальные координаты в виртуальные"""
        # Конвертируем реальные координаты мыши в виртуальные
        virtual_x = (x / self.window.width) * self.virtual_width
        virtual_y = (y / self.window.height) * self.virtual_height

        self.market_buttons.check_mouse_hover(virtual_x, virtual_y)

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мыши - конвертируем реальные координаты в виртуальные"""
        # Конвертируем реальные координаты мыши в виртуальные
        virtual_x = (x / self.window.width) * self.virtual_width
        virtual_y = (y / self.window.height) * self.virtual_height

        selected_id = self.items_list.check_mouse_press(virtual_x, virtual_y)
        if selected_id:
            self.selected_item_id = selected_id

            if selected_id in self.items_data:
                self.item_info.update_info(self.items_data[selected_id])

            self.market_buttons.update_button_state()

        self.market_buttons.on_mouse_press(virtual_x, virtual_y, button, modifiers)

        # X
        if 715 <= virtual_x <= 725 and 520 <= virtual_y <= 530:
            self.close_market()

        # Драг для скролла
        self.items_list.on_mouse_press(virtual_x, virtual_y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        """Обработка отпускания мыши - конвертируем реальные координаты в виртуальные"""
        virtual_x = (x / self.window.width) * self.virtual_width
        virtual_y = (y / self.window.height) * self.virtual_height

        self.items_list.on_mouse_release(virtual_x, virtual_y, button, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        """Обработка скролла мыши - конвертируем реальные координаты в виртуальные"""
        virtual_x = (x / self.window.width) * self.virtual_width
        virtual_y = (y / self.window.height) * self.virtual_height

        if self.items_list.on_mouse_scroll(virtual_x, virtual_y, scroll_x, scroll_y):
            self.items_list.update_visibility(self.manager)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Обработка перетаскивания мыши - конвертируем реальные координаты в виртуальные"""
        virtual_x = (x / self.window.width) * self.virtual_width
        virtual_y = (y / self.window.height) * self.virtual_height

        # Конвертируем дельту тоже
        virtual_dx = (dx / self.window.width) * self.virtual_width
        virtual_dy = (dy / self.window.height) * self.virtual_height

        if self.items_list.on_mouse_drag(virtual_x, virtual_y, virtual_dx, virtual_dy, buttons, modifiers):
            self.items_list.update_visibility(self.manager)

    # Остальные методы остаются без изменений...
    def buy_selected_item(self):
        if not self.selected_item_id:
            return

        item = self.items_data[self.selected_item_id]

        if item.price > self.player_balance:
            return

        if item.in_inventory >= item.max_in_game:
            return

        self.player_balance -= item.price
        item.in_inventory += 1

        self.item_info.update_info(item)

    def buy_all_items(self):
        items_to_buy = []
        total_cost = 0

        for item in self.items_data.values():
            if item.in_inventory < item.max_in_game:
                items_to_buy.append(item)
                total_cost += item.price

        if not items_to_buy:
            return

        if total_cost > self.player_balance:
            return

        for item in items_to_buy:
            item.in_inventory += 1

        self.player_balance -= total_cost

        if self.selected_item_id:
            self.item_info.update_info(self.items_data[self.selected_item_id])

    def take_selected_item(self):
        """Взять предмет из инвентаря с собой в игру"""
        if not self.selected_item_id:
            return

        item = self.items_data[self.selected_item_id]

        if item.in_inventory <= 0:
            return

        if item.selected >= item.max_in_game:
            return

        item.in_inventory -= 1
        item.selected += 1

        # Обновляем информацию
        self.item_info.update_info(item)

    def remove_selected_item(self):
        """Вернуть выбранный предмет из "с собой" обратно в инвентарь"""
        if not self.selected_item_id:
            return

        item = self.items_data[self.selected_item_id]

        if item.selected <= 0:
            return

        item.selected -= 1
        item.in_inventory += 1

        # Обновляем информацию
        self.item_info.update_info(item)

    def close_market(self):
        self.window.show_view(self.lobby)