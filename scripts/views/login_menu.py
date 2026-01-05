import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel

from scripts.ui import InteractiveLabel, TextInputField


class LoginMenu(arcade.View):
    def __init__(self, back_callback):
        super().__init__()
        self.back_callback = back_callback

        self.manager = UIManager()
        self.manager.enable()

        self.hover_sound = arcade.load_sound('././assets/sounds/effects/hover.wav')
        self.click_sound = arcade.load_sound('././assets/sounds/effects/click.wav')

        self.status_text = '> ОЖИДАНИЕ ВВОДА...'
        self.active_input = None

        self.setup_widgets()

    def setup_widgets(self):
        main_box = UIBoxLayout(vertical=True, space_between=20)

        # Заголовок
        title = UILabel(
            text='ПОДКЛЮЧЕНИЕ К СИСТЕМЕ P-BASE',
            font_size=24,
            font_name='Courier New',
            width=500,
            height=50,
            align='center',
            text_color=arcade.color.WHITE,
            bold=True
        )
        main_box.add(title)

        # Поле логина
        login_label = UILabel(
            text='ЛОГИН:',
            font_size=18,
            font_name='Courier New',
            width=100,
            height=30,
            text_color=arcade.color.LIGHT_GRAY
        )

        self.login_input = TextInputField(
            width=300,
            height=35,
            font_size=16,
            font_name='Courier New',
            text_color=arcade.color.WHITE,
            bg_color=arcade.color.DARK_GRAY,
            click_sound=self.click_sound,
            on_enter=self.on_login_enter
        )

        login_row = UIBoxLayout(vertical=False, space_between=15)
        login_row.add(login_label)
        login_row.add(self.login_input)
        main_box.add(login_row)

        # Поле пароля
        password_label = UILabel(
            text='ПАРОЛЬ:',
            font_size=18,
            font_name='Courier New',
            width=100,
            height=30,
            text_color=arcade.color.LIGHT_GRAY
        )

        self.password_input = TextInputField(
            width=300,
            height=35,
            font_size=16,
            font_name='Courier New',
            text_color=arcade.color.WHITE,
            bg_color=arcade.color.DARK_GRAY,
            is_password=True,
            click_sound=self.click_sound,
            on_enter=self.on_password_enter
        )

        password_row = UIBoxLayout(vertical=False, space_between=15)
        password_row.add(password_label)
        password_row.add(self.password_input)
        main_box.add(password_row)

        # Статус
        self.status_label = UILabel(
            text=self.status_text,
            font_size=16,
            font_name='Courier New',
            width=400,
            height=30,
            text_color=arcade.color.YELLOW
        )
        main_box.add(self.status_label)

        # Кнопки
        buttons_row = UIBoxLayout(vertical=False, space_between=50)

        self.connect_btn = InteractiveLabel(
            text='ПОДКЛЮЧИТЬСЯ',
            width=200,
            height=45,
            font_size=18,
            font_name='Courier New',
            normal_color='#C8C8C8',
            hover_color='#FFFFFF',
            active_color='#FFFFFF',
            hover_sound=self.hover_sound,
            click_sound=self.click_sound
        )

        self.back_btn = InteractiveLabel(
            text='НАЗАД',
            width=200,
            height=45,
            font_size=18,
            font_name='Courier New',
            normal_color='#C8C8C8',
            hover_color='#FFFFFF',
            active_color='#FFFFFF',
            hover_sound=self.hover_sound,
            click_sound=self.click_sound
        )

        buttons_row.add(self.connect_btn)
        buttons_row.add(self.back_btn)
        main_box.add(buttons_row)

        # Центрируем
        anchor = UIAnchorLayout()
        anchor.add(child=main_box, anchor_x='center', anchor_y='center')
        self.manager.add(anchor)

    def on_login_enter(self, text):
        """Когда нажали Enter в поле логина"""
        if text and self.password_input.text == '':
            # Переходим к паролю
            self.login_input.deactivate()
            self.password_input.on_click()
            self.active_input = self.password_input

    def on_password_enter(self, text):
        """Когда нажали Enter в поле пароля"""
        if text:
            self.password_input.deactivate()
            self.active_input = None
            self.attempt_login()

    def attempt_login(self):
        """Попытка входа"""
        login = self.login_input.text
        password = self.password_input.text

        if not login or not password:
            self.status_text = '> ОШИБКА: ЗАПОЛНИТЕ ВСЕ ПОЛЯ'
            self.status_label.text = self.status_text
            return

        from database import AccountManager
        manager = AccountManager()

        if manager.get_account(login, password):
            self.status_text = '> ПОДКЛЮЧЕНИЕ...'
            self.status_label.text = self.status_text

            from .lobby import LobbyView
            lobby = LobbyView()
            self.window.show_view(lobby)

            from constants import ENTRY_BACKGROUND_SOUND
            ENTRY_BACKGROUND_SOUND.pause()

        else:
            self.status_text = '> ОШИБКА: НЕВЕРНЫЕ ДАННЫЕ'
            self.status_label.text = self.status_text

    def on_draw(self):
        self.clear()

        self.manager.draw()

    def on_update(self, delta_time):
        self.connect_btn.on_update(delta_time)
        self.back_btn.on_update(delta_time)
        self.login_input.on_update(delta_time)
        self.password_input.on_update(delta_time)

    def on_mouse_motion(self, x, y, dx, dy):
        self.connect_btn.check_mouse_hover(x, y)
        self.back_btn.check_mouse_hover(x, y)
        self.login_input.check_mouse_hover(x, y)
        self.password_input.check_mouse_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Деактивируем все поля если кликнули мимо
            clicked_on_input = False

            # Проверяем поля ввода
            if self.login_input.check_mouse_hover(x, y):
                self.login_input.on_click()
                self.password_input.reset_state()
                self.active_input = self.login_input
                clicked_on_input = True
            elif self.password_input.check_mouse_hover(x, y):
                self.password_input.on_click()
                self.login_input.reset_state()
                self.active_input = self.password_input
                clicked_on_input = True

            # Кнопки
            if self.connect_btn.check_mouse_hover(x, y):
                self.connect_btn.on_click()
                if self.connect_btn.is_active:
                    self.back_btn.reset_state()
                    self.attempt_login()

            elif self.back_btn.check_mouse_hover(x, y):
                self.back_btn.on_click()
                if self.back_btn.is_active:
                    self.connect_btn.reset_state()
                    # Возвращаемся назад
                    self.back_callback()

            # Если кликнули не на поле ввода, деактивируем активное
            if not clicked_on_input and self.active_input:
                self.active_input.deactivate()
                self.active_input = None

    def on_key_press(self, key, modifiers):
        # Передаем нажатия активному полю ввода
        if self.active_input:
            self.active_input.on_key_press(key, modifiers)
        elif key == arcade.key.ESCAPE:
            self.back_callback()
