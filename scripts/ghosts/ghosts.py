import random
import arcade

from . import GHOST_EVENTS


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

        # Гост ивент
        self.ghost_event = None
        self.ge_chance = self.ghost.ghost_event_chance
        self.is_ge = False
        self.drop_san = self.ghost.drop_sanity
        self.ge_timer = 0

        self.visible = False

    def do_ghost_event(self, player_x, player_y):
        if not self.ghost_event:
            self.ghost_event = random.choice(GHOST_EVENTS)(self.ghost)
        self.ghost_event.do_ghost_event(player_x, player_y)

    def update(self, dt: float = 1 / 60, *args, **kwargs) -> None:
        if self.ghost_event and self.ghost_event.is_ge:
            self.ghost_event.timer -= dt


class Ghost:
    def __init__(self, id, name, evidences, desc='', hunt_start=50, hunt_chance=0.02, step_loud='mid',
                 ghost_event_chance=0.00005, drop_sanity=5, speed=1.0, interaction_chance=0.01, blink_chance=0.1,
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
        self._speed = speed
        self._boost = boost
        self._evidences = evidences[:]
        self._species = spec

        self.sprite = GhostSprite(self, 1.0)

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
    def speed(self):
        return self._speed

    @property
    def boost(self):
        return self._boost

    @property
    def evidences(self):
        return self._evidences

    @property
    def species(self):
        return self._species

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
        super().__init__('phantom', 'Фантом', evidences=['book', 'dict', 'uf'], blink_chance=0.05,
                         spec='редко мерцает(почти невидимый), умеет телепортироваться по карте')


class Oni(Ghost):
    def __init__(self):
        super().__init__('oni', 'Они', evidences=['emf5', 'hot_temp', 'book'], hunt_chance=0.04,
                         ghost_event_chance=0.0001, drop_sanity=10,
                         spec='много гост-ивентов, есть шанс что гост ивент снимет 20% рассудка')


class Banshee(Ghost):
    def __init__(self):
        super().__init__('banshee', 'Банши', evidences=['uf', 'book', 'mic'],
                         spec='умеет ходить к игроку, есть шанс услышать особый крик банши на микрофоне, снимает 10% рассудка')


class Reverent(Ghost):
    def __init__(self):
        super().__init__('reverent', 'Ревенант', evidences=['cold_temp', 'dict', 'book'], speed=0.3, boost=1,
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
        super().__init__('butcher', 'Мясник', evidences=['hot_temp', 'dict', 'book'], step_loud='high', speed=0.6,
                         spec='хуже реагирует на войс-чат. Противоположность Мюллингу')


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
        self.copied_ghost = random.choice(self.GHOSTS[:-1])
        return self.copied_ghost


GHOSTS = [
    Spirit, Demon, Phantom,
    Oni, Banshee, Reverent,
    Muling, Poltergeist, Mimic,
    Wrath, Shade, Butcher, Siren
]
