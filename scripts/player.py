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
