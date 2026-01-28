import arcade
import random
import time

import pyaudio as pa
import numpy as np
import threading


# TODO: сделать нормальные шансы


class Item:
    TURN_ON_OFF_SOUNDS = [
        arcade.load_sound('./assets/sounds/effects/turn_on_off_item.wav'),
        arcade.load_sound('./assets/sounds/effects/turn_on_off_item.wav')
    ]

    def __init__(self, id, name, is_stationary=False, is_grabbed=False, in_inventory=False, is_turn_on=False,
                 sprite=None, board_scale=5.0):
        self._id = id
        self._name = name
        self._is_stationary = is_stationary
        self._is_grabbed = is_grabbed
        self._in_inventory = in_inventory
        self._is_turn_on = is_turn_on
        self._sprite = sprite

        self.board_sprite = None
        self.board_scale = board_scale

        self._in_room = False
        self.on_board = True

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
        if not self.is_turn_on:
            arcade.play_sound(self.TURN_ON_OFF_SOUNDS[0])
        self.is_turn_on = True

    def turn_off(self):
        if self.is_turn_on:
            arcade.play_sound(self.TURN_ON_OFF_SOUNDS[1])
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

    def create_board_sprite(self):
        self.board_sprite = arcade.Sprite(self.TEXTURES[0], self.board_scale)
        self.board_sprite._class = self

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

        if random.random() < 0.00015:
            if 'emf5' in evidences and random.random() < 0.2:
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
    TURN_ON_OFF_SOUNDS = [
        arcade.load_sound('./assets/sounds/effects/flashlight_on.wav'),
        arcade.load_sound('./assets/sounds/effects/flashlight_off.wav')
    ]
    TEXTURES = [
        './assets/images/itms/flash_light.png'
    ]
    SOUNDS = [
        ...
    ]

    def __init__(self):
        super().__init__('flash-light', 'Фонарик', sprite=None, board_scale=2.8)


class UF(Item):
    TURN_ON_OFF_SOUNDS = [
        arcade.load_sound('./assets/sounds/effects/flashlight_on.wav'),
        arcade.load_sound('./assets/sounds/effects/flashlight_off.wav')
    ]
    TEXTURES = [
        './assets/images/itms/uf.png'
    ]
    SOUNDS = [
        ...
    ]

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

        if not self.wrote and random.random() < 0.00007:
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
        super().__init__('mic', 'Направленный микрофон', sprite=None, board_scale=4.0)

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
            if random.random() < 0.0001:
                self.sound_player = arcade.play_sound(self.SPEC_SOUNDS[1])
                return

        if ghost.id == 'banshee':
            if random.random() < 0.0001:
                self.sound_player = arcade.play_sound(self.SPEC_SOUNDS[0])
                return

        if 'mic' in evidence and random.random() < 0.0003:
            self.sound_player = arcade.play_sound(random.choice(self.SOUNDS))


