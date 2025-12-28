import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel

from scripts.custom_widgets import InteractiveLabel
import constants


class EntryMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BLACK
        constants.ENTRY_BACKGROUND_SOUND.play(loop=True, volume=0.2)

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout_labels = UIBoxLayout(vertical=True, space_between=20)
        self.box_layout_buttons = UIBoxLayout(vertical=True, space_between=20)

        self.label1 = None  # Добро пожаловать
        self.label2 = None  # Вам нужен профиль
        self.button1 = None  # Создать
        self.button2 = None  # Войти

        self.active_button = None

        self.setup_widgets()

    def setup_widgets(self):
        self.label1 = UILabel(
            text='Добро пожаловать',
            font_size=26,
            font_name='Courier New',
            width=300,
            align='center',
        )
        self.box_layout_labels.add(self.label1)

        self.label2 = UILabel(
            text='Вам нужен профиль',
            font_size=20,
            font_name='Courier New',
            width=300,
            align='center'
        )
        self.box_layout_labels.add(self.label2)

        self.button_create = InteractiveLabel(
            text='СОЗДАТЬ',
            width=250,
            height=45,
            font_size=22,
            font_name='Courier New',
            normal_color='#C8C8C8',  # Серый
            hover_color='#FFFFFF',  # Белый
            active_color='#FFFFFF',  # Белый
            hover_sound=arcade.load_sound('././assets/sounds/effects/hover.wav'),
            click_sound=arcade.load_sound('././assets/sounds/effects/click.wav')
        )
        self.box_layout_buttons.add(self.button_create)

        self.button_login = InteractiveLabel(
            text='ВОЙТИ',
            width=250,
            height=45,
            font_size=22,
            font_name='Courier New',
            normal_color='#C8C8C8',
            hover_color='#FFFFFF',
            active_color='#FFFFFF',
            hover_sound=arcade.load_sound('././assets/sounds/effects/hover.wav'),
            click_sound=arcade.load_sound('././assets/sounds/effects/click.wav')
        )
        self.box_layout_buttons.add(self.button_login)

        # Собираем все в anchor layout
        self.anchor_layout.add(
            child=self.box_layout_labels,
            anchor_x='center',
            anchor_y='top',
            align_y=-100
        )

        self.anchor_layout.add(
            child=self.box_layout_buttons,
            anchor_x='center',
            anchor_y='center'
        )

        self.manager.add(self.anchor_layout)

    def on_draw(self) -> bool | None:
        self.clear()

        self.manager.draw()

    def on_update(self, delta_time):
        """Обновление анимации"""
        self.button_create.on_update(delta_time)
        self.button_login.on_update(delta_time)

    def on_mouse_motion(self, x, y, dx, dy):
        """Обработка движения мыши"""
        # Проверяем наведение на кнопки
        self.button_create.check_mouse_hover(x, y)
        self.button_login.check_mouse_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мыши"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Проверяем клик по кнопке СОЗДАТЬ
            if self.button_create.check_mouse_hover(x, y):
                self.button_create.on_click()

                # Если нажали СОЗДАТЬ, сбрасываем ВОЙТИ
                if self.button_create._is_active:
                    self.button_login.reset_state()
                    self.active_button = self.button_create

                    # Действие при нажатии СОЗДАТЬ
                    self.on_create_click()

            # Проверяем клик по кнопке ВОЙТИ
            elif self.button_login.check_mouse_hover(x, y):
                self.button_login.on_click()

                # Если нажали ВОЙТИ, сбрасываем СОЗДАТЬ
                if self.button_login._is_active:
                    self.button_create.reset_state()
                    self.active_button = self.button_login

                    # Действие при нажатии ВОЙТИ
                    self.on_login_click()

    def on_create_click(self):
        """Действие при клике на СОЗДАТЬ"""
        from .signin_menu import SigninMenu
        registration = SigninMenu(back_callback=lambda: self.window.show_view(self))
        self.window.show_view(registration)

    def on_login_click(self):
        """Действие при клике на ВОЙТИ"""
        from .login_menu import LoginMenu
        login = LoginMenu(back_callback=lambda: self.window.show_view(self))
        self.window.show_view(login)

    def on_key_press(self, key, modifiers):
        """Обработка клавиш"""
        if key == arcade.key.ESCAPE:
            self.window.close()
        elif key == arcade.key.ENTER:
            # Если есть активная кнопка, выполняем её действие
            if self.active_button == self.button_create:
                self.on_create_click()
            elif self.active_button == self.button_login:
                self.on_login_click()

    def reset_all_buttons(self):
        """Сброс всех кнопок при возврате"""
        self.button_create.reset_state()
        self.button_login.reset_state()
        self.active_button = None

    def on_show_view(self):
        """Вызывается при показе этого View"""
        super().on_show_view()
        # Сбрасываем кнопки
        self.button_create.reset_state()
        self.button_login.reset_state()
        self.active_button = None
