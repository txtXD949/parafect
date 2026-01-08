import arcade
import json

from database import AccountManager, ProfileManager


class MarketView(arcade.View):
    def __init__(self, lobby=None, account_manager=None):
        super().__init__()

        # Окно
        self.selected_item_id = None
        self.lobby = lobby
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0

        # Профиль
        self.account = account_manager
        self.profile = ProfileManager()

        # Игрок
        self.player_balance = None
        self.player_level = None

        # Временный инвентарь
        self.temp_inventory_path = '././database/_game.json'
        self.temp_inventory = {}

    def on_show_view(self):
        # Масштаб и смещение для центрирования
        screen_width = self.window.width
        screen_height = self.window.height
        scale_x = screen_width / 800
        scale_y = screen_height / 600
        self.scale = min(scale_x, scale_y)

        # Смещение для центрирования
        self.offset_x = (screen_width - 800 * self.scale) / 2
        self.offset_y = (screen_height - 600 * self.scale) / 2

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Баланс и уровень из профиля
        profile = self.profile.load_profile(self.account.current_account)
        self.player_balance = profile['cash']
        self.player_level = profile['level']

        # Создаем или загружаем временный инвентарь
        self.load_or_create_temp_inventory()

        # МАРКЕТ
        market_label = arcade.gui.UILabel(
            text='МАРКЕТ',
            font_name='Courier New',
            font_size=int(36 * self.scale),
            text_color=arcade.color.WHITE,
            align='center'
        )
        market_label.center_x = self.offset_x + 400 * self.scale
        market_label.top = self.offset_y + 550 * self.scale
        self.manager.add(market_label)

        # ItemsList
        from ..ui import ItemsList
        self.items_list = ItemsList(
            x=self.offset_x + 70 * self.scale,
            y=self.offset_y + 520 * self.scale,
            width=380 * self.scale,
            height=450 * self.scale
        )
        self.items_list.scale = self.scale
        self.items_list.offset_x = self.offset_x
        self.items_list.offset_y = self.offset_y

        # Виджет информации о предмете
        from ..ui import ItemInfoWidget
        self.item_info = ItemInfoWidget(
            x=self.offset_x + 460 * self.scale,
            y=self.offset_y + 520 * self.scale,
            width=270 * self.scale,
            height=320 * self.scale
        )
        self.item_info.scale = self.scale
        self.item_info.offset_x = self.offset_x
        self.item_info.offset_y = self.offset_y
        self.item_info.add_to_manager(self.manager)

        # Кнопочки
        from ..ui import MarketButtons
        self.market_buttons = MarketButtons(
            x=self.offset_x + 460 * self.scale,
            y=self.offset_y + 200 * self.scale,
            width=270 * self.scale,
            height=130 * self.scale,
            market_view=self
        )
        self.market_buttons.scale = self.scale
        self.market_buttons.offset_x = self.offset_x
        self.market_buttons.offset_y = self.offset_y
        self.market_buttons.add_to_manager(self.manager)

        # Данные предметов
        from ..ui import ITEM_DATABASE
        self.items_data = ITEM_DATABASE.copy()

        self.update_items_from_temp_inventory()

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

        # Добавляем предметы
        base_y = self.offset_y + 520 * self.scale - 30 * self.scale

        for i, (item_id, name, price) in enumerate(items_to_show):
            item_label = arcade.gui.UILabel(
                text=f'  {name} - {price}$',
                font_name='Courier New',
                font_size=int(16 * self.scale),
                text_color=arcade.color.LIGHT_GRAY,
                width=380 * self.scale,
                height=40 * self.scale
            )

            y_pos = base_y - i * 45 * self.scale + self.items_list.scroll_offset

            item_label.center_x = self.offset_x + (70 + 190) * self.scale
            item_label.top = y_pos
            item_label.item_id = item_id
            item_label.name = name
            item_label.price = price
            item_label.is_selected = False

            self.items_list.items.append(item_label)

            # Максимальный скролл
            total_height = 30 * self.scale + len(self.items_list.items) * 45 * self.scale
            self.items_list.max_scroll = max(0, total_height - 450 * self.scale + 30 * self.scale)

        self.items_list.update_visibility(self.manager)

        # Устанавливаем первый предмет как выбранный
        if items_to_show:
            self.selected_item_id = items_to_show[0][0]
            self.item_info.update_info(self.items_data[self.selected_item_id])
            self.market_buttons.update_button_state()

        # Камера
        self.default_camera = arcade.Camera2D(
            projection=arcade.rect.XYWH(0, 0, self.window.width, self.window.height)
        )

        # Уровень и баланс
        self.level_label = arcade.gui.UILabel(
            text=f'Lvl: {self.player_level}',
            font_name='Courier New',
            font_size=int(16 * self.scale),
            text_color=arcade.color.WHITE,
            align='left',
            width=200 * self.scale
        )
        self.level_label.left = 10
        self.level_label.top = self.window.height - 10
        self.manager.add(self.level_label)

        self.balance_label = arcade.gui.UILabel(
            text=f'Баланс: {self.player_balance}$',
            font_name='Courier New',
            font_size=int(16 * self.scale),
            text_color=arcade.color.WHITE,
            align='left',
            width=200 * self.scale
        )
        self.balance_label.left = 10
        self.balance_label.top = self.window.height - (10 + 20 * self.scale)
        self.manager.add(self.balance_label)

    def on_draw(self):
        self.clear()

        self.default_camera.use()

        # Толщина линий с масштабом
        line_width = max(2, int(2 * self.scale))
        thin_line_width = max(1, int(1 * self.scale))

        # Внешняя рамка
        arcade.draw_line(
            self.offset_x + 50 * self.scale,
            self.offset_y + 550 * self.scale,
            self.offset_x + 750 * self.scale,
            self.offset_y + 550 * self.scale,
            arcade.color.WHITE, line_width
        )
        arcade.draw_line(
            self.offset_x + 750 * self.scale,
            self.offset_y + 550 * self.scale,
            self.offset_x + 750 * self.scale,
            self.offset_y + 50 * self.scale,
            arcade.color.WHITE, line_width
        )
        arcade.draw_line(
            self.offset_x + 750 * self.scale,
            self.offset_y + 50 * self.scale,
            self.offset_x + 50 * self.scale,
            self.offset_y + 50 * self.scale,
            arcade.color.WHITE, line_width
        )
        arcade.draw_line(
            self.offset_x + 50 * self.scale,
            self.offset_y + 50 * self.scale,
            self.offset_x + 50 * self.scale,
            self.offset_y + 550 * self.scale,
            arcade.color.WHITE, line_width
        )

        # Внутренняя рамка
        arcade.draw_line(
            self.offset_x + 60 * self.scale,
            self.offset_y + 540 * self.scale,
            self.offset_x + 740 * self.scale,
            self.offset_y + 540 * self.scale,
            arcade.color.WHITE, thin_line_width
        )
        arcade.draw_line(
            self.offset_x + 740 * self.scale,
            self.offset_y + 540 * self.scale,
            self.offset_x + 740 * self.scale,
            self.offset_y + 60 * self.scale,
            arcade.color.WHITE, thin_line_width
        )
        arcade.draw_line(
            self.offset_x + 740 * self.scale,
            self.offset_y + 60 * self.scale,
            self.offset_x + 60 * self.scale,
            self.offset_y + 60 * self.scale,
            arcade.color.WHITE, thin_line_width
        )
        arcade.draw_line(
            self.offset_x + 60 * self.scale,
            self.offset_y + 60 * self.scale,
            self.offset_x + 60 * self.scale,
            self.offset_y + 540 * self.scale,
            arcade.color.WHITE, thin_line_width
        )

        # Компьютерный интерфейс
        x = self.offset_x + 730 * self.scale
        y = self.offset_y + 530 * self.scale

        # _
        arcade.draw_line(
            x - 80 * self.scale, y - 5 * self.scale,
            x - 90 * self.scale, y - 5 * self.scale,
            arcade.color.WHITE, thin_line_width
        )

        # □
        arcade.draw_line(
            x - 55 * self.scale, y - 15 * self.scale,
            x - 40 * self.scale, y - 15 * self.scale,
            arcade.color.WHITE, thin_line_width
        )
        arcade.draw_line(
            x - 55 * self.scale, y - 15 * self.scale,
            x - 55 * self.scale, y,
            arcade.color.WHITE, thin_line_width
        )
        arcade.draw_line(
            x - 55 * self.scale, y,
            x - 40 * self.scale, y,
            arcade.color.WHITE, thin_line_width
        )
        arcade.draw_line(
            x - 40 * self.scale, y,
            x - 40 * self.scale, y - 15 * self.scale,
            arcade.color.WHITE, thin_line_width
        )

        # X
        arcade.draw_line(
            x - 15 * self.scale, y,
            x - 5 * self.scale, y - 10 * self.scale,
            arcade.color.WHITE, thin_line_width
        )
        arcade.draw_line(
            x - 5 * self.scale, y,
            x - 15 * self.scale, y - 10 * self.scale,
            arcade.color.WHITE, thin_line_width
        )

        # Разделительные линии
        arcade.draw_line(
            self.offset_x + 70 * self.scale,
            self.offset_y + 70 * self.scale,
            self.offset_x + 450 * self.scale,
            self.offset_y + 70 * self.scale,
            arcade.color.WHITE, thin_line_width
        )

        arcade.draw_line(
            self.offset_x + 460 * self.scale,
            self.offset_y + 150 * self.scale,
            self.offset_x + 730 * self.scale,
            self.offset_y + 150 * self.scale,
            arcade.color.WHITE, thin_line_width
        )
        arcade.draw_line(
            self.offset_x + 460 * self.scale,
            self.offset_y + 70 * self.scale,
            self.offset_x + 730 * self.scale,
            self.offset_y + 70 * self.scale,
            arcade.color.WHITE, thin_line_width
        )

        # Фон для списка предметов
        self.items_list.draw_background()

        # Фон для информации о предмете
        self.item_info.draw_background()

        # Спрайт предмета
        self.item_info.draw_image()

        # UI элементы
        self.manager.draw()

    def on_update(self, delta_time):
        """Обновление анимации кнопок"""
        buttons = [
            self.market_buttons.button_buy_item,
            self.market_buttons.button_buy_all,
            self.market_buttons.button_take_item,
            self.market_buttons.button_remove_all
        ]

        for button in buttons:
            if button:
                button.on_update(delta_time)

        # Обновление баланса и уровня
        self.level_label.text = f'Lvl: {self.player_level}'
        self.balance_label.text = f'Баланс: {self.player_balance}$'

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.close_market()

    def on_mouse_motion(self, x, y, dx, dy):
        """Обработка движения мыши"""
        self.market_buttons.check_mouse_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        selected_id = self.items_list.check_mouse_press(x, y)
        if selected_id:
            self.selected_item_id = selected_id

            if selected_id in self.items_data:
                self.item_info.update_info(self.items_data[selected_id])

            self.market_buttons.update_button_state()

        self.market_buttons.on_mouse_press(x, y, button, modifiers)

        # X кнопка закрытия
        close_x_min = self.offset_x + 715 * self.scale
        close_x_max = self.offset_x + 725 * self.scale
        close_y_min = self.offset_y + 520 * self.scale
        close_y_max = self.offset_y + 530 * self.scale

        if (close_x_min <= x <= close_x_max and
                close_y_min <= y <= close_y_max):
            self.close_market()

        self.items_list.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.items_list.on_mouse_release(x, y, button, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.items_list.on_mouse_scroll(x, y, scroll_x, scroll_y):
            self.items_list.scroll_offset -= scroll_y * 30 * self.scale

            # Ограничиваем
            self.items_list.scroll_offset = max(0, min(
                self.items_list.scroll_offset,
                self.items_list.max_scroll
            ))

            base_y = self.offset_y + 520 * self.scale - 30 * self.scale
            for i, item in enumerate(self.items_list.items):
                y_pos = base_y - i * 45 * self.scale + self.items_list.scroll_offset
                item.top = y_pos

            self.items_list.update_visibility(self.manager)

    def buy_selected_item(self):
        if not self.selected_item_id:
            return

        item = self.items_data[self.selected_item_id]

        # Проверяем уровень игрока
        if self.player_level < item.on_level:
            arcade.play_sound(arcade.load_sound('././assets/sounds/effects/reject_sound.wav'), volume=-0.3)
            return

        # Проверяем баланс игрока
        if item.price > self.player_balance:
            arcade.play_sound(arcade.load_sound('././assets/sounds/effects/reject_sound.wav'), volume=-0.3)
            return

        # Обновляем баланс
        new_balance = self.player_balance - item.price
        self.profile.update_cash(self.account.current_account, new_balance, 'set')

        # Добавляем на склад
        current_inventory = self.profile.load_profile(self.account.current_account)['inventory']
        new_count = current_inventory.get(self.selected_item_id, 0) + 1
        self.profile.update_inventory(
            self.account.current_account,
            self.selected_item_id,
            new_count,
            'set'
        )

        self.player_balance -= item.price
        item.in_inventory += 1

        self.item_info.update_info(item)

    def buy_all_items(self):
        items_to_buy = []
        total_cost = 0

        # Собираем предметы по уровню
        for item_id, item in self.items_data.items():
            if self.player_level >= item.on_level:
                items_to_buy.append((item_id, item))
                total_cost += item.price

        if not items_to_buy:
            arcade.play_sound(arcade.load_sound('././assets/sounds/effects/reject_sound.wav'), volume=-0.3)
            return

        if total_cost > self.player_balance:
            arcade.play_sound(arcade.load_sound('././assets/sounds/effects/reject_sound.wav'), volume=-0.3)
            return

        # Обновляем баланс
        new_balance = self.player_balance - total_cost
        self.profile.update_cash(self.account.current_account, new_balance, 'set')

        # Добавляем на склад
        for item_id, _ in items_to_buy:
            current_inventory = self.profile.load_profile(self.account.current_account)['inventory']
            new_count = current_inventory.get(item_id, 0) + 1
            self.profile.update_inventory(
                self.account.current_account,
                item_id,
                new_count,
                'set'
            )

        for _, item in items_to_buy:
            item.in_inventory += 1

        self.player_balance -= total_cost

        if self.selected_item_id:
            self.item_info.update_info(self.items_data[self.selected_item_id])

    def take_selected_item(self):
        """Взять предмет со склада с собой в игру"""
        if not self.selected_item_id:
            return

        item = self.items_data[self.selected_item_id]

        if item.in_inventory <= 0:
            arcade.play_sound(arcade.load_sound('././assets/sounds/effects/reject_sound.wav'), volume=-0.3)
            return

        current_taken = self.temp_inventory.get('inventory', {}).get(self.selected_item_id, 0)
        if current_taken >= item.max_in_game:
            arcade.play_sound(arcade.load_sound('././assets/sounds/effects/reject_sound.wav'), volume=-0.3)
            return

        inventory = self.temp_inventory.get('inventory', {})
        current_count = inventory.get(self.selected_item_id, 0)
        inventory[self.selected_item_id] = current_count + 1
        self.temp_inventory['inventory'] = inventory

        self.save_temp_inventory()

        current_stock = self.profile.load_profile(self.account.current_account)['inventory'].get(self.selected_item_id,
                                                                                                 0)
        if current_stock > 0:
            self.profile.update_inventory(
                self.account.current_account,
                self.selected_item_id,
                current_stock - 1,
                'set'
            )
        else:
            arcade.play_sound(arcade.load_sound('././assets/sounds/effects/reject_sound.wav'), volume=-0.3)
            return

        item.in_inventory -= 1
        item.selected = current_count + 1

        self.item_info.update_info(item)

    def remove_selected_item(self):
        """Вернуть предмет из "с собой" обратно на склад"""
        if not self.selected_item_id:
            return

        item = self.items_data[self.selected_item_id]

        current_taken = self.temp_inventory.get('inventory', {}).get(self.selected_item_id, 0)
        if current_taken <= 0:
            arcade.play_sound(arcade.load_sound('././assets/sounds/effects/reject_sound.wav'), volume=-0.3)
            return

        basic_items = {'flash_light', 'emf', 'uf', 'dict', 'term', 'mic', 'book'}
        if self.selected_item_id in basic_items and current_taken <= 1:
            arcade.play_sound(arcade.load_sound('././assets/sounds/effects/reject_sound.wav'), volume=-0.3)
            return

        inventory = self.temp_inventory.get('inventory', {})
        inventory[self.selected_item_id] = current_taken - 1

        if inventory[self.selected_item_id] <= 0 and self.selected_item_id not in basic_items:
            del inventory[self.selected_item_id]

        self.temp_inventory['inventory'] = inventory

        self.save_temp_inventory()

        current_stock = self.profile.load_profile(self.account.current_account)['inventory'].get(self.selected_item_id,
                                                                                                 0)
        self.profile.update_inventory(
            self.account.current_account,
            self.selected_item_id,
            current_stock + 1,  # Увеличиваем на складе
            'set'
        )

        item.in_inventory += 1
        item.selected = current_taken - 1

        self.item_info.update_info(item)

    def load_or_create_temp_inventory(self):
        """Создает или загружает временный инвентарь"""
        try:
            with open(self.temp_inventory_path, 'r', encoding='utf-8') as f:
                self.temp_inventory = json.load(f)
        except FileNotFoundError:
            self.temp_inventory = {'inventory': {}, 'map': None, 'difficulty': None}
            self.save_temp_inventory()

    def update_items_from_temp_inventory(self):
        """Обновляет данные предметов из временного инвентаря"""
        profile = self.profile.load_profile(self.account.current_account)

        for item_id, item_data in self.items_data.items():
            # Загружаем данные
            main_inventory_count = profile['inventory'].get(item_id, 0)

            # Сколько взято с собой
            in_game_count = self.temp_inventory.get('inventory', {}).get(item_id, 0)

            # Устанавливаем значения
            item_data.in_inventory = main_inventory_count
            item_data.selected = in_game_count

    def save_temp_inventory(self):
        """Сохраняет временный инвентарь в файл"""
        with open(self.temp_inventory_path, 'w', encoding='utf-8') as f:
            json.dump(self.temp_inventory, f, ensure_ascii=False, indent=2)

    def close_market(self):
        self.window.show_view(self.lobby)
