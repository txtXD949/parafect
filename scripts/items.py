import arcade
import random
import time

import pyaudio as pa
import numpy as np
import threading

from .views import SettingsManager
from .sounds import *


class Item:
    TURN_ON_OFF_SOUNDS = [
        TURN_OFF_ITEM,
        TURN_ON_ITEM
    ]

    def __init__(self, id, name, is_stationary=False, is_grabbed=False, in_inventory=False, is_turn_on=False,
                 sprite=None, board_scale=5.0, bias_scale=1):
        self._id = id
        self._name = name
        self._is_stationary = is_stationary
        self._is_grabbed = is_grabbed
        self._in_inventory = in_inventory
        self._is_turn_on = is_turn_on
        self._sprite = sprite
        self.bias_scale = bias_scale

        self.board_sprite = None
        self.board_scale = board_scale

        self._in_room = False
        self.on_board = True

        self.sound_player = None

        # Для сбоев при охоте
        self.is_malfunctioning = False
        self.malfunction_timer = 0
        self.malfunction_duration = random.uniform(3.0, 8.0)

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
            vol = SettingsManager.get_sound_volume()
            arcade.play_sound(self.TURN_ON_OFF_SOUNDS[0], volume=vol)
        self.is_turn_on = True

    def turn_off(self):
        if self.is_turn_on:
            vol = SettingsManager.get_sound_volume()
            arcade.play_sound(self.TURN_ON_OFF_SOUNDS[1], volume=vol)
        self.is_turn_on = False
        if self.sound_player:
            self.sound_player.pause()

    def update_item(self, player_sprite):
        if not self.is_grabbed:
            if self.in_inventory:
                self.sprite.visible = False
                self.sprite.center_x = player_sprite.center_x - 10 * self.bias_scale
                self.sprite.center_y = player_sprite.center_y - 10 * self.bias_scale
            return

        self.sprite.visible = True
        self.sprite.center_x = player_sprite.center_x - 10 * self.bias_scale
        self.sprite.center_y = player_sprite.center_y - 10 * self.bias_scale

    def create_sprite(self, scale):
        self.sprite = arcade.Sprite(self.TEXTURES[0], scale)
        self.sprite._class = self

    def create_board_sprite(self):
        self.board_sprite = arcade.Sprite(self.TEXTURES[0], self.board_scale)
        self.board_sprite._class = self

    def use_item(self, *args):
        ...

    def update_malfunction(self, is_hunt_active, delta_time):
        if is_hunt_active and not self.is_malfunctioning:
            if random.random() < 0.1:
                self.start_malfunction()

        if self.is_malfunctioning:
            self.malfunction_timer -= delta_time
            if self.malfunction_timer <= 0:
                self.stop_malfunction()

    def start_malfunction(self):
        self.is_malfunctioning = True
        self.malfunction_timer = self.malfunction_duration

    def stop_malfunction(self):
        self.is_malfunctioning = False
        self.malfunction_timer = 0

    def is_working_correctly(self):
        """Проверяет работает ли предмет нормально"""
        return not self.is_malfunctioning


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
        EMF3,
        EMF4,
        EMF5,
    ]

    def __init__(self, bias_scale=1):
        super().__init__('emf', ('ЭМП', 'EMF'), False, sprite=None, bias_scale=bias_scale)

        self.is_working = False

        self.active_until = 0.0
        self.active_level_index = None

    def use_item(self, evidences):
        now = time.time()

        if self.is_malfunctioning:
            if not self.is_turn_on:
                self.sprite.texture = arcade.load_texture(self.TEXTURES[0])
                return

            if random.random() < 0.3:
                false_level = random.choice([2, 3, 4])
                self.sprite.texture = arcade.load_texture(self.TEXTURES[false_level])

                if false_level in [3, 4, 5] and self.SOUNDS[false_level]:
                    if self.sound_player:
                        self.sound_player.pause()
                    vol = SettingsManager.get_sound_volume()
                    self.sound_player = arcade.play_sound(self.SOUNDS[false_level], loop=True, volume=vol)
                    self.is_working = True
                    self.active_level_index = false_level
                    self.active_until = now + random.uniform(3.0, 8.0)
            else:
                self.sprite.texture = arcade.load_texture(self.TEXTURES[1])

            return

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

        if random.random() < 0.0003 * 60:
            if 'emf5' in evidences and random.random() < 0.5:
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
            vol = SettingsManager.get_sound_volume()
            self.sound_player = arcade.play_sound(self.SOUNDS[level_index], loop=True, volume=vol)


