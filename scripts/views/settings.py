import os
import json
import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UISlider

from scripts.ui import InteractiveLabel
import constants
from ..sounds import CLICK_SOUND, HOVER_SOUND


class SettingsManager:
    SETTINGS_FILE = '././settings.json'

    @staticmethod
    def load():
        """Подгрузка настроек"""
        try:
            with open(SettingsManager.SETTINGS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            constants.MASTER_VOLUME = float(data.get('master_volume', 1.0))
            constants.GHOST_VOLUME = float(data.get('ghost_volume', 1.0))

            lang = data.get('language', 'ru')
            if lang == 'ru':
                constants.LANGUAGE_INDEX = 0
            elif lang == 'en':
                constants.LANGUAGE_INDEX = 1
            else:
                constants.LANGUAGE_INDEX = 0
            return True

        except Exception:
            SettingsManager._create_default_settings()

    @staticmethod
    def _create_default_settings():
        """Значения по умолчанию"""
        try:
            data = {
                'master_volume': 1.0,
                'ghost_volume': 1.0,
                'language': 'ru'
            }

            with open(SettingsManager.SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            return True
        except Exception:
            return False

    @staticmethod
    def save():
        """Сохраняет настройки из constants в settings.json"""
        try:
            data = {
                'master_volume': constants.MASTER_VOLUME,
                'ghost_volume': constants.GHOST_VOLUME,
                'language': constants.LANGUAGES[constants.LANGUAGE_INDEX]
            }

            with open(SettingsManager.SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            return True
        except Exception as e:
            return False

    @staticmethod
    def get_sound_volume(base_volume: float = 1.0) -> float:
        """Возвращает громкость звука"""
        return base_volume * constants.MASTER_VOLUME

    @staticmethod
    def get_ghost_sound_volume(base_volume: float = 1.0) -> float:
        """Возвращает громкость звука призрака"""
        return base_volume * constants.MASTER_VOLUME * constants.GHOST_VOLUME

    @staticmethod
    def get_current_language() -> str:
        """Возвращает текущий язык"""
        return constants.LANGUAGES[constants.LANGUAGE_INDEX]

    @staticmethod
    def update_master_volume(value: float):
        """Обновляет общую громкость"""
        constants.MASTER_VOLUME = round(max(0.0, min(1.0, value)), 2)

    @staticmethod
    def update_ghost_volume(value: float):
        """Обновляет громкость призрака"""
        constants.GHOST_VOLUME = round(max(0.0, min(1.0, value)), 2)

    @staticmethod
    def update_language(lang: str):
        """Обновляет язык"""
        if lang == 'ru':
            constants.LANGUAGE_INDEX = 0
        elif lang == 'en':
            constants.LANGUAGE_INDEX = 1


class SettingsView(arcade.View):
    def __init__(self, back_callback):
        super().__init__()
        self.back_callback = back_callback
        self.background_color = arcade.color.BLACK

        SettingsManager.load()

        self.manager = UIManager()
        self.manager.enable()

        # Lauout'ы
        self.anchor_layout = UIAnchorLayout()

        self.box_layout_title = UIBoxLayout(vertical=True, space_between=10)
        self.box_layout_settings = UIBoxLayout(vertical=True, space_between=40)
        self.box_layout_bottom = UIBoxLayout(vertical=True, space_between=20)

        # Элементы UI
        self.title_label = None
        self.master_slider = None
        self.ghost_slider = None
        self.language_button = None
        self.back_button = None

        # Цвета
        self.normal_color = arcade.color.Color.from_hex_string('#C8C8C8')
        self.hover_color = arcade.color.Color.from_hex_string('#FFFFFF')
        self.active_color = arcade.color.Color.from_hex_string('#FFFFFF')
        self.dark_gray = arcade.color.Color.from_hex_string('#888888')

        # Текущий язык
        self.languages = {
            'RU': 'РУССКИЙ',
            'EN': 'ENGLISH'
        }
        self.language_button_texts = ['ЯЗЫК: РУССКИЙ', 'LANGUAGE: ENGLISH']

        # Текущие настройки
        self.master_volume = 1.0
        self.ghost_volume = 1.0

        self.setup_widgets()
        self.update_ui_texts()

    def setup_widgets(self):
        # Заголовок
        self.title_label = UILabel(
            text='НАСТРОЙКИ',
            font_size=36,
            font_name='Courier New',
            width=400,
            height=60,
            align='center',
            text_color=self.hover_color
        )
        self.box_layout_title.add(self.title_label)

        # Настройки
        master_container = UIBoxLayout(vertical=True, space_between=8)
        master_label = UILabel(
            text='ГРОМКОСТЬ ИГРЫ:',
            font_size=18,
            font_name='Courier New',
            width=350,
            text_color=self.normal_color,
            align='left'
        )
        master_container.add(master_label)

        self.master_slider = UISlider(
            value=constants.MASTER_VOLUME,
            min_value=0.0,
            max_value=1.0,
            width=350,
            height=25
        )
        self.master_slider.bg_color = self.dark_gray
        self.master_slider.border_color = self.normal_color
        self.master_slider.border_width = 2
        self.master_slider.knob_color = self.normal_color
        self.master_slider.knob_width = 30
        self.master_slider.knob_height = 35

        slider_row = UIBoxLayout(vertical=False, space_between=15, align='center')
        slider_row.add(self.master_slider)

        self.master_value_label = UILabel(
            text=f'{int(constants.MASTER_VOLUME * 100)}%',
            font_size=16,
            font_name='Courier New',
            width=60,
            text_color=self.normal_color
        )
        slider_row.add(self.master_value_label)

        master_container.add(slider_row)
        self.box_layout_settings.add(master_container)

        # Вторая настройка
        ghost_container = UIBoxLayout(vertical=True, space_between=8)
        ghost_label = UILabel(
            text='ГРОМКОСТЬ ПРИЗРАКА:',
            font_size=18,
            font_name='Courier New',
            width=350,
            text_color=self.normal_color,
            align='left'
        )
        ghost_container.add(ghost_label)

        self.ghost_slider = UISlider(
            value=constants.GHOST_VOLUME,
            min_value=0.0,
            max_value=1.0,
            width=350,
            height=25
        )
        self.ghost_slider.bg_color = self.dark_gray
        self.ghost_slider.border_color = self.normal_color
        self.ghost_slider.border_width = 2
        self.ghost_slider.knob_color = self.normal_color
        self.ghost_slider.knob_width = 30
        self.ghost_slider.knob_height = 35

        slider_row2 = UIBoxLayout(vertical=False, space_between=15, align='center')
        slider_row2.add(self.ghost_slider)

        self.ghost_value_label = UILabel(
            text=f'{int(constants.GHOST_VOLUME * 100)}%',
            font_size=16,
            font_name='Courier New',
            width=60,
            text_color=self.normal_color
        )
        slider_row2.add(self.ghost_value_label)

        ghost_container.add(slider_row2)
        self.box_layout_settings.add(ghost_container)

        # Кнопка смены языка
        self.language_button = InteractiveLabel(
            text=f'{self.language_button_texts[constants.LANGUAGE_INDEX]}',
            width=300,
            height=45,
            font_size=20,
            font_name='Courier New',
            normal_color='#C8C8C8',
            hover_color='#FFFFFF',
            active_color='#FFFFFF',
            hover_sound=HOVER_SOUND,
            click_sound=CLICK_SOUND
        )
        self.box_layout_settings.add(self.language_button)

        # Кнопка возврата
        self.back_button = InteractiveLabel(
            text='НАЗАД',
            width=250,
            height=50,
            font_size=24,
            font_name='Courier New',
            normal_color='#C8C8C8',
            hover_color='#FFFFFF',
            active_color='#FFFFFF',
            hover_sound=HOVER_SOUND,
            click_sound=CLICK_SOUND
        )
        self.box_layout_bottom.add(self.back_button)

        # Собираем все в anchor_layout
        self.anchor_layout.add(
            child=self.box_layout_title,
            anchor_x='center',
            anchor_y='top',
            align_y=-100
        )

        self.anchor_layout.add(
            child=self.box_layout_settings,
            anchor_x='center',
            anchor_y='center'
        )

        self.anchor_layout.add(
            child=self.box_layout_bottom,
            anchor_x='center',
            anchor_y='bottom',
            align_y=100
        )

        self.manager.add(self.anchor_layout)

        @self.master_slider.event('on_change')
        def on_master_slider_change(event):
            self.on_master_volume_change(event.new_value)

        @self.ghost_slider.event('on_change')
        def on_ghost_slider_change(event):
            self.on_ghost_volume_change(event.new_value)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_update(self, delta_time):
        if self.back_button:
            self.back_button.on_update(delta_time)
        if self.language_button:
            self.language_button.on_update(delta_time)

        from ..start_sound import ENTRY_BACKGROUND_SOUND
        ENTRY_BACKGROUND_SOUND.volume = SettingsManager.get_sound_volume()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.back_button:
            self.back_button.check_mouse_hover(x, y)
        if self.language_button:
            self.language_button.check_mouse_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Проверяем клик по кнопке смены языка
            if self.language_button and self.language_button.check_mouse_hover(x, y):
                self.language_button.on_click()
                if self.language_button._is_active:
                    self.toggle_language()
                    # Сбрасываем состояние кнопки
                    self.language_button._is_active = False
                    self.language_button.check_mouse_hover(0, 0)

            # Проверяем клик по кнопке возврата
            elif self.back_button and self.back_button.check_mouse_hover(x, y):
                self.back_button.on_click()
                if self.back_button._is_active:
                    self.go_back()

    def go_back(self):
        self.manager.disable()
        if self.back_callback:
            self.back_callback()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.go_back()

    def on_hide_view(self):
        self.manager.disable()

    def on_master_volume_change(self, value):
        self.master_volume = value
        self.master_value_label.text = f'{int(value * 100)}%'

        SettingsManager.update_master_volume(value)

        SettingsManager.save()

    def on_ghost_volume_change(self, value):
        self.ghost_volume = value
        self.ghost_value_label.text = f'{int(value * 100)}%'

        SettingsManager.update_ghost_volume(value)

        SettingsManager.save()

    def toggle_language(self):
        # Меняем индекс
        constants.LANGUAGE_INDEX = 1 - constants.LANGUAGE_INDEX

        # Обновляем через SettingsManager
        SettingsManager.update_language(constants.LANGUAGES[constants.LANGUAGE_INDEX])

        # Сохраняем
        SettingsManager.save()

        # Обновляем текст кнопки
        self.language_button.base_text = self.language_button_texts[constants.LANGUAGE_INDEX]
        self.language_button.text = f'< {self.language_button_texts[constants.LANGUAGE_INDEX]} >'

        # Обновляем все тексты
        self.update_ui_texts()

    def update_ui_texts(self):
        # Все тексты через список по индексу
        title_texts = ['НАСТРОЙКИ', 'SETTINGS']
        self.title_label.text = title_texts[constants.LANGUAGE_INDEX]

        master_texts = ['ГРОМКОСТЬ ИГРЫ:', 'MASTER VOLUME:']
        ghost_texts = ['ГРОМКОСТЬ ПРИЗРАКА:', 'GHOST VOLUME:']
        back_texts = ['НАЗАД', 'BACK']
        lang_texts = ['ЯЗЫК: РУССКИЙ', 'LANGUAGE: ENGLISH']

        # Обновляем метки слайдеров
        if len(self.box_layout_settings.children) >= 1:
            master_container = self.box_layout_settings.children[0]
            if isinstance(master_container, UIBoxLayout) and len(master_container.children) > 0:
                master_label = master_container.children[0]
                if isinstance(master_label, UILabel):
                    master_label.text = master_texts[constants.LANGUAGE_INDEX]

        if len(self.box_layout_settings.children) >= 2:
            ghost_container = self.box_layout_settings.children[1]
            if isinstance(ghost_container, UIBoxLayout) and len(ghost_container.children) > 0:
                ghost_label = ghost_container.children[0]
                if isinstance(ghost_label, UILabel):
                    ghost_label.text = ghost_texts[constants.LANGUAGE_INDEX]

        # Обновляем кнопки
        self.back_button.base_text = back_texts[constants.LANGUAGE_INDEX]
        self.back_button.text = f'< {back_texts[constants.LANGUAGE_INDEX]} >'
        self.language_button.base_text = lang_texts[constants.LANGUAGE_INDEX]
        self.language_button.text = f'< {lang_texts[constants.LANGUAGE_INDEX]} >'
