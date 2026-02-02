import arcade
import enum
import random
import math

from .views import SettingsManager
from .sounds import *


class FootstepParticle(arcade.SpriteSolidColor):
    """Квадратные черные частицы следов"""

    def __init__(self, x, y):
        # Размер
        width = random.randint(1, 3)
        height = random.randint(1, 3)

        color = (20, 20, 20, 100)

        super().__init__(width, height, color)

        self.color = color

        self.center_x = x
        self.center_y = y

        # Движение
        self.change_x = random.uniform(-0.1, 0.1)
        self.change_y = random.uniform(-0.05, 0.05)

        # Вращение
        self.change_angle = random.uniform(-20, 20)

        # Свойства
        self.alpha = 180
        self.lifetime = random.uniform(0.3, 0.5)
        self.time_alive = 0

    def update(self, delta_time):
        # Движение
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Вращение
        self.angle += self.change_angle * delta_time

        # Замедление
        self.change_x *= 0.9
        self.change_y *= 0.9
        self.change_angle *= 0.95

        # Исчезание и уменьшение
        self.alpha = max(0, self.alpha - 3)
        self.scale_x *= 0.98
        self.scale_y *= 0.98

        # Обновляем цвет с новой прозрачностью
        self.color = (20, 20, 20, int(self.alpha))

        # Время жизни
        self.time_alive += delta_time
        if self.time_alive >= self.lifetime or self.alpha <= 10:
            self.remove_from_sprite_lists()


class Direction(enum.Enum):
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3


class PlayerSprite(arcade.Sprite):
    def __init__(self, player_class=None, scale=1.0):
        super().__init__(scale=scale)
        self.player_class = player_class

        self.textures = [arcade.load_texture(f'./assets/images/hum/hum_fd{i}.png') for i in range(1, 4)] + \
                        [arcade.load_texture(f'./assets/images/hum/hum_bw{i}.png') for i in range(1, 4)] + \
                        [arcade.load_texture(f'./assets/images/hum/hum_lt{i}.png') for i in range(1, 4)] + \
                        [arcade.load_texture(f'./assets/images/hum/hum_lt{i}.png').flip_horizontally() for i in
                         range(1, 4)]

        self.texture = self.textures[0]
        self.animation_timer = 0
        self.current_frame = 0
        self.direction = Direction.DOWN
        self.is_going = False

        self.speed = 1

        # Частицы следов
        self.footstep_particles = arcade.SpriteList()
        self.last_step_particle_time = 0
        self.step_particle_interval = 0.15

        self.actual_direction = Direction.DOWN
        self.last_direction = Direction.DOWN

    def update(self, dt: float = 1 / 60, *args, **kwargs) -> None:
        is_moving = (self.change_x != 0 or self.change_y != 0)

        if is_moving:
            move_vector_length = math.sqrt(self.change_x ** 2 + self.change_y ** 2)

            if move_vector_length > 0:
                self.change_x = (self.change_x / move_vector_length) * 1.0
                self.change_y = (self.change_y / move_vector_length) * 1.0

        if is_moving:
            self.is_going = True

            if abs(self.change_x) > abs(self.change_y):
                if self.change_x > 0:
                    self.actual_direction = Direction.RIGHT
                else:
                    self.actual_direction = Direction.LEFT
            else:
                if self.change_y > 0:
                    self.actual_direction = Direction.UP
                else:
                    self.actual_direction = Direction.DOWN

            self.last_direction = self.actual_direction

            if self.animation_timer == 4:
                self.current_frame = 1
            elif self.animation_timer == 8:
                self.current_frame = 2
                self.animation_timer = -1

            self.animation_timer += 1

        else:
            self.is_going = False
            self.animation_timer = 0
            self.current_frame = 0

        direction_index = self.actual_direction.value if is_moving else self.last_direction.value
        base_index = direction_index * 3
        texture_index = base_index + self.current_frame

        self.texture = self.textures[texture_index]

        # Создаем частицы при движении
        if self.is_going:
            self.last_step_particle_time += dt
            if self.last_step_particle_time >= self.step_particle_interval:
                self.create_footstep_particle()
                self.last_step_particle_time = 0

        # Дополнительные частицы при звуке шага
        if self.is_going and self.animation_timer in (8,):
            self.create_footstep_particle()

    def create_footstep_particle(self):
        if not self.is_going:
            return

        # Позиция под ногами
        x = self.center_x + random.uniform(-5, 5)
        y = self.bottom - 1

        for _ in range(random.randint(1, 2)):
            particle = FootstepParticle(x, y)
            self.footstep_particles.append(particle)


