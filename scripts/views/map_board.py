import arcade
from pyglet.graphics import Batch

from functools import lru_cache


class MapInfo:
    def __init__(self, name, size, desc, cords, on_level=1):
        self.name: str = name
        self.size: str = size
        self.desc: str = desc
        self.cords: str = cords
        self.on_level: int = on_level


MAP_DATABASE = {
    'dom_1': MapInfo(
        name='ДОМ 1',
        size='МАЛЕНЬКАЯ',
        cords='38.279567°N, -122.009865°E',
        desc='"Они переехали через месяц. Говорят, ребёнок всё время разговаривал с кем-то в углу."',
    ),
    'dom_3': MapInfo(
        name='ДОМ 3',
        size='СРЕДНЯЯ',
        cords='38.349100°N, -121.956000°E',
        desc='"Местные обходят это место. Говорят, ночью в окнах виден свет, хотя электричество отключено ещё в 90-х."',
        on_level=5
    ),
    'caffe': MapInfo(
        name='КАФЕ',
        size='СРЕДНЯЯ',
        cords='34.163680°N, -117.904245°E',
        desc='"Бармен жаловался, на посетителя, который несколько часов пил один кофе в углу. На камера никого не было видно."',
        on_level=10
    ),
    'kv_no96': MapInfo(
        name='КВАРТИРА №96',
        size='СРЕДНЯЯ',
        cords='58.630501°N, 59.789185°E',
        desc='"Жильцы писали коллективную жалобу на соседа, который стучал по батареям, в двери и моргал светом ночами. Этот сосед умер в 1989."',
        on_level=15
    ),
    'school': MapInfo(
        name='ШКОЛА',
        size='БОЛЬШАЯ',
        cords='57.874040°N, 59.949528°E',
        desc='"Школа была закрыта давно по неизвестным причинам. Власти не торопятся ее сносить."',
        on_level=20
    ),
    'bunker': MapInfo(
        name='КАФЕ',
        size='СРЕДНЯЯ',
        cords='68.925214°N, 33.089326°E',
        desc='"Группа исследователей сообщила, что видела свои же трупы. Больше сообщений от них не поступало."',
        on_level=30
    )
}


