import arcade
from pyglet.graphics import Batch

import random

from . import DIFFICULTY_DATABASE
from . import MAP_DATABASE
from ..ui import ITEM_DATABASE

P_EXP_WIN = 100
P_EXP_LOSE = 10

P_CASH_WIN = 200
P_CASH_LOSE = 1

FIRST_DEATH_COEF = 0.8

P_HUNT = 20
P_ZERO_SAN = 20

DIFFICULTIES_COEFS = {
    'peaceful': 0.2,
    'simple': 0.5,
    'normal': 1.0,
    'difficult': 1.4,
    'nightmare': 2.0,
    'madness': 2.5,
    'chaos': 5.0,
}
MAP_SIZE_COEFS = {
    'МАЛЕНЬКАЯ': 1.0,
    'СРЕДНЯЯ': 1.5,
    'БОЛЬШАЯ': 2.0,
    'ОГРОМНАЯ': 3.0
}

LEVEL_EXP = 50


class YesNoWidget():
    ...


class ResultsView(arcade.View):
    SOUNDS = [
        arcade.load_sound('././assets/sounds/effects/print.wav'),
        arcade.load_sound('././assets/sounds/effects/counter.wav'),
        arcade.load_sound('././assets/sounds/effects/cash_counter.wav'),
        arcade.load_sound('././assets/sounds/effects/hover.wav'),
        arcade.load_sound('././assets/sounds/effects/return_lobby.wav')
    ]

    def __init__(self, game):
        super().__init__()
        self.batch = Batch()
        self.camera = arcade.Camera2D(
            projection=arcade.rect.XYWH(0, 0, 800, 600),
            position=(400, 300)
        )
        self.sound_player = None
        self.is_playing = False

        self.game = game

        self.ghost = game.ghost
        self.map_id = game.map_id
        self.dif_id = game.dif_id
        self.inv = game.inv

        self.animation_timer = 0
        self.state_cord = 600
        self.state = True

        # Игрок
        self.lvl = game.player.lvl
        self.cash = game.player.cash
        self.exp = game.player.exp

        self.new_exp = None
        self.new_cash = None
        self.comp = None
        self.get_results()

        from database import ProfileManager
        self.profile = ProfileManager()

        self.account = game.account

        # Кнопка
        self.can_click = False
        self.on_hover = False

        # Полоска
        self.line_width = 1

        self.set_texts()

    def get_results(self):
        """

        EXP: (WIN/LOSE + P_HUNT + P_ZERO_SAN) * (DIFF_COEF * MAP_COEF * F_LOSE_COEF)
        CASH: (WIN/LOSE + P_HUNT + P_ZERO_SAN) * (DIFF_COEF * MAP_COEF * F_LOSE_COEF) + COMPENSATION(OPT)

        """

        # Игровое
        is_win = self.game.is_win
        p_hunt = self.game.was_hunt
        p_zero_san = self.game.was_zero_sanity

        # Коэффициенты
        map_coef = MAP_SIZE_COEFS[MAP_DATABASE[self.game.map_id].size]
        diff_coef = DIFFICULTIES_COEFS[self.dif_id]
        f_lose_coef = self.game.was_first_death

        # Компенсация
        default_items = ('emf', 'low_light', 'dict', 'term', 'mic', 'book')
        comp = sum(map(lambda x: (self.inv[x] - (1 if x in default_items else 0)) * ITEM_DATABASE[x].price, self.inv))
        self.comp = int((0, comp * 0.25)[self.game.was_death and comp >= 1000])

        # EXP
        self.new_exp = int(((P_EXP_LOSE, P_EXP_WIN)[is_win] + (0, P_HUNT)[p_hunt] + (0, P_ZERO_SAN)[p_zero_san]) * (
                map_coef * diff_coef * (1, f_lose_coef)[f_lose_coef]))

        # cash
        self.new_cash = int(((P_CASH_LOSE, P_CASH_WIN)[is_win] + (0, P_HUNT)[p_hunt] + (0, P_ZERO_SAN)[p_zero_san]) * (
                map_coef * diff_coef * (1, f_lose_coef)[f_lose_coef]) + self.comp)

    def give_away_items(self):
        if not self.game.was_death:
            default_items = ('emf', 'low_light', 'dict', 'term', 'mic', 'book')
            for item_id, item_count in self.inv.items():
                if item_count > 0:
                    self.profile.update_inventory(
                        self.account.current_account,
                        item_id,
                        item_count - (1 if item_id in default_items else 0),
                        operation='add'
                    )

        # Обновляем деньги игрока
        total_cash = self.cash + self.new_cash
        self.profile.update_cash(
            self.account.current_account,
            total_cash,
            operation='set'
        )

        # Обновляем опыт и уровень
        self.profile.update_experience(
            self.account.current_account,
            self.exp
        )

        self.profile.update_level(
            self.account.current_account,
            self.lvl
        )

    def set_texts(self):
        # Тайтл
        lst = list('aGVscCE=')
        random.shuffle(lst)
        self.title = arcade.Text(
            text=('Вы мертвы', ''.join(lst), 'Поздравляем')[0 if self.game.was_death else self.game.is_win + 1],
            x=150 + 150, y=530 + self.state_cord,
            color=arcade.color.BLACK,
            font_size=20,
            font_name='Courier New',
            anchor_x='center',
            anchor_y='center',
            batch=self.batch
        )

        # Призрак
        self.ghost_text = arcade.Text(
            text=f'{('Призрак',)[0]}: {self.ghost}.',
            x=160, y=440 + self.state_cord,
            color=arcade.color.BLACK,
            font_size=16,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='bottom',
            batch=self.batch
        )

        # Lvl
        self.lvl_text = arcade.Text(
            text=f'Lvl: {self.lvl}.',
            x=160, y=390 + self.state_cord,
            color=arcade.color.BLACK,
            font_size=16,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='bottom',
            batch=self.batch
        )

        # exp
        self.exp_text = arcade.Text(
            text=f'exp: {self.exp}/{LEVEL_EXP * self.lvl} ',
            x=160, y=375 + self.state_cord,
            color=arcade.color.BLACK,
            font_size=9 if 0 <= self.lvl * LEVEL_EXP <= 999 else 8 if 1000 <= self.lvl * LEVEL_EXP <= 9990 else 7,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='bottom',
            batch=self.batch
        )

        # Баланс
        self.cash_text = arcade.Text(
            text=f'Баланс: {self.cash}$.',
            x=160, y=340 + self.state_cord,
            color=arcade.color.BLACK,
            font_size=16,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='bottom',
            batch=self.batch
        )

        # Точки
        self.dot_text1 = arcade.Text(
            text='...',
            x=160, y=290 + self.state_cord,
            color=arcade.color.BLACK,
            font_size=16,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='bottom',
            batch=self.batch
        )

        self.dot_text2 = arcade.Text(
            text='...',
            x=160, y=240 + self.state_cord,
            color=arcade.color.BLACK,
            font_size=16,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='bottom',
            batch=self.batch
        )

        # Компенсация
        self.comp_text = arcade.Text(
            text=f'Страховка: {self.comp}$.' if self.game.was_death else '',
            x=160, y=190 + self.state_cord,
            color=arcade.color.BLACK,
            font_size=16,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='bottom',
            batch=self.batch
        )

    def on_draw(self) -> bool | None:
        self.clear()

        self.camera.use()

        # Листик
        arcade.draw_rect_filled(
            arcade.rect.LBWH(150, 20 + self.state_cord, 300, 560),
            color=(240, 240, 240)
        )
        arcade.draw_line(150, 560 + self.state_cord, 450, 560 + self.state_cord, color=arcade.color.BLACK,
                         line_width=3.5)
        arcade.draw_line(150, 500 + self.state_cord, 450, 500 + self.state_cord, color=arcade.color.BLACK,
                         line_width=3.5)

        # Подчеркивания
        arcade.draw_line(160, 440 + self.state_cord, 255, 440 + self.state_cord, color=arcade.color.BLACK, line_width=2)

        # Кнопка
        color = (50, 50, 50)
        if self.on_hover:
            color = (70, 70, 70)
        arcade.draw_rect_filled(
            arcade.rect.XYWH(625, 300, 50, 50),
            color=color
        )
        arcade.draw_line(625 - 20, 300 + 10, 625 - 5, 300 - 15,
                         color=arcade.color.WHITE)
        arcade.draw_line(625 - 5, 300 - 15, 625 + 20, 300 + 15,
                         color=arcade.color.WHITE)

        # Полоса exp
        arcade.draw_line(249, 385 + self.state_cord, 250 + self.line_width, 385 + self.state_cord,
                         color=arcade.color.BLACK, line_width=5)

        self.set_texts()

        self.batch.draw()

    def on_update(self, delta_time: float) -> bool | None:
        if not self.state:
            if self.new_exp:
                if not self.is_playing:
                    self.sound_player = arcade.play_sound(self.SOUNDS[1], loop=True)
                    self.is_playing = True
                self.exp = min(self.exp + 1, LEVEL_EXP * self.lvl)
                if self.exp == LEVEL_EXP * self.lvl:
                    self.lvl += 1
                    self.exp = 0
                self.new_exp -= 1
                self.line_width = self.exp / (self.lvl * LEVEL_EXP) * 190
            else:
                self.sound_player.pause()
                self.is_playing = False

            if self.new_cash and not self.new_exp:
                if not self.is_playing:
                    self.sound_player = arcade.play_sound(self.SOUNDS[2], loop=True)
                    self.is_playing = True
                self.cash += 1
                self.new_cash -= 1
            else:
                if not self.new_exp:
                    self.sound_player.pause()
                    self.is_playing = False

            if self.new_exp == self.new_cash == 0:
                self.can_click = True
            return

        if self.state_cord != 0:
            if not self.is_playing:
                self.sound_player = arcade.play_sound(self.SOUNDS[0], loop=True)
                self.is_playing = True
            self.state_cord -= 3
        if self.state_cord <= 0:
            self.sound_player.pause()
            self.is_playing = False
            self.state_cord = 0
            self.state = False

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        w = self.camera.unproject((x, y))
        print(w.x, w.y)
        if self.state:
            return

        if (w.x, w.y) in arcade.rect.XYWH(625, 300, 50, 50) and self.can_click:
            arcade.play_sound(self.SOUNDS[4])
            self.open_lobby()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> bool | None:
        w = self.camera.unproject((x, y))

        if (w.x, w.y) in arcade.rect.XYWH(625, 300, 50, 50) and self.can_click:
            if not self.on_hover:
                arcade.play_sound(self.SOUNDS[3])
            self.on_hover = True
        else:
            self.on_hover = False

    def open_lobby(self):
        self.give_away_items()

        print(':)')
        from ..maps import LobbyView
        lobby_view = LobbyView(self.account)
        self.window.show_view(lobby_view)
