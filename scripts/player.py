import arcade
import enum


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

        self.actual_direction = Direction.DOWN
        self.last_direction = Direction.DOWN

    def update(self, dt: float = 1 / 60, *args, **kwargs) -> None:
        is_moving = (self.change_x != 0 or self.change_y != 0)

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


class Player:
    def __init__(self):
        from itertools import cycle

        self._inventory = []
        self._gripped_item = None
        self.inds = cycle((1, 0))

        self.has_lighter = False

        self.sanity = 3
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
            self.inventory.append(item)
            item.in_inventory = True
            return

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

    def drop_item(self):
        if self.gripped_item is None:
            return

        if self.gripped_item.id in ('book',):
            self.gripped_item.is_dropped = True
        self.gripped_item.in_inventory = False
        self.gripped_item.is_grabbed = False
        self.turn_off_item()

        self.inventory.remove(self.gripped_item)
        try:
            self.gripped_item = self.inventory[0]
            self.gripped_item.is_grabbed = True
        except IndexError:
            self.gripped_item = None

    def put_item(self, item):
        if not self.inventory:
            return

        item.in_inventory = False
        item.is_grabbed = False
        item.turn_off()

        self.inventory.remove(item)
        try:
            self.gripped_item = self.inventory[0]
            self.gripped_item.is_grabbed = True
        except IndexError:
            self.gripped_item = None

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
