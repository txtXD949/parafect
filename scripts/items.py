import arcade
import random


class Item:
    def __init__(self, id, name, is_grabbed=False, in_inventory=False, is_turn_on=False, sprite=None):
        self._id = id
        self._name = name
        self._is_grabbed = is_grabbed
        self._in_inventory = in_inventory
        self._is_turn_on = is_turn_on
        self._sprite = sprite


    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def is_grabbed(self):
        return self._is_grabbed

    @is_grabbed.setter
    def is_grabbed(self, new_val):
        self._is_grabbed = new_val

    @property
    def in_inventory(self):
        return self._in_inventory

    @in_inventory.setter
    def in_inventory(self, new_val):
        self._in_inventory = new_val

    @property
    def is_turn_on(self):
        return self._is_turn_on

    @is_turn_on.setter
    def is_turn_on(self, new_val):
        self._is_turn_on = new_val

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, new_sprite):
        self._sprite = new_sprite


    def update_item(self, player_sprite):
        if not self.is_grabbed:
            if self.in_inventory:
                self.sprite.visible = False
                self.sprite.center_x = player_sprite.center_x - 10
                self.sprite.center_y = player_sprite.center_y - 10
            return

        self.sprite.visible = True
        self.sprite.center_x = player_sprite.center_x - 10
        self.sprite.center_y = player_sprite.center_y - 10

    def create_sprite(self, scale):
        self.sprite = arcade.Sprite(self.TEXTURES[0], scale)
        self.sprite._class = self

    def use_item(self, *args):
        ...

    def __str__(self):
        return self.id + ' ' + self.name


class EMF(Item):
    TEXTURES = []

    def __init__(self):
        super().__init__('emf', 'ЭМП', sprite=None)


class UF(Item):
    TEXTURES = []

    def __init__(self):
        super().__init__('uf', 'УФ-фонарик', sprite=None)


class Book(Item):
    TEXTURES = []

    def __init__(self):
        super().__init__('book', 'Блокнот', sprite=None)


class Microphone(Item):
    TEXTURES = [
        './assets/images/itms/mic.png'
    ]

    def __init__(self):
        super().__init__('mic', 'Направленный микрофон', sprite=None)


class Dictaphone(Item):
    TEXTURES = []

    def __init__(self):
        super().__init__('dict', 'Диктофон', sprite=None)


class Thermometer(Item):
    TEXTURES = [
        './assets/images/itms/term_norm.png',
        './assets/images/itms/term_cold.png',
        './assets/images/itms/term_hot.png'
    ]

    def __init__(self):
        super().__init__('term', 'Термометр', sprite=None)

    def use_item(self, evidence=None, got_before=False):
        if got_before:
            return

        if evidence is None:
            self.sprite.texture = self.TEXTURES[2]
            return '...'

        if evidence == 'cold_temp':
            if random.random() < 0.007:
                self.sprite.texture = self.TEXTURES[0]
                return ('Брр.. холодно тут,', 'Брр,')[random.randint(0, 1)]
            else:
                return '...'

        if evidence == 'hot_temp':
            if random.random() < 0.007:
                self.sprite.texture = self.TEXTURES[1]
                return ('Жарко..,',)[random.randint(0, 0)]
            else:
                return '...'


class FlashLight(Item):
    TEXTURES = []

    def __init__(self):
        super().__init__('flash-light', 'Фонарик', sprite=None)


class PhotoCamera(Item):
    TEXTURES = []

    def __init__(self):
        super().__init__('camera', 'Фотокамера', sprite=None)


class Incense(Item):
    TEXTURES = []

    def __init__(self):
        super().__init__('incense', 'Благовония', sprite=None)


class Lighter(Item):
    TEXTURES = []

    def __init__(self):
        super().__init__('incense', 'Зажигалка', sprite=None)


class Pills(Item):
    TEXTURES = []

    def __init__(self):
        super().__init__('pills', 'Успокоительное', sprite=None)