class FlashLight(Item):
    TURN_ON_OFF_SOUNDS = [
        TURN_ON_FLSH,
        TURN_OFF_FLSH
    ]
    TEXTURES = [
        './assets/images/itms/flash_light.png'
    ]
    SOUNDS = [
        ...
    ]

    def __init__(self, bias_scale=1):
        super().__init__('flash-light', ('Фонарик', 'FlashLight'), sprite=None, board_scale=2.8, bias_scale=bias_scale)


class LowFlashlight(Item):
    TURN_ON_OFF_SOUNDS = [
        TURN_ON_FLSH,
        TURN_OFF_FLSH
    ]
    TEXTURES = [
        './assets/images/itms/uf.png'
    ]
    SOUNDS = [
        ...
    ]

    def __init__(self, bias_scale=1):
        super().__init__('low_light', ('Слабый фонарик', 'Low flashlight'), sprite=None, bias_scale=bias_scale)


class Book(Item):
    TEXTURES = [
        '././assets/images/itms/book1.png',
        '././assets/images/itms/book2.png'
    ]
    SOUNDS = [
        BOOK_WRITINGS
    ]

    def __init__(self, bias_scale=1):
        super().__init__('book', ('Блокнот', 'Book'), is_stationary=True, sprite=None, bias_scale=bias_scale)

        self.is_dropped = False
        self.wrote = False

    def use_item(self, evidences):
        if 'book' not in evidences:
            return

        if not self.is_dropped:
            return

        if not self.in_room:
            return

        if not self.wrote and random.random() < 0.001:
            self.sprite.texture = arcade.load_texture(self.TEXTURES[1])
            vol = SettingsManager.get_sound_volume()
            self.sound_player = arcade.play_sound(self.SOUNDS[0], volume=vol)
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
        WHISPER_MIC1,
        WHISPER_MIC2,
        WHISPER_MIC3,
        WHISPER_MIC4,
        WHISPER_MIC5,
        WHISPER_MIC6,
        WHISPER_MIC7

    ]
    SPEC_SOUNDS = [
        WHISPER_MIC_BANSHEE,
        WHISPER_MIC_MULING
    ]

    def __init__(self, bias_scale=1):
        super().__init__('mic', ('Направленный микрофон', 'Directional microphone'), sprite=None, board_scale=4.0, bias_scale=bias_scale)

    def use_item(self, evidence, ghost, sound_players=None):
        if not sound_players:
            sound_players = []

        if self.is_malfunctioning:
            if not self.is_turn_on:
                self.sprite.texture = arcade.load_texture(self.TEXTURES[0])
                return

            self.sprite.texture = arcade.load_texture(self.TEXTURES[1])

            if random.random() < 0.25:
                vol = SettingsManager.get_sound_volume()
                self.sound_player = arcade.play_sound(random.choice(self.SOUNDS), volume=vol)

            return

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
            if random.random() < 0.0001 * 60:
                vol = SettingsManager.get_sound_volume()
                self.sound_player = arcade.play_sound(self.SPEC_SOUNDS[1], volume=vol)
                return

        if ghost.id == 'banshee':
            if random.random() < 0.0001 * 60:
                vol = SettingsManager.get_sound_volume()
                self.sound_player = arcade.play_sound(self.SPEC_SOUNDS[0], volume=vol)
                return

        if 'mic' in evidence and random.random() < 0.0003 * 60:
            vol = SettingsManager.get_sound_volume()
            self.sound_player = arcade.play_sound(random.choice(self.SOUNDS), volume=vol)