class Dictaphone(Item):
    TEXTURES = [
        './assets/images/itms/dict_off.png',
        './assets/images/itms/dict_on.png'
    ]
    SOUNDS = [arcade.load_sound('././assets/sounds/effects/dict_noise.wav')] + [
        arcade.load_sound(f'././assets/sounds/effects/dict_say{i}.wav') for i in range(1, 18)
    ] + [arcade.load_sound('././assets/sounds/effects/dict_siren.wav')]

    def __init__(self):
        super().__init__('dict', 'Диктофон', sprite=None, board_scale=3.0)

        self.pa = pa.PyAudio()
        self.stream = False
        self.is_capt = False
        self.audio_buffer = []

        self.chunk = 1024
        self.form = pa.paInt16
        self.channels = 1
        self.rate = 44100

        self.voice_detected = False
        self.last_voice_time = 0.5

        self.ghost_voice = None

    def start_capture(self):
        if self.stream or self.is_capt:
            return

        self.is_capt = True
        self.audio_buffer = []

        self.stream = self.pa.open(
            format=self.form,
            channels=self.channels,
            rate=self.rate,
            input_device_index=0,
            input=True,
            frames_per_buffer=self.chunk,
            stream_callback=self.audio_callback
        )

        self.stream.start_stream()

    def stop_capture(self):
        self.is_capt = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def audio_callback(self, in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        self.audio_buffer.append(audio_data)

        if len(self.audio_buffer) * self.chunk / self.rate > 10.0:
            self.audio_buffer.pop(0)

        return in_data, pa.paContinue

    def get_voice_volume(self):
        if not self.audio_buffer:
            return 0.0

        recent_chunk = 20
        recent_data = np.concatenate(self.audio_buffer[-recent_chunk:])

        if not len(recent_data):
            return 0.0

        rms = np.sqrt(np.mean(recent_data.astype(np.float32) ** 2))
        volume = min(1.0, rms / 32768 * 5.0)

        return volume

    def update_voice_detection(self, player):
        volume = self.get_voice_volume()
        player.voice_vol = volume

        player.is_voice = volume > player.threshold

        if player.is_voice and not self.voice_detected:
            self.voice_detected = True
            self.last_voice_time = time.time()
        elif time.time() - self.last_voice_time > 1.0:
            self.voice_detected = False

    def turn_on(self):
        super().turn_on()
        self.start_capture()
        self.sprite.texture = arcade.load_texture(self.TEXTURES[1])
        self.sound_player = arcade.play_sound(self.SOUNDS[0], loop=True)

    def turn_off(self):
        super().turn_off()
        self.stop_capture()
        self.sprite.texture = arcade.load_texture(self.TEXTURES[0])
        if self.sound_player:
            self.sound_player.pause()

    def use_item(self, _, ghost, evidences):
        if not self.is_turn_on or not self.in_room:
            return

        if ghost.id == 'siren' and random.random() < 0.0001:
            self.ghost_voice = arcade.play_sound(self.SOUNDS[-1])
            return

        if 'dict' not in evidences:
            return

        if self.voice_detected and random.random() < 0.0003:
            self.ghost_voice = arcade.play_sound(random.choice(self.SOUNDS[1:-1]))


class Thermometer(Item):
    TEXTURES = [
        './assets/images/itms/term_norm.png',
        './assets/images/itms/term_cold.png',
        './assets/images/itms/term_hot.png'
    ]

    def __init__(self):
        super().__init__('term', 'Термометр', sprite=None, board_scale=3.1)

    def use_item(self, evidences):
        if not self.in_room:
            self.sprite.texture = arcade.load_texture(self.TEXTURES[0])
            return

        if 'cold_temp' in evidences and random.random() < 0.00007:
            self.sprite.texture = arcade.load_texture(self.TEXTURES[1])
            return

        if 'hot_temp' in evidences and random.random() < 0.00007:
            self.sprite.texture = arcade.load_texture(self.TEXTURES[2])
            return

    def turn_on(self):
        pass

    def turn_off(self):
        pass


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

        # Замедление призрака
        self.slow_duration = 10.0
        self.slow_power = 0.3
        self.protection_duration = 90.0
        self.ghost_slowed = False

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

    def check_ghost_collision(self, ghost_sprite):
        if not self.is_burning or not ghost_sprite.visible:
            return False

        for smoke in self.smoke_particles:
            if arcade.check_for_collision(smoke, ghost_sprite):
                return True

        return False

    def apply_slow_to_ghost(self, ghost):
        if self.ghost_slowed:
            return

        # Определяем длительность защиты
        if ghost.id == 'spirit':
            protection = 180.0  # 3 минуты для Духа
        else:
            protection = self.protection_duration  # 1.5 минуты для остальных

        # Замедляем призрака
        original_speed = ghost.physics.base_speed
        ghost.physics.base_speed *= self.slow_power

        # Восстанавливаем через slow_duration секунд
        arcade.schedule(
            lambda dt: setattr(ghost.physics, 'base_speed', original_speed),
            self.slow_duration
        )

        # Останавливаем охоту
        ghost.stop_timer = max(ghost.stop_timer, self.protection_duration)

        self.ghost_slowed = True

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
        super().__init__('lighter', 'Зажигалка', sprite=None, board_scale=1.0)

    def use_item(self, player):
        if player.has_lighter:
            return
        arcade.play_sound(arcade.load_sound('./assets/sounds/effects/take_item.wav'))
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
        super().__init__('pills', 'Успокоительное', sprite=None, board_scale=2.0)

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

    def turn_on(self):
        pass

    def turn_off(self):
        pass
