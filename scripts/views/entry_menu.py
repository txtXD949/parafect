import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel

from scripts.ui import InteractiveLabel
from ..start_sound import ENTRY_BACKGROUND_SOUND

from constants import LANGUAGE_INDEX


class EntryMenu(arcade.View):
    """Меню входа"""

    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BLACK

        # Звук в меню
        ENTRY_BACKGROUND_SOUND.play()

        # Менеджер
        self.manager = UIManager()
        self.manager.enable()

        # Слои
        self.anchor_layout = UIAnchorLayout()
        self.box_layout_labels = UIBoxLayout(vertical=True, space_between=20)
        self.box_layout_buttons = UIBoxLayout(vertical=True, space_between=20)
        self.box_layout_bottom = UIBoxLayout(vertical=False, space_between=30)

        self.label1 = None  # Добро пожаловать
        self.label2 = None  # Вам нужен профиль
        self.button1 = None  # Создать
        self.button2 = None  # Войти
        self.button_settings = None  # Настройки
        self.button_exit = None  # Выход

        self.active_button = None

        self.setup_widgets()

    def setup_widgets(self):
        """Настройка виджетов"""
        # Добро пожаловать
        self.label1 = UILabel(
            text='Welcome',
            font_size=26,
            font_name='Courier New',
            width=300,
            align='center',
        )
        self.box_layout_labels.add(self.label1)

        # Вам нужен профиль
        self.label2 = UILabel(
            text='You need a profile',
            font_size=20,
            font_name='Courier New',
            width=300,
            align='center'
        )
        self.box_layout_labels.add(self.label2)

        # Кнопка СОЗДАТЬ
        self.button_create = InteractiveLabel(
            text='CREATE',
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

        # Кнопка ВОЙТИ
        self.button_login = InteractiveLabel(
            text='LOGIN',
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

        # Кнопка НАСТРОЙКИ
        self.button_settings = InteractiveLabel(
            text='SETTINGS',
            width=180,
            height=35,
            font_size=18,
            font_name='Courier New',
            normal_color='#888888',  # Темно-серый
            hover_color='#C8C8C8',  # Светло-серый
            active_color='#C8C8C8',
            hover_sound=arcade.load_sound('././assets/sounds/effects/hover.wav'),
            click_sound=arcade.load_sound('././assets/sounds/effects/click.wav')
        )
        self.box_layout_bottom.add(self.button_settings)

        # Кнопка ВЫХОД
        self.button_exit = InteractiveLabel(
            text='EXIT',
            width=180,
            height=35,
            font_size=18,
            font_name='Courier New',
            normal_color='#888888',
            hover_color='#C8C8C8',
            active_color='#C8C8C8',
            hover_sound=arcade.load_sound('././assets/sounds/effects/hover.wav'),
            click_sound=arcade.load_sound('././assets/sounds/effects/click.wav')
        )
        self.box_layout_bottom.add(self.button_exit)

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

        self.anchor_layout.add(
            child=self.box_layout_bottom,
            anchor_x='center',
            anchor_y='bottom',
            align_y=50  # Отступ от низа
        )

        self.manager.add(self.anchor_layout)

    def update_texts(self):
        """Обновляет тексты"""
        from . import SettingsManager
        c_lang = SettingsManager.iget_current_language()

        self.label1.text = ('Добро пожаловать', 'Welcome')[c_lang]
        self.label2.text = ('Вам нужен профиль', 'You need a profile')[c_lang]
        self.button_create.base_text = ('СОЗДАТЬ', 'CREATE')[c_lang]
        self.button_login.base_text = ('ВОЙТИ', 'LOGIN')[c_lang]
        self.button_settings.base_text = ('НАСТРОЙКИ', 'SETTINGS')[c_lang]
        self.button_exit.base_text = ('ВЫХОД', 'EXIT')[c_lang]

    def on_draw(self) -> bool | None:
        self.clear()

        self.manager.draw()

    def on_update(self, delta_time):
        self.button_create.on_update(delta_time)
        self.button_login.on_update(delta_time)
        self.button_settings.on_update(delta_time)
        self.button_exit.on_update(delta_time)

        from . import SettingsManager
        vol = SettingsManager.get_sound_volume()
        ENTRY_BACKGROUND_SOUND.volume = vol

        # Обновление текстов
        self.update_texts()

    def on_mouse_motion(self, x, y, dx, dy):
        self.button_create.check_mouse_hover(x, y)
        self.button_login.check_mouse_hover(x, y)
        self.button_settings.check_mouse_hover(x, y)
        self.button_exit.check_mouse_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
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

            elif self.button_settings.check_mouse_hover(x, y):
                self.button_settings.on_click()
                if self.button_settings._is_active:
                    self.reset_other_buttons(self.button_settings)
                    self.on_settings_click()

                # Проверяем клик по кнопке ВЫХОД
            elif self.button_exit.check_mouse_hover(x, y):
                self.button_exit.on_click()
                if self.button_exit._is_active:
                    self.reset_other_buttons(self.button_exit)
                    self.on_exit_click()

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

    def on_settings_click(self):
        """Действие при клике на НАСТРОЙКИ"""
        self.reset_all_buttons()
        from . import SettingsView
        settings_view = SettingsView(back_callback=lambda: self.window.show_view(self))
        self.window.show_view(settings_view)

    def on_exit_click(self):
        """Действие при клике на ВЫХОД"""
        self.window.close()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.close()
        if key == arcade.key.F10:
            self.on_settings_click()
        elif key == arcade.key.ENTER:
            # Если есть активная кнопка, выполняем её действие
            if self.active_button == self.button_create:
                self.on_create_click()
            elif self.active_button == self.button_login:
                self.on_login_click()
            elif self.active_button == self.button_settings:
                self.on_settings_click()
            elif self.active_button == self.button_exit:
                self.on_exit_click()

    def reset_all_buttons(self):
        """Сброс всех кнопок при возврате"""
        self.button_create.reset_state()
        self.button_login.reset_state()
        self.active_button = None
        self.button_settings.reset_state()
        self.button_exit.reset_state()
        self.active_button = None

    def reset_other_buttons(self, active_button):
        """Сбрасывает все кнопки кроме активной"""
        buttons = [self.button_create, self.button_login,
                   self.button_settings, self.button_exit]

        for button in buttons:
            if button != active_button:
                button.reset_state()

        self.active_button = active_button

    def on_show_view(self):
        super().on_show_view()
        # Сбрасываем кнопки
        self.button_create.reset_state()
        self.button_login.reset_state()
        self.active_button = None