class Player:
    def __init__(self, name, lvl, cash, exp):
        from itertools import cycle

        self.name = name
        self.lvl = lvl
        self.cash = cash
        self.exp = exp

        self._inventory = []
        self._gripped_item = None
        self.inds = cycle((1, 0))

        self.has_lighter = False

        self.sanity = None
        self.is_unhittable = False

        self.sprite = None

        self.voice_vol = 0.0
        self.is_voice = True
        self.threshold = 0.2

    @property
    def inventory(self):
        return self._inventory

    @property
    def gripped_item(self):
        return self._gripped_item

    @gripped_item.setter
    def gripped_item(self, new_val):
        self._gripped_item = new_val

    def take_item(self, item):
        if item.id in ('pills',):
            if item.used:
                return

        if item.id == 'incense' and not item.take_item(self):
            return

        if item.id in ('lighter',):
            item.use_item(self)
            return

        if len(self.inventory) == 2:
            return
        if len(self.inventory) == 1:
            vol = SettingsManager.get_sound_volume()
            arcade.play_sound(TAKE_ITEM, volume=vol)
            self.inventory.append(item)
            item.in_inventory = True
            return

        vol = SettingsManager.get_sound_volume()
        arcade.play_sound(TAKE_ITEM, volume=vol)
        self.inventory.append(item)
        self.gripped_item = item
        item.in_inventory = True
        item.is_grabbed = True

    def change_gripped_item(self):
        if len(self.inventory) in (0, 1):
            return

        self.gripped_item.is_grabbed = False
        self.turn_off_item()

        self.gripped_item = self.inventory[next(self.inds)]
        self.gripped_item.is_grabbed = True

        vol = SettingsManager.get_sound_volume()
        arcade.play_sound(TAKE_ITEM, volume=vol)

    def drop_item(self):
        if self.gripped_item is None:
            return

        if self.gripped_item.id in ('book',):
            self.gripped_item.is_dropped = True
        self.gripped_item.in_inventory = False
        self.gripped_item.is_grabbed = False
        self.turn_off_item()

        self.inventory.remove(self.gripped_item)
        vol = SettingsManager.get_sound_volume(0.55)
        arcade.play_sound(DROP_ITEM, volume=vol)
        try:
            self.gripped_item = self.inventory[0]
            self.gripped_item.is_grabbed = True
        except IndexError:
            self.gripped_item = None

    def put_item(self, item):
        if not self.inventory or item not in self.inventory:
            return False

        item.in_inventory = False
        item.is_grabbed = False
        item.turn_off()

        self.inventory.remove(item)
        vol = SettingsManager.get_sound_volume()
        arcade.play_sound(BOARD_ITEM, volume=vol)
        try:
            self.gripped_item = self.inventory[0]
            self.gripped_item.is_grabbed = True
        except IndexError:
            self.gripped_item = None

        return True

    def turn_on_item(self):
        if not self.gripped_item:
            return

        if self.gripped_item.id in ('pills',):
            self.gripped_item.use_item(self)
            return

        if self.gripped_item.id == 'incense':
            self.gripped_item.use_item(self)
            return

        if self.gripped_item.is_turn_on:
            self.turn_off_item()
            return
        self.gripped_item.turn_on()

    def turn_off_item(self):
        self.gripped_item.turn_off()
