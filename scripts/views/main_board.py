import arcade
from pyglet.graphics import Batch
from arcade.gui import UIManager

from itertools import cycle


class DifficultyInfo:
    def __init__(self, name, desc, sanity, broke_chance, roomchange_chance, evidence_count, on_level=1):
        self.name: str = name
        self.desc: str = desc
        self.sanity: str = sanity
        self.broke_chance: str = broke_chance
        self.roomchange_chance: str = roomchange_chance
        self.evidence_count: int = evidence_count
        self.on_level: int = on_level


DIFFICULTY_DATABASE = {
    'peaceful': DifficultyInfo(
        name='Мирный',
        desc='Ознакомительный режим, призраки не начинают охоту.',
        sanity='100%',
        broke_chance='0%',
        roomchange_chance='0%',
        evidence_count=3,
        on_level=1
    ),
    'simple': DifficultyInfo(
        name='Легкий',
        desc='Подходит для новичков.',
        sanity='100%',
        broke_chance='10%',
        roomchange_chance='0%',
        evidence_count=3,
        on_level=1
    ),
    'normal': DifficultyInfo(
        name='Нормальный',
        desc='Стандартный уровень сложности.',
        sanity='100%',
        broke_chance='30%',
        roomchange_chance='25%',
        evidence_count=3,
        on_level=1
    ),
    'difficult': DifficultyInfo(
        name='Сложный',
        desc='Призрак более агрессивен. Для продвинутых игроков',
        sanity='85%',
        broke_chance='50%',
        roomchange_chance='35%',
        evidence_count=3,
        on_level=10
    ),
    'nightmare': DifficultyInfo(
        name='Кошмар',
        desc='Призрак настроен убить вас, будь аккуратнее. Для профессиональных игроков',
        sanity='25%',
        broke_chance='70%',
        roomchange_chance='50%',
        evidence_count=2,
        on_level=20
    ),
    'madness': DifficultyInfo(
        name='Безумие',
        desc='Призрак обезумел и не даст тебе шансов.',
        sanity='10%',
        broke_chance='85%',
        roomchange_chance='60%',
        evidence_count=1,
        on_level=30
    ),
    'chaos': DifficultyInfo(
        name='Хаос',
        desc='Призрак совсем в бешенстве. У тебя нет шансов…',
        sanity='1%',
        broke_chance='99%',
        roomchange_chance='99%',
        evidence_count=0,
        on_level=50
    ),
}


