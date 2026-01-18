import arcade
import random
import time


# TODO: сделать нормальные шансы


class Item:
    def __init__(self, id, name, is_stationary=False, is_grabbed=False, in_inventory=False, is_turn_on=False,
                 sprite=None):
        self._id = id
        self._name = name
        self._is_stationary = is_stationary
        self._is_grabbed = is_grabbed
        self._in_inventory = in_inventory
        self._is_turn_on = is_turn_on
        self._sprite = sprite

        self._in_room = False

        self.sound_player = None

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def is_stationary(self):
        return self._is_stationary

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

    @property
    def in_room(self):
        return self._in_room

    @in_room.setter
    def in_room(self, new_val):
        self._in_room = new_val

    def turn_on(self):
        self.is_turn_on = True

    def turn_off(self):
        self.is_turn_on = False
        if self.sound_player:
            self.sound_player.pause()

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
    TEXTURES = [
        './assets/images/itms/emf_off.png',
        './assets/images/itms/emf_on.png',
        './assets/images/itms/emf_3.png',
        './assets/images/itms/emf_4.png',
        './assets/images/itms/emf_5.png',
    ]
    SOUNDS = [
        None, None,
        arcade.load_sound('./assets/sounds/effects/emf_3.wav'),
        arcade.load_sound('./assets/sounds/effects/emf_4.wav'),
        arcade.load_sound('./assets/sounds/effects/emf_5.wav'),
    ]

    def __init__(self):
        super().__init__('emf', 'ЭМП', False, sprite=None)

        self.is_working = False

        self.active_until = 0.0
        self.active_level_index = None

    def use_item(self, evidences):
        now = time.time()

        if not self.is_turn_on:
            self.is_working = False
            self.active_until = 0.0
            self.active_level_index = None
            self.sprite.texture = arcade.load_texture(self.TEXTURES[0])
            if self.sound_player:
                self.sound_player.pause()
            return

        if not self.in_room:
            self.is_working = False
            self.active_until = 0.0
            self.active_level_index = None
            self.sprite.texture = arcade.load_texture(self.TEXTURES[1])
            if self.sound_player:
                self.sound_player.pause()
            return

        if self.is_working and now >= self.active_until:
            self.is_working = False
            self.active_level_index = None
            self.sprite.texture = arcade.load_texture(self.TEXTURES[1])
            if self.sound_player:
                self.sound_player.pause()

        if self.is_working:
            if self.active_level_index is not None:
                self.sprite.texture = arcade.load_texture(self.TEXTURES[self.active_level_index])
            return

        self.sprite.texture = arcade.load_texture(self.TEXTURES[1])

        if random.random() < 0.003:
            if 'emf5' in evidences and random.random() < 0.005:
                level_index = 4
            else:
                level_index = random.choice((2, 3))

            self.is_working = True
            self.active_level_index = level_index

            duration = random.uniform(5.0, 12.0)
            self.active_until = now + duration

            self.sprite.texture = arcade.load_texture(self.TEXTURES[level_index])
            if self.sound_player:
                self.sound_player.pause()
            self.sound_player = arcade.play_sound(self.SOUNDS[level_index], loop=True)


class FlashLight(Item):
    TEXTURES = []

    def __init__(self):
        super().__init__('flash-light', 'Фонарик', sprite=None)


class UF(Item):
    TEXTURES = []

    def __init__(self):
        super().__init__('uf', 'УФ-фонарик', sprite=None)


class Book(Item):
    TEXTURES = [
        '././assets/images/itms/book1.png',
        '././assets/images/itms/book2.png'
    ]
    SOUNDS = [
        arcade.load_sound('././assets/sounds/effects/book_writing.wav')
    ]

    def __init__(self):
        super().__init__('book', 'Блокнот', is_stationary=True, sprite=None)

        self.is_dropped = False
        self.wrote = False

    def use_item(self, evidences):
        if 'book' not in evidences:
            return

        if not self.is_dropped:
            return

        if not self.in_room:
            return

        if not self.wrote and random.random() < 0.01:
            self.sprite.texture = arcade.load_texture(self.TEXTURES[1])
            self.sound_player = arcade.play_sound(self.SOUNDS[0])
            self.wrote = True

    def turn_on(self):
        pass

    def turn_off(self):
        pass


class Microphone(Item):
    TEXTURES = [
        './assets/images/itms/mic_off.png',
        './assets/images/itms/mic_on.png'
    ]
    SOUNDS = [
        arcade.load_sound('./assets/sounds/effects/whisper_1.wav'),
        arcade.load_sound('./assets/sounds/effects/whisper_2.wav'),
        arcade.load_sound('./assets/sounds/effects/whisper_3.wav'),
        arcade.load_sound('./assets/sounds/effects/whisper_4.wav'),
        arcade.load_sound('./assets/sounds/effects/whisper_5.wav'),
        arcade.load_sound('./assets/sounds/effects/whisper_6.wav'),
        arcade.load_sound('./assets/sounds/effects/whisper_7.wav')
    ]
    SPEC_SOUNDS = [
        arcade.load_sound('./assets/sounds/effects/whisper_banshee.wav'),
        arcade.load_sound('./assets/sounds/effects/whisper_muling.wav')
    ]

    def __init__(self):
        super().__init__('mic', 'Направленный микрофон', sprite=None)

    def use_item(self, evidence, ghost, sound_players=None):
        if not sound_players:
            sound_players = []

        if not self.is_turn_on:
            if self.sound_player:
                self.sound_player.pause()
            for sp in sound_players:
                sp.play()
            self.sprite.texture = arcade.load_texture(self.TEXTURES[0])
            return

        self.sprite.texture = arcade.load_texture(self.TEXTURES[1])
        for sp in sound_players:
            sp.pause()

        if not self.in_room:
            return

        if ghost.id == 'muling':
            if random.random() < 0.002:
                self.sound_player = arcade.play_sound(self.SPEC_SOUNDS[1])
                return

        if ghost.id == 'banshee':
            if random.random() < 0.02:
                self.sound_player = arcade.play_sound(self.SPEC_SOUNDS[0])
                return

        if 'mic' in evidence and random.random() < 0.03:
            self.sound_player = arcade.play_sound(random.choice(self.SOUNDS))


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

    def use_item(self, evidences):
        if not self.in_room:
            self.sprite.texture = arcade.load_texture(self.TEXTURES[0])
            return

        if 'cold_temp' in evidences and random.random() < 0.02:
            self.sprite.texture = arcade.load_texture(self.TEXTURES[1])
            return

        if 'hot_temp' in evidences and random.random() < 0.02:
            self.sprite.texture = arcade.load_texture(self.TEXTURES[2])
            return


class PhotoCamera(Item):
    TEXTURES = []

    def __init__(self):
        super().__init__('camera', 'Фотокамера', sprite=None)


class Incense(Item):
    TEXTURES = []

    def __init__(self):
        super().__init__('incense', 'Благовония', sprite=None)


class Lighter(Item):  # TODO: доделать
    TEXTURES = []

    def __init__(self):
        super().__init__('incense', 'Зажигалка', sprite=None)

    def use_item(self, player):
        player.has_lighter = True


class Pills(Item):  # TODO: добавить звуки
    TEXTURES = [
        '././assets/images/itms/pills.png'
    ]

    def __init__(self):
        super().__init__('pills', 'Успокоительное', sprite=None)

        self.used = False
        self.to_use = False

    def use_item(self, player, sanity):
        if self.used or not self.to_use:
            return

        self.used = True

        if player.sanity + sanity >= 100:
            player.sanity = 100
        else:
            player.sanity += sanity

        player.drop_item()
