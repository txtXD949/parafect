import arcade
from typing import Optional

from ..sounds import HOVER_SOUND, CLICK_SOUND


class InteractiveLabel(arcade.gui.UILabel):
    """Кнопка"""

    def __init__(self,
                 text: str = '',
                 x: float = 0,
                 y: float = 0,
                 width: float = 200,
                 height: float = 50,
                 font_size: float = 20,
                 font_name=('Courier New',),
                 normal_color='#C8C8C8',
                 hover_color='#FFFFFF',
                 active_color='#FFFFFF',
                 hover_sound: Optional[arcade.sound] = None,
                 click_sound: Optional[arcade.sound] = None,
                 **kwargs):

        self.base_text = text
        self.normal_color = arcade.color.Color.from_hex_string(normal_color)
        self.hover_color = arcade.color.Color.from_hex_string(hover_color)
        self.active_color = arcade.color.Color.from_hex_string(active_color)

        super().__init__(
            text=f'< {text} >',
            x=x,
            y=y,
            width=width,
            height=height,
            font_size=font_size,
            font_name=font_name,
            text_color=self.normal_color,
            align='center',
            **kwargs
        )

        self._is_hovered = False
        self._is_active = False
        self.hover_sound = hover_sound
        self.click_sound = click_sound
        self.hover_sound_played = False

        if not hover_sound:
            self.hover_sound = HOVER_SOUND
        if not click_sound:
            self.click_sound = CLICK_SOUND

    def check_mouse_hover(self, x: float, y: float) -> bool:
        """Проверка на ховер"""
        old_hovered = self._is_hovered
        self._is_hovered = (self.rect.left <= x <= self.rect.right and
                            self.rect.bottom <= y <= self.rect.top)

        # Звук при наведении
        if self._is_hovered and not old_hovered and self.hover_sound:
            from ..views.settings import SettingsManager
            volume = SettingsManager.get_sound_volume(0.6)
            arcade.play_sound(self.hover_sound, volume=volume)

        if self._is_active:
            self.text = f'= {self.base_text} ='
            self._label.color = self.active_color
        elif self._is_hovered:
            self.text = f'> {self.base_text} <'
            self._label.color = self.hover_color
        else:
            self.text = f'< {self.base_text} >'
            self._label.color = self.normal_color

        return self._is_hovered

    def on_click(self):
        """При клике"""
        # Звук при клике
        if self.click_sound:
            from ..views.settings import SettingsManager
            volume = SettingsManager.get_sound_volume(0.6)
            arcade.play_sound(self.click_sound, volume=volume)

        self._is_active = not self._is_active
        self.check_mouse_hover(0, 0)
        return True

    def reset_state(self):
        """Сбросить кнопку"""
        self._is_hovered = False
        self._is_active = False
        self.hover_sound_played = False
        self.check_mouse_hover(0, 0)

    @property
    def is_hovered(self):
        return self._is_hovered

    @property
    def is_active(self):
        return self._is_active
