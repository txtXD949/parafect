import json
from functools import lru_cache

import arcade
from pyglet.graphics import Batch


class MapInfo:
    def __init__(self, id, name, size, desc, cords, on_level=1):
        self.id: int = id
        self.name: str = name
        self.size: str = size
        self.desc: str = desc
        self.cords: str = cords
        self.on_level: int = on_level


MAP_DATABASE = {
    'dom_1': MapInfo(
        id='0',
        name='ДОМ 1',
        size='МАЛЕНЬКАЯ',
        cords='38.279567°N, -122.009865°E',
        desc='"Они переехали через месяц. Говорят, ребёнок всё время разговаривал с кем-то в углу."',
    ),
    'dom_3': MapInfo(
        id='1',
        name='ДОМ 3',
        size='СРЕДНЯЯ',
        cords='38.349100°N, -121.956000°E',
        desc='"Местные обходят это место. Говорят, ночью в окнах виден свет, хотя электричество отключено ещё в 90-х."',
        on_level=5
    ),
    'caffe': MapInfo(
        id='2',
        name='КАФЕ',
        size='СРЕДНЯЯ',
        cords='34.163680°N, -117.904245°E',
        desc='"Бармен жаловался, на посетителя, который несколько часов пил один кофе в углу. На камерах никого не было видно."',
        on_level=10
    ),
    'kv_no96': MapInfo(
        id='3',
        name='КВАРТИРА №96',
        size='СРЕДНЯЯ',
        cords='58.630501°N, 59.789185°E',
        desc='"Жильцы писали коллективную жалобу на соседа, который стучал по батареям, в двери и моргал светом ночами. Этот сосед умер в 1989."',
        on_level=15
    ),
    'school': MapInfo(
        id='4',
        name='ШКОЛА',
        size='БОЛЬШАЯ',
        cords='57.874040°N, 59.949528°E',
        desc='"Школа была закрыта давно по неизвестным причинам. Власти не торопятся ее сносить."',
        on_level=20
    ),
    'bunker': MapInfo(
        id='5',
        name='БУНКЕР',
        size='ОГРОМНАЯ',
        cords='68.925214°N, 33.089326°E',
        desc='"Группа исследователей сообщила, что видела свои же трупы. Больше сообщений от них не поступало."',
        on_level=30
    )
}


