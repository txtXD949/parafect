import arcade
import arcade.text
from pyglet.graphics import Batch

from .entry_menu import EntryMenu


class Screensaver(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.WHITE
        self.fade_alpha = 0
        self.fade_speed = 40

        self.batch = None
        self.font = None
        self.title = None
        self.title_ = None

        self.heartbeat_sound = arcade.load_sound('././assets/sounds/effects/heartbeat.wav')

        # Анимация буквы f
        self.f_animation_timer = 0
        self.f_animation_phase = 'waiting'
        self.blink_count = 0

        self.setup_text()

    def setup_text(self):
        """Создаем текст через Batch"""
        self.batch = Batch()

        center_x = self.window.width // 2
        center_y = self.window.height // 2

        self.title = arcade.Text(
            text='Parafect',
            x=center_x,
            y=center_y,
            color=arcade.color.WHITE,
            font_size=100,
            font_name='Courier New',
            batch=self.batch,
            anchor_x='center',
            anchor_y='center',
            bold=True
        )

        self.title_ = arcade.Text(
            text='Para ect',
            x=center_x,
            y=center_y,
            color=arcade.color.WHITE,
            font_size=100,
            font_name='Courier New',
            batch=self.batch,
            anchor_x='center',
            anchor_y='center',
            bold=True
        )

    def on_update(self, delta_time):
        # Анимация затемнения фона
        self.fade_alpha = min(self.fade_alpha + self.fade_speed * delta_time, 255)

        # Управление анимацией буквы f
        if self.fade_alpha >= 255:
            self.f_animation_timer += delta_time

            # Ждем 1.5 секунды после полного затемнения
            if self.f_animation_phase == 'waiting' and self.f_animation_timer >= 0.5:
                self.f_animation_phase = 'fade_out'
                self.f_animation_timer = 0

            # Потухание буквы f
            elif self.f_animation_phase == 'fade_out':
                self.title_.batch = self.batch
                self.title.batch = None
                if self.f_animation_timer >= 0.6:
                    self.f_animation_phase = 'blinking'
                    self.f_animation_timer = 0

            # Быстрое мерцание
            elif self.f_animation_phase == 'blinking':
                self.heartbeat_sound.play()
                blink_interval = 0.1
                blink_state = int(self.f_animation_timer / blink_interval) % 2
                if blink_state == 0:
                    self.title.batch = self.batch
                    self.title_.batch = None
                else:
                    self.title.batch = None
                    self.title_.batch = self.batch

                # Считаем количество мерцаний
                if self.f_animation_timer >= 0.2 * (self.blink_count + 1):
                    self.blink_count += 1
                    if self.blink_count >= 4:
                        self.f_animation_phase = 'fade_in'
                        self.f_animation_timer = 0

            # Загорание обратно (0.5 секунды)
            elif self.f_animation_phase == 'fade_in':
                if self.f_animation_timer >= 0.5:
                    self.f_animation_phase = 'done'

            if self.f_animation_phase == 'done':
                login_menu = EntryMenu()
                self.window.show_view(login_menu)

    def on_draw(self):
        """Отрисовка кадра"""
        self.clear(arcade.color.WHITE)

        # Черный прямоугольник с анимацией прозрачности
        if self.fade_alpha > 0:
            arcade.draw_lrbt_rectangle_filled(
                left=0,
                right=self.window.width,
                top=self.window.height,
                bottom=0,
                color=(0, 0, 0, int(self.fade_alpha))
            )

        self.batch.draw()
