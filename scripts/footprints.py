import arcade
import random
import math


class Footprint(arcade.Sprite):
    TEXTURES = [
        f'./assets/images/footprints/fp_{i}.png' for i in range(7)
    ]

    def __init__(self, x, y, lifetime=25.0, scale=0.6):
        path = random.choice(self.TEXTURES)
        super().__init__(path, scale=scale)

        self.center_x = x
        self.center_y = y
        self.angle = random.uniform(0, 360)

        # Время жизни
        self.lifetime = lifetime
        self.time_alive = 0

        self.alpha = 80

    def update(self, delta_time):
        self.time_alive += delta_time

        # Исчезание в последние 5 секунд
        if self.lifetime - self.time_alive < 5.0:
            remaining = self.lifetime - self.time_alive
            if remaining <= 0:
                self.remove_from_sprite_lists()
                return

            # Плавное исчезание
            fade_ratio = remaining / 5.0
            self.alpha = int(80 * fade_ratio)

            # Мерцание
            if random.random() < 0.3:
                self.alpha = max(40, self.alpha - random.randint(10, 30))

        if self.time_alive >= self.lifetime:
            self.remove_from_sprite_lists()