class MapBoard(arcade.View):
    def __init__(self, lobby=None, account_manager=None):
        super().__init__()
        self.background_color = arcade.color.BLACK

        self.lobby = lobby

        # Профиль
        from database import ProfileManager
        self.account = account_manager
        self.profile = ProfileManager()

        # Игрок
        self.player_level = None

        # Временный выбор карты
        self.game_state_path = '././database/_game.json'
        self.game_state = None

        # Спрайт-листы
        self.map_sprites = arcade.SpriteList()  # Белые #
        self.point_sprites = arcade.SpriteList()  # Желтые #
        self.all_sprites = arcade.SpriteList()  # Все вместе

        # Загружаем и создаем спрайты
        self.create_map_sprites()

        # Камера
        self.camera = None

        # UI
        self.batch = Batch()
        self.setup()

    def setup(self):
        # Камера
        self.camera = arcade.Camera2D(
            projection=arcade.rect.XYWH(0, 0, 800, 600),
            position=(400, 300)
        )
        self.camera.viewport_width = self.width
        self.camera.viewport_height = self.height

        # Уровень
        profile = self.profile.load_profile(self.account.current_account)
        self.player_level = profile['level']

        # Создаем или загружаем карту
        self.load_game_state()

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

        # Уровень игрока
        self.text_lvl = arcade.Text(
            text=f'Lvl: {self.player_level}',
            x=35,
            y=485,
            color=arcade.color.WHITE,
            font_size=14,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='top',
            batch=self.batch
        )

    def on_show_view(self) -> None:
        self.__init__(self.lobby, self.account)
        profile = self.profile.load_profile(self.account.current_account)
        self.player_level = profile['level']

    def get_map_texts_dom_1(self):
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
            batch=None
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
            batch=None
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
            batch=None
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
            batch=None
        )
        # Описание
        self.dom1_desc = arcade.Text(
            text=map.desc,
            x=600,
            y=320,
            color=arcade.color.Color.from_hex_string('#C8C8C8'),
            font_size=9,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='bottom',
            width=160,
            align='left',
            multiline=True,
            batch=None
        )

        return self.dom1_title, self.dom1_cords, self.dom1_size, self.dom1_on_level, self.dom1_desc

    def get_map_texts_dom_3(self):
        # Дом 3
        map = MAP_DATABASE['dom_3']

        # Название
        self.dom3_title = arcade.Text(
            text=map.name,
            x=680,
            y=490,
            color=arcade.color.WHITE,
            font_size=18,
            font_name='Courier New',
            anchor_x='center',
            anchor_y='center',
            batch=None
        )
        # Координаты
        self.dom3_cords = arcade.Text(
            text=map.cords,
            x=680,
            y=470,
            color=arcade.color.WHITE,
            font_size=8,
            font_name='Courier New',
            anchor_x='center',
            anchor_y='center',
            batch=None
        )
        # Размер
        self.dom3_size = arcade.Text(
            text=f'Размер: {map.size}',
            x=600,
            y=430,
            color=arcade.color.WHITE,
            font_size=10,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='center',
            batch=None
        )
        # С уровня
        self.dom3_on_level = arcade.Text(
            text=f'С уровня: {map.on_level}',
            x=600,
            y=410,
            color=arcade.color.WHITE,
            font_size=10,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='center',
            batch=None
        )
        # Описание
        self.dom3_desc = arcade.Text(
            text=map.desc,
            x=600,
            y=320,
            color=arcade.color.Color.from_hex_string('#C8C8C8'),
            font_size=9,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='bottom',
            width=160,
            align='left',
            multiline=True,
            batch=None
        )

        return self.dom3_title, self.dom3_cords, self.dom3_size, self.dom3_on_level, self.dom3_desc

    def get_map_texts_caffe(self):
        # Кафе
        map = MAP_DATABASE['caffe']

        # Название
        self.caffe_title = arcade.Text(
            text=map.name,
            x=680,
            y=490,
            color=arcade.color.WHITE,
            font_size=18,
            font_name='Courier New',
            anchor_x='center',
            anchor_y='center',
            batch=None
        )
        # Координаты
        self.caffe_cords = arcade.Text(
            text=map.cords,
            x=680,
            y=470,
            color=arcade.color.WHITE,
            font_size=8,
            font_name='Courier New',
            anchor_x='center',
            anchor_y='center',
            batch=None
        )
        # Размер
        self.caffe_size = arcade.Text(
            text=f'Размер: {map.size}',
            x=600,
            y=430,
            color=arcade.color.WHITE,
            font_size=10,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='center',
            batch=None
        )
        # С уровня
        self.caffe_on_level = arcade.Text(
            text=f'С уровня: {map.on_level}',
            x=600,
            y=410,
            color=arcade.color.WHITE,
            font_size=10,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='center',
            batch=None
        )
        # Описание
        self.caffe_desc = arcade.Text(
            text=map.desc,
            x=600,
            y=305,
            color=arcade.color.Color.from_hex_string('#C8C8C8'),
            font_size=9,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='bottom',
            width=160,
            align='left',
            multiline=True,
            batch=None
        )

        return self.caffe_title, self.caffe_cords, self.caffe_size, self.caffe_on_level, self.caffe_desc

    def get_map_texts_kv_no96(self):
        # Кв.96
        map = MAP_DATABASE['kv_no96']

        # Название
        self.kv_no96_title = arcade.Text(
            text=map.name,
            x=680,
            y=490,
            color=arcade.color.WHITE,
            font_size=18,
            font_name='Courier New',
            anchor_x='center',
            anchor_y='center',
            batch=None
        )
        # Координаты
        self.kv_no96_cords = arcade.Text(
            text=map.cords,
            x=680,
            y=470,
            color=arcade.color.WHITE,
            font_size=8,
            font_name='Courier New',
            anchor_x='center',
            anchor_y='center',
            batch=None
        )
        # Размер
        self.kv_no96_size = arcade.Text(
            text=f'Размер: {map.size}',
            x=600,
            y=430,
            color=arcade.color.WHITE,
            font_size=10,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='center',
            batch=None
        )
        # С уровня
        self.kv_no96_on_level = arcade.Text(
            text=f'С уровня: {map.on_level}',
            x=600,
            y=410,
            color=arcade.color.WHITE,
            font_size=10,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='center',
            batch=None
        )
        # Описание
        self.kv_no96_desc = arcade.Text(
            text=map.desc,
            x=600,
            y=290,
            color=arcade.color.Color.from_hex_string('#C8C8C8'),
            font_size=9,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='bottom',
            width=160,
            align='left',
            multiline=True,
            batch=None
        )

        return self.kv_no96_title, self.kv_no96_cords, self.kv_no96_size, self.kv_no96_on_level, self.kv_no96_desc

    def get_map_texts_school(self):
        # Школа
        map = MAP_DATABASE['school']

        # Название
        self.school_title = arcade.Text(
            text=map.name,
            x=680,
            y=490,
            color=arcade.color.WHITE,
            font_size=18,
            font_name='Courier New',
            anchor_x='center',
            anchor_y='center',
            batch=None
        )
        # Координаты
        self.school_cords = arcade.Text(
            text=map.cords,
            x=680,
            y=470,
            color=arcade.color.WHITE,
            font_size=8,
            font_name='Courier New',
            anchor_x='center',
            anchor_y='center',
            batch=None
        )
        # Размер
        self.school_size = arcade.Text(
            text=f'Размер: {map.size}',
            x=600,
            y=430,
            color=arcade.color.WHITE,
            font_size=10,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='center',
            batch=None
        )
        # С уровня
        self.school_on_level = arcade.Text(
            text=f'С уровня: {map.on_level}',
            x=600,
            y=410,
            color=arcade.color.WHITE,
            font_size=10,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='center',
            batch=None
        )
        # Описание
        self.school_desc = arcade.Text(
            text=map.desc,
            x=600,
            y=330,
            color=arcade.color.Color.from_hex_string('#C8C8C8'),
            font_size=9,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='bottom',
            width=160,
            align='left',
            multiline=True,
            batch=None
        )

        return self.school_title, self.school_cords, self.school_size, self.school_on_level, self.school_desc

    def get_map_texts_bunker(self):
        # Бункер
        map = MAP_DATABASE['bunker']

        # Название
        self.bunker_title = arcade.Text(
            text=map.name,
            x=680,
            y=490,
            color=arcade.color.WHITE,
            font_size=18,
            font_name='Courier New',
            anchor_x='center',
            anchor_y='center',
            batch=None
        )
        # Координаты
        self.bunker_cords = arcade.Text(
            text=map.cords,
            x=680,
            y=470,
            color=arcade.color.WHITE,
            font_size=8,
            font_name='Courier New',
            anchor_x='center',
            anchor_y='center',
            batch=None
        )
        # Размер
        self.bunker_size = arcade.Text(
            text=f'Размер: {map.size}',
            x=600,
            y=430,
            color=arcade.color.WHITE,
            font_size=10,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='center',
            batch=None
        )
        # С уровня
        self.bunker_on_level = arcade.Text(
            text=f'С уровня: {map.on_level}',
            x=600,
            y=410,
            color=arcade.color.WHITE,
            font_size=10,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='center',
            batch=None
        )
        # Описание
        self.bunker_desc = arcade.Text(
            text=map.desc,
            x=600,
            y=320,
            color=arcade.color.Color.from_hex_string('#C8C8C8'),
            font_size=9,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='bottom',
            width=160,
            align='left',
            multiline=True,
            batch=None
        )

        return self.bunker_title, self.bunker_cords, self.bunker_size, self.bunker_on_level, self.bunker_desc

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

    def on_update(self, delta_time: float) -> bool | None:
        profile = self.profile.load_profile(self.account.current_account)
        self.player_level = profile['level']
        self.text_lvl.text = f'Lvl: {self.player_level}'

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        # Мировые координаты
        world_pos = self.camera.unproject((x, y))

        # Закрытие доски
        if 300 <= world_pos.x <= 330 and 70 <= world_pos.y <= 80:
            self.close_mapboard()

        # Желтые точки
        clicked_points = arcade.get_sprites_at_point(
            (world_pos.x, world_pos.y),
            self.point_sprites
        )

        if clicked_points:
            for point in clicked_points:
                self.show_info_info(point.map_id)
                self.on_point_clicked(point)
            return

        print(f"Клик: {world_pos}")

    def create_map_sprites(self):
        """Создает спрайты для карты и точек"""
        map_lines = self.get_map(arg='map')
        point_lines = self.get_map(arg='points')

        # Позиции
        char_size = 16.5
        start_x = 23
        start_y = 450

        # Создание текстур
        white_texture = self.create_char_texture('#', arcade.color.WHITE)
        yellow_texture = self.create_char_texture('#', arcade.color.YELLOW)
        red_texture = self.create_char_texture('#', arcade.color.RED)

        # Белые #
        for y_idx, line in enumerate(map_lines):
            for x_idx, char in enumerate(line):
                if char == '#':
                    sprite = arcade.Sprite()
                    sprite.texture = white_texture
                    sprite.width = char_size
                    sprite.height = char_size
                    sprite.center_x = start_x + (x_idx * char_size)
                    sprite.center_y = start_y - (y_idx * char_size)
                    sprite.char_type = 'map'
                    sprite.char_x = x_idx
                    sprite.char_y = y_idx

                    self.map_sprites.append(sprite)
                    self.all_sprites.append(sprite)

        # Желтые #
        for y_idx, line in enumerate(point_lines):
            for x_idx, char in enumerate(line):
                if char == '#':
                    sprite = arcade.Sprite()
                    sprite.texture = yellow_texture
                    sprite.width = char_size
                    sprite.height = char_size
                    sprite.center_x = start_x + (x_idx * char_size)
                    sprite.center_y = start_y - (y_idx * char_size)
                    sprite.char_type = 'point'
                    sprite.point_id = len(self.point_sprites)
                    sprite.char_x = x_idx
                    sprite.char_y = y_idx

                    # Даем цвет
                    player_lvl = self.profile.load_profile(self.account.current_account)['level']
                    map_info = MAP_DATABASE[self.get_map_key_by_id(self.get_map_id(x_idx, y_idx))]

                    if player_lvl >= map_info.on_level:
                        sprite.texture = yellow_texture
                        sprite.color = arcade.color.YELLOW
                        sprite.original_color = arcade.color.YELLOW
                    else:
                        sprite.texture = red_texture
                        sprite.color = arcade.color.RED
                        sprite.original_color = arcade.color.RED

                    sprite.map_id = self.get_map_id(x_idx, y_idx)

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
        r, g, b = color[:3]
        return self.create_char_texture_cached(r, g, b)

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.ESCAPE:
            self.close_mapboard()

    @staticmethod
    def get_map_id(grid_y, grid_x):
        """Возвращает данные уровня по координатам сетки"""
        # Мапинг координат
        maps = {
            (9, 8): MAP_DATABASE['kv_no96'].id,
            (8, 18): MAP_DATABASE['caffe'].id,
            (20, 13): MAP_DATABASE['school'].id,
            (27, 6): MAP_DATABASE['dom_3'].id,
            (22, 1): MAP_DATABASE['dom_1'].id,
            (32, 13): MAP_DATABASE['bunker'].id
        }

        return maps.get((grid_y, grid_x))

    def show_info_info(self, map_id):
        data = {
            MAP_DATABASE['dom_1'].id: self.get_map_texts_dom_1(),
            MAP_DATABASE['dom_3'].id: self.get_map_texts_dom_3(),
            MAP_DATABASE['caffe'].id: self.get_map_texts_caffe(),
            MAP_DATABASE['kv_no96'].id: self.get_map_texts_kv_no96(),
            MAP_DATABASE['school'].id: self.get_map_texts_school(),
            MAP_DATABASE['bunker'].id: self.get_map_texts_bunker(),
        }

        for i in data:
            for text in data[i]:
                try:
                    text.batch = (None, self.batch)[i == map_id]
                except Exception:
                    pass

    def on_point_clicked(self, point_sprite):
        """Обработчик клика на желтую/красную точку"""

        # id карты
        map_id = self.get_map_id(point_sprite.char_x, point_sprite.char_y)
        map_key = self.get_map_key_by_id(map_id)
        map_info = MAP_DATABASE[map_key]

        # Информация о карте
        self.show_info_info(map_id)

        # Сброс все цвета к исходным
        for point in self.point_sprites:
            point.color = point.original_color

        # Проверка карты на доступность
        if self.player_level >= map_info.on_level:
            point_sprite.color = arcade.color.DARK_YELLOW
            self.game_state['map'] = map_key
            self.save_game_state()

    def load_game_state(self):
        try:
            with open(self.game_state_path, 'r', encoding='utf-8') as f:
                self.game_state = json.load(f)
        except FileNotFoundError:
            self.game_state = {'inventory': {}, 'map': None, 'difficulty': None}
            self.save_game_state()

    def get_map_key_by_id(self, map_id):
        """Возвращает ключ карты по её ID (например, 'dom_1' для id='0')"""
        for key, map_info in MAP_DATABASE.items():
            if map_info.id == map_id:  # Сравниваем строки '0' == '0'
                return key
        return

    def save_game_state(self):
        """Сохраняет состояние игры в файл"""
        with open(self.game_state_path, 'w', encoding='utf-8') as f:
            json.dump(self.game_state, f, ensure_ascii=False, indent=2)

    def close_mapboard(self):
        self.window.show_view(self.lobby)

    @staticmethod
    def get_map(arg: 'map' or 'points' = 'map') -> list:
        """Возвращает текстовую карту или точки на ней"""
        lines = []

        with open(f'././assets/txts/{arg}(map_board).txt') as f:
            lines = f.readlines()

        return list(map(lambda x: x.strip('\n'), lines))

# TODO: Добавить звуки
