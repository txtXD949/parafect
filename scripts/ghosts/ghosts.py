import random
import math
import arcade

from . import GHOST_EVENTS


class GhostParticle(arcade.SpriteSolidColor):
    """Частицы дыма/тумана для призрака"""

    def __init__(self, x, y, ghost, direction_angle):
        # Размер
        width = random.randint(4, 8)
        height = random.randint(4, 8)

        # Цвет
        if ghost.is_charging:
            color = (100, 100, 255, 150)  # Синий при зарядке
        elif ghost.is_hunt:
            color = (150, 150, 255, 120)  # Голубой при охоте
        else:
            color = (255, 255, 255, 170)  # Светло-синий обычно

        super().__init__(width, height, color)

        self.color = color
        self.ghost = ghost

        self.center_x = x
        self.center_y = y

        # Движение
        speed = random.uniform(0.1, 0.3)
        self.change_x = -math.cos(direction_angle) * speed
        self.change_y = -math.sin(direction_angle) * speed

        self.change_x += random.uniform(-0.05, 0.05)
        self.change_y += random.uniform(-0.05, 0.05)

        # Вращение
        self.change_angle = random.uniform(-10, 10)

        # Свойства
        self.alpha = color[3] if len(color) > 3 else 150
        self.lifetime = random.uniform(0.5, 1.0)
        self.time_alive = 0

    def update(self, delta_time):
        # Движение
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Вращение
        self.angle += self.change_angle * delta_time

        # Замедление
        self.change_x *= 0.92
        self.change_y *= 0.92
        self.change_angle *= 0.9

        # Исчезание и уменьшение
        self.alpha = max(0, self.alpha - 2)
        self.scale_x *= 0.97
        self.scale_y *= 0.97

        # Обновляем цвет с новой прозрачностью
        if len(self.color) == 4:
            self.color = (self.color[0], self.color[1], self.color[2], int(self.alpha))
        else:
            self.color = (self.color[0], self.color[1], self.color[2], int(self.alpha))

        # Время жизни
        self.time_alive += delta_time
        if self.time_alive >= self.lifetime or self.alpha <= 10:
            self.remove_from_sprite_lists()


class GhostSprite(arcade.Sprite):
    TEXTURES = [
        arcade.load_texture('./assets/images/ghost/ghost_0.png'),
        arcade.load_texture('./assets/images/ghost/ghost_1.png')
    ]
    GE_SOUNDS = [

    ]
    HUNT_SOUNDS = [

    ]

    def __init__(self, ghost, scale=1.0):
        super().__init__(scale=scale)
        self.texture = self.TEXTURES[0]
        self.ghost = ghost
        self.visible = False

        # Частицы
        self.particles = arcade.SpriteList()
        self.particle_timer = 0
        self.particle_interval = 0.03
        self.last_direction = 0

    def update(self, dt: float = 1 / 60, *args, **kwargs) -> None:
        if self.ghost.ghost_event and self.ghost.ghost_event.is_ge:
            self.ghost.ghost_event.timer -= dt

        self.last_direction = self.ghost.physics.angle
        if self.visible:
            self.update_particles(dt)

        self.particles.update(dt)

    def update_particles(self, delta_time):
        self.particle_timer += delta_time

        if self.particle_timer >= self.particle_interval:
            for _ in range(random.randint(1, 5)):
                self.create_particle()
            self.particle_timer = 0

    def create_particle(self):
        offset_distance = random.uniform(5, 15)

        x = self.center_x - math.cos(self.last_direction) * offset_distance
        y = self.center_y - math.sin(self.last_direction) * offset_distance

        # Небольшой разброс
        side_offset = random.uniform(-8, 8)
        x += math.cos(self.last_direction + math.pi / 2) * side_offset
        y += math.sin(self.last_direction + math.pi / 2) * side_offset

        particle = GhostParticle(x, y, self.ghost, self.last_direction)
        self.particles.append(particle)


