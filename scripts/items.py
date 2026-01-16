class Item:
    def __init__(self, id, name, is_grabbed=False, is_turn_on=False, sprite=None):
        self._id = id
        self._name = name
        self._is_grabbed = is_grabbed
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
    TEXTURES = []

    def __init__(self):
        super().__init__('mic', 'Направленный микрофон', sprite=None)


class Dictaphone(Item):
    TEXTURES = []

    def __init__(self):
        super().__init__('dict', 'Диктофон', sprite=None)


class Thermometer(Item):
    TEXTURES = []

    def __init__(self):
        super().__init__('term', 'Термометр', sprite=None)


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