class MapBoard(arcade.View):
    def __init__(self, lobby=None):
        super().__init__()
        self.background_color = arcade.color.BLACK
        self.lobby = lobby

        # Спрайт-листы
        self.map_sprites = arcade.SpriteList()  # Белые #
        self.point_sprites = arcade.SpriteList()  # Желтые #
        self.all_sprites = arcade.SpriteList()  # Все вместе (для отрисовки)

        # Загружаем и создаем спрайты
        self.create_map_sprites()

        # Камера
        self.camera = None

        # UI элементы (оставляем batch для текстов)
        self.batch = Batch()
        self.setup()

    def setup(self):
        """UI элементы (заголовки)"""
        # КАРТА
        self.text_map = arcade.Text(
            text='КАРТА',
            x=570 / 2 + 30,
            y=600 - 35,
            color=arcade.color.WHITE,
            font_size=22,
            font_name='Courier New',
            anchor_x='center',
            anchor_y='top',
            batch=self.batch
        )

        # ИНФО
        self.text_info = arcade.Text(
            text='ИНФОРМАЦИЯ',
            x=180 / 2 + 590,
            y=600 - 35,
            color=arcade.color.WHITE,
            font_size=22,
            font_name='Courier New',
            anchor_x='center',
            anchor_y='top',
            batch=self.batch
        )

        self.map_textes()

    def on_show_view(self) -> None:
        self.camera = arcade.Camera2D(
            projection=arcade.rect.XYWH(0, 0, 800, 600),
            position=(400, 300)
        )
        self.camera.viewport_width = self.width
        self.camera.viewport_height = self.height

    def on_draw(self) -> bool | None:
        self.clear()

        self.camera.use()

        # Рамка
        arcade.draw_line(20, 20, 780, 20, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(20, 20, 20, 580, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(20, 580, 780, 580, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(780, 20, 780, 580, color=arcade.color.WHITE, line_width=1)

        # Панелька карта
        arcade.draw_line(30, 30, 580, 30, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(30, 30, 30, 570, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(30, 570, 580, 570, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(580, 30, 580, 570, color=arcade.color.WHITE, line_width=1)
        arcade.draw_rect_filled(arcade.rect.LBWH(30, 30, 550, 540), color=(30, 30, 30))

        # Панелька инфо
        arcade.draw_line(590, 30, 770, 30, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(590, 30, 590, 570, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(590, 570, 770, 570, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(770, 30, 770, 570, color=arcade.color.WHITE, line_width=1)
        arcade.draw_rect_filled(arcade.rect.LBWH(590, 30, 180, 540), color=(30, 30, 30))

        # Граница карты
        arcade.draw_line(30, 460, 580, 460, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(30, 120, 580, 120, color=arcade.color.WHITE, line_width=1)

        # Выход из доски
        arcade.draw_line(570 / 2 + 30, 70, 570 / 2 + 30 + 15, 80, color=arcade.color.WHITE)
        arcade.draw_line(570 / 2 + 30, 70, 570 / 2 + 30 - 15, 80, color=arcade.color.WHITE)

        # Рисуем все спрайты
        self.all_sprites.draw()

        # Batch
        self.batch.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        # Преобразуем в мировые координаты
        world_pos = self.camera.unproject((x, y))

        # Закрытие доски
        if 300 <= world_pos[0] <= 330 and 70 <= world_pos[1] <= 80:
            self.close_mapboard()

        # 1. Проверяем желтые точки (кликабельные)
        clicked_points = arcade.get_sprites_at_point(
            (world_pos.x, world_pos.y),
            self.point_sprites
        )

        if clicked_points:
            for point in clicked_points:
                print(f"Клик на желтую точку! ID: {point.point_id}")
                print(f"Координаты сетки: ({point.char_x}, {point.char_y})")
                print(f"Данные уровня: {point.level_data}")

                # Вызываем обработчик
                self.on_point_clicked(point)
            return

        # 2. Проверяем белые # (не кликабельные, но можем логировать)
        clicked_map = arcade.get_sprites_at_point(
            (world_pos.x, world_pos.y),
            self.map_sprites
        )

        if clicked_map:
            print(f"Клик на карту (белый #)")
            # Ничего не делаем, или просто логируем
            return

        print(f"Клик вне карты: {world_pos}")

    def create_map_sprites(self):
        """Создает спрайты для карты и точек"""
        # Загружаем текстовые файлы
        map_lines = self.get_map(arg='map')
        point_lines = self.get_map(arg='points')

        # Настройки
        char_size = 16.5  # Размер спрайта (квадрат 20x20)
        start_x = 23  # Начальная позиция X
        start_y = 450  # Начальная позиция Y (сверху вниз)

        # 1. СОЗДАЕМ ТЕКСТУРЫ ОДИН РАЗ
        white_texture = self.create_char_texture('#', arcade.color.WHITE)
        yellow_texture = self.create_char_texture('#', arcade.color.YELLOW)

        # 2. СОЗДАЕМ СПРАЙТЫ ДЛЯ КАРТЫ (белые #)
        for y_idx, line in enumerate(map_lines):
            for x_idx, char in enumerate(line):
                if char == '#':
                    sprite = arcade.Sprite()
                    sprite.texture = white_texture
                    sprite.width = char_size
                    sprite.height = char_size
                    sprite.center_x = start_x + (x_idx * char_size)
                    sprite.center_y = start_y - (y_idx * char_size)
                    sprite.char_type = 'map'  # Метаданные
                    sprite.char_x = x_idx  # Позиция в сетке
                    sprite.char_y = y_idx

                    self.map_sprites.append(sprite)
                    self.all_sprites.append(sprite)

        # 3. СОЗДАЕМ СПРАЙТЫ ДЛЯ ТОЧЕК (желтые #)
        for y_idx, line in enumerate(point_lines):
            for x_idx, char in enumerate(line):
                if char == '#':
                    sprite = arcade.Sprite()
                    sprite.texture = yellow_texture
                    sprite.width = char_size
                    sprite.height = char_size
                    sprite.center_x = start_x + (x_idx * char_size)
                    sprite.center_y = start_y - (y_idx * char_size)
                    sprite.char_type = 'point'  # Метаданные
                    sprite.point_id = len(self.point_sprites)  # ID точки
                    sprite.char_x = x_idx
                    sprite.char_y = y_idx

                    # Можно добавить дополнительные данные
                    sprite.clickable = True
                    sprite.map_data = self.get_map_data(y_idx, x_idx)  # Пример

                    self.point_sprites.append(sprite)
                    self.all_sprites.append(sprite)

    @staticmethod
    @lru_cache(maxsize=2)
    def create_char_texture_cached(r: int, g: int, b: int):
        """Создает текстуру с символом '#' и кеширует"""
        from PIL import Image, ImageDraw, ImageFont

        color = (r, g, b)
        size = 32

        # Создаем изображение
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Шрифт
        font = ImageFont.truetype("cour.ttf", 32)

        # Рисуем #
        bbox = draw.textbbox((0, 0), '#', font=font)
        x = (size - (bbox[2] - bbox[0])) // 2
        y = (size - (bbox[3] - bbox[1])) // 2
        draw.text((x, y), '#', fill=(r, g, b, 255), font=font)

        # Сохраняем в файл
        filename = f"temp_{r}_{g}_{b}.png"
        image.save(filename)

        # Загружаем текстуру
        texture = arcade.load_texture(filename)

        # Удаляем файл
        import os
        os.remove(filename)

        return texture

    def create_char_texture(self, char, color):
        """Обертка для удобства"""
        r, g, b = color[:3]
        return self.create_char_texture_cached(r, g, b)

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.ESCAPE:
            self.close_mapboard()

    def map_textes(self):
        # Дом 1
        map = MAP_DATABASE['dom_1']
        # Название
        self.dom1_title = arcade.Text(
            text=map.name,
            x=680,
            y=490,
            color=arcade.color.WHITE,
            font_size=18,
            font_name='Courier New',
            anchor_x='center',
            anchor_y='center',
            batch=self.batch
        )
        # Координаты
        self.dom1_cords = arcade.Text(
            text=map.cords,
            x=680,
            y=470,
            color=arcade.color.WHITE,
            font_size=8,
            font_name='Courier New',
            anchor_x='center',
            anchor_y='center',
            batch=self.batch
        )
        # Размер
        self.dom1_size = arcade.Text(
            text=f'Размер: {map.size}',
            x=600,
            y=430,
            color=arcade.color.WHITE,
            font_size=10,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='center',
            batch=self.batch
        )
        # С уровня
        self.dom1_on_level = arcade.Text(
            text=f'С уровня: {map.on_level}',
            x=600,
            y=410,
            color=arcade.color.WHITE,
            font_size=10,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='center',
            batch=self.batch
        )
        # Описание
        self.dom1_desc = arcade.Text(  # TODO: Исправить неперенос
            text=map.desc,
            x=600,
            y=390,
            color=arcade.color.WHITE,
            font_size=9,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='center',
            width=1,
            align='center',
            batch=self.batch
        )
        # Дом 3
        map = MAP_DATABASE['dom_3']

        # Кафе
        map = MAP_DATABASE['caffe']

        # Кв.96
        map = MAP_DATABASE['kv_no96']

        # Школа
        map = MAP_DATABASE['school']

        # Бункер
        map = MAP_DATABASE['bunker']

    @staticmethod
    def get_map_data(grid_y, grid_x):
        """Возвращает данные уровня по координатам сетки"""
        # Здесь можешь мапить координаты на ID уровней
        maps = {
            (9, 8): MAP_DATABASE['kv_no96'],
            (8, 18): MAP_DATABASE['caffe'],
            (20, 13): MAP_DATABASE['school'],
            (27, 6): MAP_DATABASE['dom_3'],
            (22, 1): MAP_DATABASE['dom_1'],
            (32, 13): MAP_DATABASE['bunker']
        }

        return maps.get((grid_y, grid_x))

    def show_info_info(self, map_id):
        data = {
            'dom_1': ...,
            'dom_3': ...,
            'caffe': ...,
            'kv_no96': ...,
            'school': ...,
            'bunker': ...,
        }

        for map in data:
            for b in data[map]:
                b = (None, self.batch)[map == map_id]

    def on_point_clicked(self, point_sprite):
        """Обработчик клика на желтую точку"""
        map_data = point_sprite.map_data

        # Визуальная обратная связь
        point_sprite.color = arcade.color.RED  # Подсветка

    def show_map_info(self, point_sprite):
        """Показать информацию о карте"""
        # Поля
        self.name_text = ...
        self.size_text = ...
        self.desc_text = ...
        self.cord_text = ...
        self.on_level_text = ...

    def close_mapboard(self):
        self.window.show_view(self.lobby)

    @staticmethod
    def get_map(arg: 'map' or 'points' = 'map') -> list:
        """Возвращает текстовую карту или точки на ней"""
        lines = []

        with open(f'././assets/txts/{arg}(map_board).txt') as f:
            lines = f.readlines()

        return list(map(lambda x: x.strip('\n'), lines))

# TODO: Сделать инфо-панельку
# TODO: Подключить к _game.json
# TODO: Добавить звуки
# TODO: Почистить код