class Ghost:
    def __init__(self, id, name, evidences, desc='', hunt_start=50, hunt_chance=0.02, step_loud='mid',
                 ghost_event_chance=0.00005, drop_sanity=5, speed=0.3, interaction_chance=0.01, blink_chance=0.1,
                 boost=0.07, spec=''):
        self._id = id
        self._name = name
        self._description = desc
        self._hunt_start = hunt_start
        self._hunt_chance = hunt_chance
        self._step_loud = step_loud
        self._ghost_event_chance = ghost_event_chance
        self._drop_sanity = drop_sanity
        self._interaction_chance = interaction_chance
        self._blink_chance = blink_chance
        self.speed = speed
        self.boost = boost
        self._evidences = evidences[:]
        self._species = spec

        self.sprite = GhostSprite(self, 1.0)

        # Физика
        from . import GhostPhysics
        self.physics = GhostPhysics(speed=self.speed, boost=self.boost)

        # Охота
        self.detection_radius = 170.0
        self.last_seen_player = None

        self.is_hunt = False
        self.hunt_timer = 0
        self.stop_timer = 0
        self.hunt_state: 'chase' or 'seek' or None = None

        # Таймер зарядки перед охотой
        self.charge_timer = 0
        self.is_charging = False

        # Для блуждания
        self.wander_target = None
        self.wander_timer = 0
        self.wander_cooldown = 0

        # Для мерцания
        self.blink_timer = 0
        self.blink_interval = 0.02
        self.blink_duration = 0.2
        self.is_blinking = False
        self.original_visible = True

        # Гост ивент
        self.ghost_event = None
        self.is_ge = False
        self.ge_timer = 0

        self.sound_player_g = None
        self.sound_player_h = None

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def hunt_start(self):
        return self._hunt_start

    @property
    def hunt_chance(self):
        return self._hunt_chance

    @property
    def step_loud(self):
        return self._step_loud

    @property
    def ghost_event_chance(self):
        return self._ghost_event_chance

    @ghost_event_chance.setter
    def ghost_event_chance(self, val):
        self._ghost_event_chance = val

    @property
    def drop_sanity(self):
        return self._drop_sanity

    @property
    def interaction_chance(self):
        return self._interaction_chance

    @property
    def blink_chance(self):
        return self._blink_chance

    @property
    def evidences(self):
        return self._evidences

    @property
    def species(self):
        return self._species

    def start_hunt(self):
        if self.game.dif_id == 'peaceful':
            return

        if self.is_hunt or self.ghost_event.is_ge or self.stop_timer:
            return

        self.is_charging = True
        self.charge_timer = random.uniform(1.5, 2.0)
        self.sprite.visible = True

        if hasattr(self, 'hunt_initialized'):
            del self.hunt_initialized

    def end_hunt(self):
        self.is_hunt = False
        self.is_charging = False
        self.hunt_timer = 0
        self.stop_timer = 0
        self.hunt_state = None
        self.sprite.visible = False
        self.is_blinking = False
        self.blink_timer = 0
        self.sprite.angle = 0

    def update_hunt(self, dt, player_x, player_y, player_in_closet, walls_layer=None):
        if self.is_charging:
            self.charge_timer -= dt
            if self.charge_timer <= 0:
                self.is_charging = False
                self.is_hunt = True
                self.hunt_timer = 25 + random.uniform(-5.5, 5.5)
                self.hunt_state = 'seek'

                self.update_blinking(dt)

            return

        if not self.is_hunt:
            return

        self.hunt_timer -= dt
        if self.hunt_timer <= 0:
            self.end_hunt()
            return

        self.update_blinking(dt)

        sees_player = False

        if player_in_closet:
            target_x, target_y = self.get_wander_target(dt)
        else:
            dx = player_x - self.physics.x
            dy = player_y - self.physics.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < self.detection_radius:
                target_x, target_y = player_x, player_y
                self.last_seen_player = (player_x, player_y)
                self.wander_target = None
                sees_player = True
            elif self.last_seen_player:
                target_x, target_y = self.last_seen_player
                dist_to_last = math.sqrt((target_x - self.physics.x) ** 2 + (target_y - self.physics.y) ** 2)

                if dist_to_last < 50:
                    self.last_seen_player = None
            else:
                target_x, target_y = self.get_wander_target(dt)

        self.physics.set_boosted(sees_player)

        x, y, angle = self.physics.update(
            target_x,
            target_y,
            dt,
            walls=walls_layer,
            sprite_width=self.sprite.width,
            sprite_height=self.sprite.height
        )

        self.sprite.center_x = x
        self.sprite.center_y = y
        self.sprite.angle = math.degrees(angle)

        return x, y

    def get_wander_target(self, dt):
        if not hasattr(self, 'wander_cooldown'):
            self.wander_cooldown = 0
            self.wander_target = None

        self.wander_cooldown -= dt

        if self.wander_target is None or self.wander_cooldown <= 0:
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(200, 400)

            new_x = self.physics.x + math.cos(angle) * distance
            new_y = self.physics.y + math.sin(angle) * distance

            self.wander_target = (new_x, new_y)
            self.wander_cooldown = random.uniform(0.2, 0.5)

        return self.wander_target

    def do_ghost_event(self, player_x, player_y):
        if self.is_hunt:
            return
        if not self.ghost_event:
            self.ghost_event = random.choice(GHOST_EVENTS)(self)
        self.ghost_event.do_ghost_event(player_x, player_y)

    def update_blinking(self, dt):
        if not self.is_hunt:
            return

        self.blink_timer += dt

        if self.is_blinking:
            if self.blink_timer >= self.blink_duration:
                self.sprite.visible = self.original_visible
                self.is_blinking = False
                self.blink_timer = 0
        else:
            if self.blink_timer >= self.blink_interval:
                if random.random() < self._blink_chance:
                    self.original_visible = self.sprite.visible
                    self.sprite.visible = False
                    self.is_blinking = True
                    self.blink_timer = 0
                else:
                    self.blink_timer = 0

    def __str__(self):
        return self.name


