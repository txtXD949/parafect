import arcade
from arcade.gui import UIWidget, UIBoxLayout, UIAnchorLayout, UIManager
from arcade.gui.widgets import UIDummy
from arcade.gui.widgets.buttons import UIFlatButton, UITextureButton

from .. import GHOSTS

E = []


class JournalButton(UITextureButton):

    def __init__(self, text, width, height, journal_widget, type, *, ghost=None, evidence=None):
        self.journal_widget = journal_widget
        self.circle_tex = arcade.load_texture('././assets/images/ui/circle_button.png')
        self.cross_tex = arcade.load_texture('././assets/images/ui/cross_button.png')
        self.drow_tex = arcade.load_texture('././assets/images/ui/drow_button.png')

        self.state = 0
        self.disabled = False

        self.type = type
        self.ghost = ghost
        self.evidence = evidence

        super().__init__(
            text=text,
            width=width,
            height=height,
            texture=None,
            multiline=True,
            style={
                "normal": {
                    "font_name": 'Correction Tape',
                    "font_size": 18,
                    "font_color": arcade.color.BLACK,
                },
                "hover": {
                    "font_name": 'Correction Tape',
                    "font_size": 18,
                    "font_color": arcade.color.EERIE_BLACK,
                },
                "press": {
                    "font_name": 'Correction Tape',
                    "font_size": 18,
                    "font_color": arcade.color.BLACK,
                },
                "disabled": {
                    "font_name": 'Correction Tape',
                    "font_size": 18,
                    "font_color": arcade.color.GRAY,
                }
            }
        )

    def on_click(self, event):
        if self.disabled:
            return

        if self.type == 'ghost':
            self.state = (self.state + 1) % 3
            self._update_visual()
            return

        self.state = (self.state + 1) % 3

        if self.type == 'evidence':
            circled_evidences = []
            crossed_evidences = []

            for btn in self.journal_widget.evidence_buttons:
                if btn.state == 1 and btn.evidence:
                    circled_evidences.append(btn.evidence)
                elif btn.state == 2 and btn.evidence:
                    crossed_evidences.append(btn.evidence)

            for ghost_btn in self.journal_widget.ghost_buttons:
                is_valid = True

                for ev in circled_evidences:
                    if ev not in ghost_btn.ghost.evidences:
                        is_valid = False
                        break

                for ev in crossed_evidences:
                    if ev in ghost_btn.ghost.evidences:
                        is_valid = False
                        break

                ghost_btn.disabled = not is_valid

                ghost_btn._update_visual()

        self._update_visual()

    def _update_visual(self):
        if self.type == 'ghost' and self.disabled:
            # Для заблокированных кнопок призраков показываем drow_texture
            self.texture = self.drow_tex
            self.texture_hovered = self.drow_tex
            self.texture_pressed = self.drow_tex

            # Меняем цвет текста
            self.style['normal']['font_color'] = arcade.color.DARK_GRAY
            self.style['hover']['font_color'] = arcade.color.DARK_GRAY
            self.style['press']['font_color'] = arcade.color.DARK_GRAY
        else:
            # Нормальная логика для активных кнопок и evidence
            if self.state == 1:
                self.texture = self.circle_tex
                self.texture_hovered = self.circle_tex
                self.texture_pressed = self.circle_tex
            elif self.state == 2:
                self.texture = self.cross_tex
                self.texture_hovered = self.cross_tex
                self.texture_pressed = self.cross_tex
            else:
                self.texture = None
                self.texture_hovered = None
                self.texture_pressed = None


class JournalWidget(UIWidget):
    def __init__(self, width: float, height: float, stretch_x, stretch_y, **kwargs):
        super().__init__(**kwargs)
        self.bg_texture = arcade.load_texture('././assets/images/bg/paper.png').transpose()

        self.width = width
        self.height = height

        self.stretch_x = stretch_x
        self.stretch_y = stretch_y

        self.visible = False

        main_container = UIAnchorLayout(
            anchor_x="center",
            anchor_y="center",
            width=width * self.stretch_x,
            height=height * self.stretch_y
        ).with_background(texture=self.bg_texture)
        self.add(main_container)

        content_layout = UIBoxLayout(
            vertical=True,
            width=width * self.stretch_x * 0.9,
            height=height * self.stretch_y * 0.9,
            space_between=15
        )
        main_container.add(content_layout)

        self.evidence_buttons = []
        self.create_section(
            content_layout,
            [
                'ЭМП5', 'Радиоприемник', 'Голос в микрофоне',
                'Отпечатки', 'Высокая температура',
                'Низкая температура', 'Записи в блокноте'
            ],
            rows=3,
            section_height=content_layout.height * 0.4,
            lst=self.evidence_buttons,
            type='evidence',
            ghosts_evidences=[
                'emf5', 'dict', 'mic',
                'uf', 'hot_temp',
                'cold_temp', 'book'
            ]
        )

        self.ghost_buttons = []
        self.create_section(
            content_layout,
            [
                'Дух', 'Демон', 'Фантом', 'Они',
                'Банши', 'Ревенант', 'Мюлинг',
                'Полтергейст', 'Мимик', 'Тень',
                'Мясник', 'Мираж', 'Сирена'
            ],
            rows=5,
            section_height=content_layout.height * 0.45,
            lst=self.ghost_buttons,
            type='ghost',
            ghosts_evidences=list(map(lambda x: x(), GHOSTS))
        )

    def create_section(self, parent, button_texts, rows, section_height, lst, type, ghosts_evidences):
        for row in range(rows):
            row_height = section_height / rows
            row_layout = UIBoxLayout(
                vertical=False,
                width=parent.width,
                height=row_height,
                space_between=5
            )

            for col in range(3):
                index = row * 3 + col
                if index < len(button_texts):
                    button_width = parent.width / 3 - 10
                    button = self.create_blue_button(button_texts[index], button_width, row_height - 10, type,
                                                     ghosts_evidences[index])
                    row_layout.add(button)
                    lst.append(button)

            parent.add(row_layout)

    def get_circled_ghosts(self):
        ...

    def create_blue_button(self, text, width, height, type, ghost_evidence):
        arcade.load_font('././assets/fonts/CorrectionTape.otf')

        if type == 'ghost':
            button = JournalButton(
                text=text,
                width=width,
                height=height,
                journal_widget=self,
                type=type,
                ghost=ghost_evidence
            )
        elif type == 'evidence':
            button = JournalButton(
                text=text,
                width=width,
                height=height,
                journal_widget=self,
                type=type,
                evidence=ghost_evidence
            )

        return button
