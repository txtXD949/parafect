import math
import arcade


class GhostPhysics:
    def __init__(self, x=0, y=0, speed=1.0, boost=0.07):
        self.x = x
        self.y = y

        self.velocity_x = 0.0
        self.velocity_y = 0.0

        self.acceleration = 0.5
        self.max_speed = 8.0
        self.friction = 0.92

        self.boost = boost
        self.base_speed = speed
        self.boost_multiplier = 1 + boost
        self.current_speed = speed

        self.angle = 0
        self.target_angle = 0
        self.rotation_speed = 0.1

        self.last_dx = 0
        self.last_dy = 0

    def set_boosted(self, boosted):
        if boosted:
            self.current_speed = self.base_speed * self.boost_multiplier
        else:
            self.current_speed = self.base_speed

    def check_wall_collision(self, new_x, new_y, sprite_width, sprite_height, walls):
        """Проверяет столкновение со стенами"""
        if not walls:
            return False

        ghost_rect = arcade.Sprite()
        ghost_rect.width = sprite_width
        ghost_rect.height = sprite_height
        ghost_rect.center_x = new_x
        ghost_rect.center_y = new_y

        for wall in walls:
            if arcade.check_for_collision(ghost_rect, wall):
                return True
        return False

    def update(self, target_x, target_y, dt, walls=None, sprite_width=50, sprite_height=50):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > 10:
            dx /= dist
            dy /= dist

        self.last_dx = self.last_dx * 0.7 + dx * 0.3
        self.last_dy = self.last_dy * 0.7 + dy * 0.3

        if abs(self.last_dx) > 0.001 or abs(self.last_dy) > 0.001:
            self.target_angle = math.atan2(self.last_dy, self.last_dx)

        angle_diff = self.target_angle - self.angle
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi

        self.angle += angle_diff * self.rotation_speed

        move_x = math.cos(self.angle) * self.acceleration * self.current_speed
        move_y = math.sin(self.angle) * self.acceleration * self.current_speed

        self.velocity_x += move_x
        self.velocity_y += move_y

        self.velocity_x *= self.friction
        self.velocity_y *= self.friction

        speed = math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.velocity_x *= scale
            self.velocity_y *= scale

        new_x = self.x + self.velocity_x
        new_y = self.y + self.velocity_y

        if walls and self.check_wall_collision(new_x, new_y, sprite_width, sprite_height, walls):
            self.velocity_x *= -0.5
            self.velocity_y *= -0.5
            return self.x, self.y, self.angle

        self.x = new_x
        self.y = new_y

        return self.x, self.y, self.angle