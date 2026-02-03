import random

import arcade
from pyglet.graphics import Batch

from ..sounds import BOARD_2, BROKEN_SAN_SCREEN, SETTINGS
from . import SettingsManager


class SanityScreen(arcade.View):
    """Экран рассудка"""

    def __init__(self, player, map, game):
        super().__init__()

        # Параметры игры
        self.player = player
        self.game = game
        self.map = map

        # UI
        self.camera = None
        self.batch = None
        self.sound_player = None

        # Параметры экрана
        self.bar_width = 0

        self.setup()

    def setup(self):
        """НАстройка сцены"""
        # Камеры
        self.camera = arcade.Camera2D(
            projection=arcade.rect.XYWH(0, 0, 800, 600),
            position=(400, 300)
        )
        self.gui_camera = arcade.Camera2D()

        # Batch
        self.batch = Batch()
        self.text = arcade.Text(
            text='Sanity:',
            x=30, y=560,
            color=arcade.color.WHITE,
            font_size=22,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='top',
            batch=self.batch
        )

        self.name_text = arcade.Text(
            text=self.game.player_name,
            x=580, y=470,
            color=arcade.color.WHITE,
            font_size=14,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='center',
            batch=self.batch
        )

    def on_draw(self) -> bool | None:
        self.clear()

        self.camera.use()

        # Рамка экрана
        arcade.draw_rect_outline(
            arcade.rect.LRBT(20, 760, 20, 560),
            color=arcade.color.WHITE,
            border_width=3
        )

        # Шкала рассудка
        arcade.draw_rect_filled(
            arcade.rect.LBWH(30, 430, self.bar_width, 40),
            color=arcade.color.WINE
        )

        # Рамка рассудка
        arcade.draw_rect_outline(
            arcade.rect.LBWH(30, 470 - 40, 540, 40),
            color=arcade.color.WHITE,
            border_width=1
        )
        arcade.draw_rect_outline(
            arcade.rect.LBWH(30, 360 - 40, 540, 40),
            color=arcade.color.WHITE,
            border_width=1
        )
        arcade.draw_rect_outline(
            arcade.rect.LBWH(30, 250 - 40, 540, 40),
            color=arcade.color.WHITE,
            border_width=1
        )
        arcade.draw_rect_outline(
            arcade.rect.LBWH(30, 140 - 40, 540, 40),
            color=arcade.color.WHITE,
            border_width=1
        )

        self.sanity_text = arcade.Text(
            text=f'{self.player.sanity if self.game.dif.sanity_screen else random.randint(1, 100)}%',
            x=580, y=430,
            color=arcade.color.WHITE,
            font_size=14,
            font_name='Courier New',
            anchor_x='left',
            anchor_y='center',
            batch=self.batch
        )
        self.batch.draw()

        # Закрыть экран
        arcade.draw_line(740 - 10, 540 - 10, 740 + 10, 540 + 10, color=arcade.color.WHITE)
        arcade.draw_line(740 + 10, 540 - 10, 740 - 10, 540 + 10, color=arcade.color.WHITE)

    def on_show_view(self) -> None:
        volume = SettingsManager.get_sound_volume()
        arcade.play_sound(BOARD_2, volume=volume)
        if not self.game.dif.sanity_screen:
            volume = SettingsManager.get_sound_volume(0.5)
            self.sound_player = arcade.play_sound(BROKEN_SAN_SCREEN, loop=True, volume=volume)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        world_cords = self.camera.unproject((x, y))

        if 740 - 10 < world_cords.x < 740 + 10 and 540 - 10 < world_cords.y < 540 + 10:
            self.close()
            return

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.ESCAPE:
            self.close()

    def on_update(self, delta_time: float) -> bool | None:
        self.bar_width = (self.player.sanity / 100 * 540) if self.game.dif.sanity_screen else random.randint(0, 540)

        # Обновляем тексты
        self.update_texts()

    def close(self):
        """Закрыть экран рассудка"""
        if self.sound_player:
            self.sound_player.pause()

        volume = SettingsManager.get_sound_volume()
        arcade.play_sound(BOARD_2, volume=volume)
        self.window.show_view(self.map)

    def open_settings(self):
        """Открыть настройки"""
        volume = SettingsManager.get_sound_volume(1.2)
        arcade.play_sound(SETTINGS, volume=volume)

        from . import SettingsView
        settings_view = SettingsView(back_callback=lambda: self.window.show_view(self))
        self.window.show_view(settings_view)

    def update_texts(self):
        """Обновить тексты"""
        from . import SettingsManager
        c_lang = SettingsManager.iget_current_language()
        self.text.text = ('Рассудок:', 'Sanity:')[c_lang]