class MainBoard(arcade.View):
    def __init__(self, lobby=None, account_manager=None):
        super().__init__()
        self.background_color = arcade.color.BLACK

        self.lobby = lobby
        self.account = account_manager

        self.camera = None

        self.batch = None

        self.setup()

    def setup(self):
        # Batch
        self.batch = Batch()

        # Подгрузка текстов
        self.set_gui_texts()
        self.set_profile_texts()
        self.set_info_game_texts()

        # UI
        from ..ui import ChangeButton
        self.btn = ChangeButton(
            values=[' '] + list(map(lambda x: DIFFICULTY_DATABASE[x].name, DIFFICULTY_DATABASE.keys())),
            start_x=590,
            start_y=460,
            font_size=20,
            font_name='Courier New',
            color=arcade.color.WHITE,
            batch=self.batch,
        )

        # Камера
        self.camera = arcade.Camera2D(
            projection=arcade.rect.XYWH(0, 0, 800, 600),
            position=(400, 300)
        )
        self.camera.viewport_width = self.width
        self.camera.viewport_height = self.height

    def set_gui_texts(self):
        """Тексты: ИГРА/СЛОЖНОСТЬ"""
        # ИГРА
        self.game_text = arcade.Text(
            text='ИГРА',
            x=365 / 2 + 30,
            y=600 - 30 - 20,
            color=arcade.color.WHITE,
            font_name='Courier New',
            font_size=22,
            anchor_x='center',
            anchor_y='center',
            batch=self.batch
        )

        # СЛОЖНОСТЬ
        self.difficulty_text_ = arcade.Text(
            text='СЛОЖНОСТЬ',
            x=800 - 365 / 2 - 30,
            y=600 - 30 - 20,
            color=arcade.color.WHITE,
            font_name='Courier New',
            font_size=22,
            anchor_x='center',
            anchor_y='center',
            batch=self.batch
        )

    def set_profile_texts(self, name='test_name', lvl=1000):
        """Тексты: ник/уровень"""
        # Ник
        self.name_text = arcade.Text(
            text=name,
            x=45 + 30 + 10,
            y=465 + 15,
            color=arcade.color.WHITE,
            font_name='Courier New',
            font_size=15,
            anchor_x='left',
            anchor_y='center',
            batch=self.batch
        )

        # Уровень
        self.lvl_text = arcade.Text(
            text=f'Lvl: {lvl}',
            x=290,
            y=465 + 15,
            color=arcade.color.WHITE,
            font_name='Courier New',
            font_size=12,
            anchor_x='left',
            anchor_y='center',
            batch=self.batch
        )

    def set_info_game_texts(self, map='...', difficulty='...'):
        """Тексты: карта/сложность/играть"""
        # Карта
        self.map_text = arcade.Text(
            text=f'Карта: {map}.',
            x=40,
            y=225 - 20,
            color=arcade.color.WHITE,
            font_name='Courier New',
            font_size=14,
            anchor_x='left',
            anchor_y='center',
            batch=self.batch
        )

        # Сложность
        self.difficulty_text = arcade.Text(
            text=f'Сложность: {difficulty}.',
            x=40,
            y=225 - 50,
            color=arcade.color.WHITE,
            font_name='Courier New',
            font_size=14,
            anchor_x='left',
            anchor_y='center',
            batch=self.batch
        )

        # Кнопка играть
        arcade.load_font('././assets/fonts/CorrectionTape.otf')
        self.play_text = arcade.Text(
            text=f'Играть',
            x=365 / 2 + 30,
            y=120,
            color=arcade.color.WHITE,
            font_name='Correction Tape',
            font_size=24,
            anchor_x='center',
            anchor_y='center',
            batch=self.batch
        )

    def set_difficulty_texts(self, difficulty_name):
        """Тексты: название/описание/рассудок/шансы/улики/на уровне/???"""
        chosen = False
        try:
            info = next(DIFFICULTY_DATABASE[it] for it in DIFFICULTY_DATABASE.keys() if
                        DIFFICULTY_DATABASE[it].name == difficulty_name)
            desc, sanity, broke_chance, roomchange_chance, evidence_count, on_level = \
                (
                    info.desc, f'Начальный уровень рассудка: {info.sanity}.',
                    f'Призрак ломает укрытия с шансом {info.broke_chance}.',
                    f'Призрак меняет комнату с шансом {info.roomchange_chance}.',
                    f'Количество улик: {info.evidence_count}.',
                    f'На уровне {info.on_level}.'
                )
            chosen = True
        except StopIteration:
            desc = sanity = broke_chance = roomchange_chance = evidence_count = on_level = ''

        # Описание
        self.name_text1 = arcade.Text(
            text=desc,
            x=430,
            y=380,
            color=arcade.color.Color.from_hex_string('#C8C8C8'),
            font_name='Courier New',
            font_size=9,
            anchor_x='left',
            anchor_y='top',
            align='left',
            width=310,
            multiline=True,
            batch=self.batch
        )

        # Рассудок
        self.sanity_text = arcade.Text(
            text=sanity,
            x=430,
            y=380 - 50,
            color=arcade.color.WHITE,
            font_name='Courier New',
            font_size=11,
            anchor_x='left',
            anchor_y='top',
            align='left',
            width=310,
            multiline=True,
            batch=self.batch
        ),

        # Шансы
        self.broke_chance_text = arcade.Text(
            text=broke_chance,
            x=430,
            y=380 - 70,
            color=arcade.color.WHITE,
            font_name='Courier New',
            font_size=11,
            anchor_x='left',
            anchor_y='top',
            align='left',
            width=310,
            multiline=True,
            batch=self.batch
        ),

        self.roomchange_chance_text = arcade.Text(
            text=roomchange_chance,
            x=430,
            y=380 - 90,
            color=arcade.color.WHITE,
            font_name='Courier New',
            font_size=11,
            anchor_x='left',
            anchor_y='top',
            align='left',
            width=310,
            multiline=True,
            batch=self.batch
        ),

        # Улики
        self.evidence_count_text = arcade.Text(
            text=evidence_count,
            x=430,
            y=380 - 110,
            color=arcade.color.WHITE,
            font_name='Courier New',
            font_size=11,
            anchor_x='left',
            anchor_y='top',
            align='left',
            width=310,
            multiline=True,
            batch=self.batch
        ),

        # На уровне
        self.on_level_text = arcade.Text(
            text=on_level,
            x=430,
            y=380 - 130,
            color=arcade.color.WHITE,
            font_name='Courier New',
            font_size=11,
            anchor_x='left',
            anchor_y='top',
            align='left',
            width=310,
            multiline=True,
            batch=self.batch
        )

    def on_draw(self) -> bool | None:
        self.clear()

        self.camera.use()

        # Рамка
        arcade.draw_line(20, 20, 780, 20, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(20, 20, 20, 580, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(20, 580, 780, 580, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(780, 20, 780, 580, color=arcade.color.WHITE, line_width=1)

        # Панелька "инфо игрока"
        arcade.draw_line(30, 30, 395, 30, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(30, 30, 30, 570, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(30, 570, 395, 570, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(395, 30, 395, 570, color=arcade.color.WHITE, line_width=1)
        arcade.draw_rect_filled(arcade.rect.LBWH(30, 30, 365, 540), color=(30, 30, 30))

        # Панелька сложность
        arcade.draw_line(405, 30, 770, 30, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(405, 30, 405, 570, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(405, 570, 770, 570, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(770, 30, 770, 570, color=arcade.color.WHITE, line_width=1)
        arcade.draw_rect_filled(arcade.rect.LBWH(405, 30, 365, 540), color=(30, 30, 30))

        # Панелька "инфо сложность"
        arcade.draw_line(415, 40, 760, 40, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(415, 40, 415, 400, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(415, 400, 760, 400, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(760, 40, 760, 400, color=arcade.color.WHITE, line_width=1)
        arcade.draw_rect_filled(arcade.rect.LBWH(415, 40, 345, 360), color=(25, 25, 25))

        # Профиль игрока
        # Рамка
        arcade.draw_line(40, 460, 385, 460, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(40, 460, 40, 500, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(40, 500, 385, 500, color=arcade.color.WHITE, line_width=1)
        arcade.draw_line(385, 460, 385, 500, color=arcade.color.WHITE, line_width=1)
        arcade.draw_rect_filled(arcade.rect.LBWH(40, 460, 345, 40), color=(25, 25, 25))

        # Аватарка (белый квадратик, так как одиночный)
        arcade.draw_lbwh_rectangle_filled(45, 465, 30, 30, color=arcade.color.WHITE)
        arcade.draw_lbwh_rectangle_outline(45, 465, 30, 30, color=arcade.color.BLACK)

        # Выход из доски
        arcade.draw_line(365 / 2 + 30, 60, 365 / 2 + 30 + 15, 70, color=arcade.color.WHITE)
        arcade.draw_line(365 / 2 + 30, 60, 365 / 2 + 30 - 15, 70, color=arcade.color.WHITE)

        self.batch.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        # Мировые координаты
        world_pos = self.camera.unproject((x, y))

        print(world_pos.x, world_pos.y)

        # Закрытие доски
        if 195 <= world_pos.x <= 225 and 60 <= world_pos.y <= 70:
            self.close_mainboard()

        # Старт игры
        if 155 <= world_pos.x <= 270 and 105 <= world_pos.y <= 135:
            self.start_game()

        if self.btn.on_mouse_press(world_pos.x, world_pos.y, button, modifiers):
            self.set_difficulty_texts(self.btn.value)
            print(f"Значение: {self.btn.value}")

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.ESCAPE:
            self.close_mainboard()

    def close_mainboard(self):
        self.window.show_view(self.lobby)

    def start_game(self):
        print('Начинаем игру...')

# TODO: Подключить к _game.json
# TODO: Добавить звуки
# TODO: ??? для тех, где уровень игрока ниже
# TODO: Скрывать "на уровне" при уровне выше
# TODO: Почистить код
# TODO:
