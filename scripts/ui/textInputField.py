import arcade
from arcade.gui import UIInputText


class TextInputField(UIInputText):
    """Ввод текста"""

    def __init__(self, width=300, height=35,
                 font_name='Courier New', font_size=16,
                 text_color=arcade.color.WHITE,
                 click_sound=None, **kwargs):

        super().__init__(
            width=width,
            height=height,
            text='',
            font_name=font_name,
            font_size=font_size,
            text_color=text_color
        )

        self.click_sound = click_sound
        self.caret.visible = False
        self._is_active = False

    def check_mouse_hover(self, x, y):
        """проверка на ховер"""
        return (self.left <= x <= self.right and
                self.bottom <= y <= self.top)

    def on_click(self, event=None):
        """При клике"""
        if self.click_sound:
            from ..sounds import CLICK_SOUND
            from ..views.settings import SettingsManager
            volume = SettingsManager.get_sound_volume(0.6)
            arcade.play_sound(CLICK_SOUND, volume=volume)

        self.caret.visible = True
        self.caret.position = len(self.text)
        self._is_active = True
        return True

    def reset_state(self):
        """Сбросить кнопку"""
        self.caret.visible = False
        self._is_active = False

    def on_key_press(self, key, modifiers):
        if not self._is_active:
            return

        if key == arcade.key.BACKSPACE:
            if self.text:
                self.text = self.text[:-1]
                self.caret.position = len(self.text)
        elif key == arcade.key.ENTER:
            self.reset_state()
        elif key == arcade.key.ESCAPE:
            self.reset_state()

    def on_text(self, text):
        if self._is_active:
            if text and text.isprintable() and text != '\r' and text != '\n':
                self.text += text
                self.caret.position = len(self.text)
