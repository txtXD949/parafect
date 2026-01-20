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
    TEXTURES = [
        './assets/images/itms/incense.png',
        './assets/images/itms/incense_1.png',
        './assets/images/itms/incense_2.png',
        './assets/images/itms/incense_3.png',
        './assets/images/itms/incense_4.png'
    ]
    SOUNDS = [
        arcade.load_sound('./assets/sounds/effects/smoke_incense.wav')
    ]

    def __init__(self):
        super().__init__('incense', 'Благовония', sprite=None)

        # состояние горения
        self.phase = 0  # 0-4
        self.phase_timer = 0.0
        self.is_burning = False
        self.sound_player = None

        # частицы дыма
        self.smoke_particles = arcade.SpriteList()

        # ссылка на игрока
        self.player = None

    def use_item(self, player):
        if self.phase > 0 or self.is_burning:
            return

        if not player.has_lighter:
            return

        self.phase = 1
        self.phase_timer = 2.0
        self.is_burning = True
        self.player = player

        player.is_unhittable = True

        self.sound_player = arcade.play_sound(self.SOUNDS[0])

        self.sprite.texture = arcade.load_texture(self.TEXTURES[1])

    def update_smoke(self, delta_time):
        if not self.is_burning:
            return

        if random.random() < 0.4:
            smoke = arcade.SpriteSolidColor(4, 4, arcade.color.WHITE_SMOKE)
            smoke.center_x = self.sprite.center_x + random.randint(-6, 6)
            smoke.center_y = self.sprite.top + random.randint(2, 6)
            smoke.change_y = random.uniform(25, 45)
            smoke.change_x = random.uniform(-8, 8)
            smoke.life = 1.8
            self.smoke_particles.append(smoke)

        for smoke in self.smoke_particles[:]:
            smoke.center_x += smoke.change_x * delta_time
            smoke.center_y += smoke.change_y * delta_time
            smoke.life -= delta_time

            alpha_ratio = max(0.0, smoke.life / 1.8)
            alpha = int(255 * alpha_ratio)
            smoke.color = (200, 200, 210, alpha)

            if smoke.life <= 0:
                smoke.kill()

    def update_phase(self, delta_time):
        if not self.is_burning:
            return

        self.phase_timer -= delta_time

        if self.phase_timer <= 0:
            self.phase += 1

            if self.phase >= 4:
                self.phase = 4
                self.is_burning = False
                self.smoke_particles.clear()

                if self.player:
                    self.player.is_unhittable = False
                    self.player = None
                return

            self.phase_timer = 2.0
            self.sprite.texture = arcade.load_texture(self.TEXTURES[self.phase])
            if self.sound_player:
                self.sound_player.pause()
            self.sound_player = arcade.play_sound(self.SOUNDS[0])

    def update_item(self, player_sprite):
        super().update_item(player_sprite)

        self.update_phase(1 / 60.0)
        self.update_smoke(1 / 60.0)

        self.smoke_particles.draw()

    def take_item(self, player):
        if self.phase > 0:
            return False
        return True

    def turn_on(self):
        pass

    def turn_off(self):
        pass


class Lighter(Item):
    TEXTURES = [
        '././assets/images/itms/light.png'
    ]

    def __init__(self):
        super().__init__('lighter', 'Зажигалка', sprite=None)

    def use_item(self, player):
        if player.has_lighter:
            return
        player.has_lighter = True

    def turn_on(self):
        pass

    def turn_off(self):
        pass


class Pills(Item):
    TEXTURES = [
        '././assets/images/itms/pills.png'
    ]
    SOUNDS = [
        arcade.load_sound('./assets/sounds/effects/pills.wav')
    ]

    def __init__(self, reg_sanity):
        super().__init__('pills', 'Успокоительное', sprite=None)

        self._reg_sanity = reg_sanity

        self.used = False
        self.to_use = False

    def use_item(self, player):
        if self.used:
            return

        self.used = True

        Item.sound_player = arcade.play_sound(self.SOUNDS[0])

        player.sanity = min(100, player.sanity + self._reg_sanity)
        player.drop_item()
