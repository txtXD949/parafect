import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel
from scripts.ui import InteractiveLabel, TextInputField

from ..sounds import HOVER_SOUND, CLICK_SOUND


class SigninMenu(arcade.View):
    def __init__(self, back_callback):
        super().__init__()
        self.back_callback = back_callback

        self.manager = UIManager()
        self.manager.enable()

        self.hover_sound = HOVER_SOUND
        self.click_sound = CLICK_SOUND

        self.status_text = '> ДАННЫЕ НЕ ПРОАНАЛИЗИРОВАНЫ'
        self.active_input = None

        self.setup_widgets()

    def setup_widgets(self):
        main_box = UIBoxLayout(vertical=True, space_between=15)

        # Заголовок
        title = UILabel(
            text='РЕГИСТРАЦИЯ В СИСТЕМЕ P-BASE',
            font_size=24,
            font_name='Courier New',
            width=500,
            height=50,
            align='center',
            text_color=arcade.color.WHITE,
            bold=True
        )
        main_box.add(title)

        subtitle = UILabel(
            text='(Форма №7)',
            font_size=16,
            font_name='Courier New',
            width=500,
            height=30,
            align='center',
            text_color=arcade.color.LIGHT_GRAY
        )
        main_box.add(subtitle)

        # Пустая строка для отступа
        main_box.add(UILabel(text='', width=500, height=30))

        # Имя
        name_label = UILabel(
            text='ИМЯ:',
            font_size=18,
            font_name='Courier New',
            width=200,
            height=30,
            text_color=arcade.color.LIGHT_GRAY
        )

        self.name_input = TextInputField(
            width=300,
            height=35,
            font_size=16,
            font_name='Courier New',
            text_color=arcade.color.WHITE,
            bg_color=arcade.color.DARK_GRAY,
            click_sound=self.click_sound
        )

        name_row = UIBoxLayout(vertical=False, space_between=10)
        name_row.add(name_label)
        name_row.add(self.name_input)
        main_box.add(name_row)

        # Пустая строка
        main_box.add(UILabel(text='', width=500, height=15))

        # Код доступа 1
        code1_label = UILabel(
            text='КОД ДОСТУПА:',
            font_size=18,
            font_name='Courier New',
            width=200,
            height=30,
            text_color=arcade.color.LIGHT_GRAY
        )

        self.code1_input = TextInputField(
            width=300,
            height=35,
            font_size=16,
            font_name='Courier New',
            text_color=arcade.color.WHITE,
            bg_color=arcade.color.DARK_GRAY,
            is_password=True,
            click_sound=self.click_sound
        )

        code1_row = UIBoxLayout(vertical=False, space_between=10)
        code1_row.add(code1_label)
        code1_row.add(self.code1_input)
        main_box.add(code1_row)

        # Код доступа 2
        code2_label = UILabel(
            text='ПОВТОРИТЕ КОД:',
            font_size=18,
            font_name='Courier New',
            width=200,
            height=30,
            text_color=arcade.color.LIGHT_GRAY
        )

        self.code2_input = TextInputField(
            width=300,
            height=35,
            font_size=16,
            font_name='Courier New',
            text_color=arcade.color.WHITE,
            bg_color=arcade.color.DARK_GRAY,
            is_password=True,
            click_sound=self.click_sound
        )

        code2_row = UIBoxLayout(vertical=False, space_between=10)
        code2_row.add(code2_label)
        code2_row.add(self.code2_input)
        main_box.add(code2_row)

        # Пустая строка
        main_box.add(UILabel(text='', width=500, height=30))

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

        # Пустая строка
        main_box.add(UILabel(text='', width=500, height=30))

        # Кнопки
        buttons_row = UIBoxLayout(vertical=False, space_between=50)

        self.register_btn = InteractiveLabel(
            text='ЗАРЕГИСТРИРОВАТЬ',
            width=250,
            height=45,
            font_size=18,
            font_name='Courier New',
            normal_color='#C8C8C8',
            hover_color='#FFFFFF',
            active_color='#FFFFFF',
            hover_sound=self.hover_sound,
            click_sound=self.click_sound
        )

        self.cancel_btn = InteractiveLabel(
            text='ОТМЕНА',
            width=250,
            height=45,
            font_size=18,
            font_name='Courier New',
            normal_color='#C8C8C8',
            hover_color='#FFFFFF',
            active_color='#FFFFFF',
            hover_sound=self.hover_sound,
            click_sound=self.click_sound
        )

        buttons_row.add(self.register_btn)
        buttons_row.add(self.cancel_btn)
        main_box.add(buttons_row)

        # Центрируем
        anchor = UIAnchorLayout()
        anchor.add(child=main_box, anchor_x='center', anchor_y='center')
        self.manager.add(anchor)

    def attempt_registration(self):
        """Попытка регистрации"""
        name = self.name_input.text
        code1 = self.code1_input.text
        code2 = self.code2_input.text

        if not name or not code1 or not code2:
            self.status_text = '> ОШИБКА: ЗАПОЛНИТЕ ВСЕ ПОЛЯ'
            self.status_label.text = self.status_text
            return

        if code1 != code2:
            self.status_text = '> ОШИБКА: КОДЫ НЕ СОВПАДАЮТ'
            self.status_label.text = self.status_text
            return

        self.status_text = '> РЕГИСТРАЦИЯ...'
        self.status_label.text = self.status_text

        from database import AccountManager
        manager = AccountManager()

        if name in manager.get_logins():
            self.status_text = '> ОШИБКА: ВВЕДЕН СУЩЕСТВУЮЩИЙ ЛОГИН'
            self.status_label.text = self.status_text
            return

        manager.add_account(name, code1)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_update(self, delta_time):
        self.register_btn.on_update(delta_time)
        self.cancel_btn.on_update(delta_time)
        self.name_input.on_update(delta_time)
        self.code1_input.on_update(delta_time)
        self.code2_input.on_update(delta_time)

    def on_mouse_motion(self, x, y, dx, dy):
        self.register_btn.check_mouse_hover(x, y)
        self.cancel_btn.check_mouse_hover(x, y)
        self.name_input.check_mouse_hover(x, y)
        self.code1_input.check_mouse_hover(x, y)
        self.code2_input.check_mouse_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            clicked_on_input = False

            # Поля ввода
            inputs = [
                (self.name_input, [self.code1_input, self.code2_input]),
                (self.code1_input, [self.name_input, self.code2_input]),
                (self.code2_input, [self.name_input, self.code1_input])
            ]

            for input_field, others in inputs:
                if input_field.check_mouse_hover(x, y):
                    input_field.on_click()
                    for other in others:
                        other.reset_state()
                    self.active_input = input_field
                    clicked_on_input = True
                    break

            # Кнопка регистрации
            if self.register_btn.check_mouse_hover(x, y):
                self.register_btn.on_click()
                if self.register_btn.is_active:
                    self.cancel_btn.reset_state()
                    self.attempt_registration()

            # Кнопка отмены
            elif self.cancel_btn.check_mouse_hover(x, y):
                self.cancel_btn.on_click()
                if self.cancel_btn.is_active:
                    self.register_btn.reset_state()
                    self.back_callback()

            # Деактивация полей если кликнули мимо
            if not clicked_on_input and self.active_input:
                self.active_input.deactivate()
                self.active_input = None

    def on_key_press(self, key, modifiers):
        if self.active_input:
            self.active_input.on_key_press(key, modifiers)
        elif key == arcade.key.ESCAPE:
            self.back_callback()

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()