class Spirit(Ghost):
    def __init__(self):
        super().__init__('spirit', 'Дух', evidences=['emf5', 'hot_temp', 'dict'])


class Demon(Ghost):
    def __init__(self):
        super().__init__('demon', 'Демон', evidences=['cold_temp', 'mic', 'book'], hunt_start=75, hunt_chance=0.05)


class Phantom(Ghost):
    def __init__(self):
        super().__init__('phantom', 'Фантом', evidences=['book', 'dict', 'uf'], blink_chance=0.5,
                         spec='редко мерцает(почти невидимый), умеет телепортироваться по карте')
        self.blink_interval = 0.1
        self.blink_duration = 0.6


class Oni(Ghost):
    def __init__(self):
        super().__init__('oni', 'Они', evidences=['emf5', 'hot_temp', 'book'], hunt_chance=0.04,
                         ghost_event_chance=0.0001, drop_sanity=10, blink_chance=0.02,
                         spec='много гост-ивентов, есть шанс что гост ивент снимет 20% рассудка')

        self.blink_interval = 0.3
        self.blink_duration = 0.2


class Banshee(Ghost):
    def __init__(self):
        super().__init__('banshee', 'Банши', evidences=['uf', 'book', 'mic'],
                         spec='умеет ходить к игроку, есть шанс услышать особый крик банши на микрофоне, снимает 10% рассудка')


class Reverent(Ghost):
    def __init__(self):
        super().__init__('reverent', 'Ревенант', evidences=['cold_temp', 'dict', 'book'], speed=0.05, boost=10.0,
                         spec='при виде игрока очень быстро ускоряется')


class Muling(Ghost):
    def __init__(self):
        super().__init__('muling', 'Мюллинг', evidences=['hot_temp', 'mic', 'uf'], step_loud='low',
                         spec='лучше реагирует на войс-чат')


class Poltergeist(Ghost):
    def __init__(self):
        super().__init__('poltergeist', 'Полтергейст', evidences=['emf5', 'mic', 'hot_temp'], interaction_chance=0.05,
                         spec='сильнее бросается предметами')


class Siren(Ghost):
    def __init__(self):
        super().__init__('siren', 'Сирена', evidences=['dict', 'cold_temp', 'uf'],
                         spec='в диктофоне можно услышать пение снимает 10% рассудка')


class Shade(Ghost):
    def __init__(self):
        super().__init__('shade', 'Тень', evidences=['cold_temp', 'mic', 'emf5'], hunt_start=35,
                         interaction_chance=0.005, ghost_event_chance=0.00002, spec='спокойный призрак')


class Butcher(Ghost):
    def __init__(self):
        super().__init__('butcher', 'Мясник', evidences=['hot_temp', 'dict', 'book'], step_loud='high', speed=0.1,
                         boost=0.1, spec='хуже реагирует на войс-чат. Противоположность Мюллингу')


class Wrath(Ghost):
    def __init__(self):
        super().__init__('wrath', 'Мираж', evidences=['emf5', 'uf', 'book'], hunt_start=60, drop_sanity=10,
                         spec='умеет телепортироваться к игроку')


class Mimic(Ghost):
    GHOSTS = [
        Spirit, Demon, Phantom,
        Oni, Banshee, Reverent,
        Muling, Poltergeist, Siren,
        Wrath, Shade, Butcher
    ]

    def __init__(self):
        self.copied_ghost = None

        self.change_ghost()

        super().__init__('mimic', 'Мимик', spec='копирует другого призрака', evidences=['uf', 'cold_temp', 'mic'],
                         hunt_start=self.copied_ghost.hunt_start, hunt_chance=self.copied_ghost.hunt_chance,
                         step_loud=self.copied_ghost.step_loud, drop_sanity=self.copied_ghost.drop_sanity,
                         speed=self.copied_ghost.speed, interaction_chance=self.copied_ghost.interaction_chance,
                         blink_chance=self.copied_ghost.blink_chance, boost=self.copied_ghost.boost)

        self.change_chance = 0.7

    def change_ghost(self):
        self.copied_ghost = random.choice(self.GHOSTS[:-1])()
        return self.copied_ghost

    def start_hunt(self):
        super().start_hunt()
        self.change_ghost()


GHOSTS = [
    Spirit, Demon, Phantom,
    Oni, Banshee, Reverent,
    Muling, Poltergeist, Mimic,
    Wrath, Shade, Butcher, Siren
]