class Radio(Item):
    TEXTURES = [
        './assets/images/itms/dict_off.png',
        './assets/images/itms/dict_on.png'
    ]
    SOUNDS = [DICT_NOISE] + DICT_SAYS + [DICT_SAY_SIREN]

    def __init__(self, bias_scale=1):
        super().__init__('dict', ('Радиоприемник', 'Radio'), sprite=None, board_scale=3.0, bias_scale=bias_scale)

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
        vol = SettingsManager.get_sound_volume()
        self.sound_player = arcade.play_sound(self.SOUNDS[0], loop=True, volume=vol)

    def turn_off(self):
        super().turn_off()
        self.stop_capture()
        self.sprite.texture = arcade.load_texture(self.TEXTURES[0])
        if self.sound_player:
            self.sound_player.pause()

    def use_item(self, _, ghost, evidences):
        if self.is_malfunctioning:
            if not self.is_turn_on or not self.in_room:
                return

            if random.random() < 0.2:
                if random.random() < 0.7:
                    vol = SettingsManager.get_sound_volume()
                    self.ghost_voice = arcade.play_sound(random.choice(self.SOUNDS[1:-1]), volume=vol)
                else:
                    vol = SettingsManager.get_sound_volume()
                    self.ghost_voice = arcade.play_sound(self.SOUNDS[-1], volume=vol)

            return

        if not self.is_turn_on or not self.in_room:
            return

        if ghost.id == 'siren' and random.random() < 0.0002 * 60:
            vol = SettingsManager.get_sound_volume()
            self.ghost_voice = arcade.play_sound(self.SOUNDS[-1], volume=vol)
            return

        if 'dict' not in evidences:
            return

        if self.voice_detected and random.random() < 0.0006 * 60:
            vol = SettingsManager.get_sound_volume()
            self.ghost_voice = arcade.play_sound(random.choice(self.SOUNDS[1:-1]), volume=vol)


class Thermometer(Item):
    TEXTURES = [
        './assets/images/itms/term_norm.png',
        './assets/images/itms/term_cold.png',
        './assets/images/itms/term_hot.png'
    ]

    def __init__(self, bias_scale=1):
        super().__init__('term', ('Термометр', 'Thermometer'), sprite=None, board_scale=3.1, bias_scale=bias_scale)

    def use_item(self, evidences):
        if not self.in_room:
            self.sprite.texture = arcade.load_texture(self.TEXTURES[0])
            return

        if 'cold_temp' in evidences and random.random() < 0.001:
            self.sprite.texture = arcade.load_texture(self.TEXTURES[1])
            return

        if 'hot_temp' in evidences and random.random() < 0.0001:
            self.sprite.texture = arcade.load_texture(self.TEXTURES[2])
            return

    def turn_on(self):
        pass

    def turn_off(self):
        pass


class PhotoCamera(Item):
    TEXTURES = []

    def __init__(self, bias_scale=1):
        super().__init__('camera', ('Фотокамера', 'Camera'), sprite=None, bias_scale=bias_scale)


class Incense(Item):
    TEXTURES = [
        './assets/images/itms/incense.png',
        './assets/images/itms/incense_1.png',
        './assets/images/itms/incense_2.png',
        './assets/images/itms/incense_3.png',
        './assets/images/itms/incense_4.png'
    ]
    SOUNDS = [
        INCENSE_BURN
    ]

    def __init__(self, bias_scale=1):
        super().__init__('incense', ('Благовония', 'Incense'), sprite=None, bias_scale=bias_scale)

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

        vol = SettingsManager.get_sound_volume()
        self.sound_player = arcade.play_sound(self.SOUNDS[0], volume=vol)
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
            vol = SettingsManager.get_sound_volume()
            self.sound_player = arcade.play_sound(self.SOUNDS[0], volume=vol)

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

    def __init__(self, bias_scale=1):
        super().__init__('lighter', ('Зажигалка', 'Lighter'), sprite=None, board_scale=1.0, bias_scale=bias_scale)

    def use_item(self, player):
        if player.has_lighter:
            return
        vol = SettingsManager.get_sound_volume()
        arcade.play_sound(TAKE_LIGHTER, volume=vol)
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
        TAKE_PILLS
    ]

    def __init__(self, reg_sanity, bias_scale=1):
        super().__init__('pills', ('Успокоительное', 'Pills'), sprite=None, board_scale=2.0, bias_scale=bias_scale)

        self._reg_sanity = reg_sanity

        self.used = False
        self.to_use = False

    def use_item(self, player):
        if self.used:
            return

        self.used = True

        vol = SettingsManager.get_sound_volume()
        Item.sound_player = arcade.play_sound(self.SOUNDS[0], volume=vol)

        player.sanity = min(100, player.sanity + self._reg_sanity)
        player.drop_item()

    def turn_on(self):
        pass

    def turn_off(self):
        pass
