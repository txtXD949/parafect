from arcade.future.light import LightLayer, Light

from .. import Game
from ..views import SettingsManager
from ..sounds import *

import arcade
from arcade.gui import UIManager
from math import atan, degrees
from random import choice, randint
import random
import math

SPEED = 1


class Kv96(arcade.View):
    def __init__(self, game):
        super().__init__()

        self.game = game

        self.pressed_E = False

        self.is_under_roof = False

        self.is_under_roof_tent = False

        self.time_blinking = 0

        self.evidences = self.game.evidences
        print(self.evidences, self.game.ghost)

        self.setup()

    def setup(self):
        # Микрофон (игрока)
        from .. import MicManager
        self.mic_manager = MicManager()
        self.mic_manager.start()

        # Карта
        self.tile_map = arcade.load_tilemap('././assets/maps/hrush.tmx', scaling=1.0)

        # Расчет размеров карты с учетом масштаба
        self.map_width = self.tile_map.width * self.tile_map.tile_width
        self.map_height = self.tile_map.height * self.tile_map.tile_height

        # Сцена
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Игрок
        from .. import PlayerSprite, Player
        self.player = self.game.player
        self.player.sanity = self.game.sanity
        self.player_sprite = PlayerSprite(scale=0.45)

        self.player_sprite.hit_box = arcade.hitbox.RotatableHitBox([(-1, -14), (1, -14), (1, 0), (-1, 0)])

        self.player_sprite.position = self.scene["spawn"][0].position

        self.player.sprite = self.player_sprite

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        # Физ.движок
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.scene['collitions'])

        # Предметы
        self.items_sprite_list = arcade.SpriteList()
        self.free_items_sprite_list = arcade.SpriteList()
        self.items_list = []

        # Система отпечатков
        self.footprints_list = arcade.SpriteList()
        self.footprint_timer = 0
        self.footprint_interval = 1.0

        # Комнаты
        self.rooms = [
            "corridor",
            "toilet1",
            "toilet2",
            "toilet3",
            "kitchen1",
            "kitchen2",
            "kitchen3",
            "room1",
            "room2",
            "room3",
            "room4",
            "wardroom1",
            "wardroom2",
            "wardroom3"
        ]

        # Призрак
        self.ghost = self.game.ghost
        self.ghost.game = self.game
        self.ghost_sprite_list = arcade.SpriteList()
        self.ghost.sprite.scale = 0.7
        self.ghost_sprite_list.append(self.ghost.sprite)
        choice_ = choice(self.rooms)
        self.ghost.room = self.scene[choice_]
        print(choice_)

        self.spawn_ghost_in_room()

        # Устанавливаем начальную позицию призрака
        self.ghost.physics.x = random.uniform(30, self.map_width - 30)
        self.ghost.physics.y = random.uniform(250, self.map_height - 30)
        self.ghost.sprite.center_x = self.ghost.physics.x
        self.ghost.sprite.center_y = self.ghost.physics.y

        # Сцены
        from ..views import ToolBoard
        self.tool_board = ToolBoard(self.game.inv, self, self.player, bias_scale=0.7)
        self.tool_board_use = False

        from ..views import Paper
        self.paper = Paper(800, 600, 0.9, 1.4)

        self.manager = UIManager()
        self.manager.enable()
        self.manager.add(self.paper)

        from ..views import SanityScreen
        self.sanity_screen = SanityScreen(self.player, self, self.game)
        self.sanity_screen_use = False

        # Камера
        self.world_camera = arcade.Camera2D()
        self.world_camera.zoom = 1.0

        self.world_camera.projection = arcade.rect.XYWH(
            0, 0,
            16 * 12,
            9 * 12
        )

        self.world_camera.viewport_width = self.width
        self.world_camera.viewport_height = self.height

        self.world_camera.position = (
            self.map_width / 2,
            self.map_height / 2
        )

        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.world_camera.view_data,
            max_amplitude=5.0,
            acceleration_duration=1.0,
            falloff_time=0.5,
            shake_frequency=8.0
        )

        # Двери
        from ..door import DoorSprite
        self.doors_list = arcade.SpriteList()
        for door in self.scene["doors"]:
            door_sprite = DoorSprite(door.position, self.scene["collitions"], door.texture)
            self.doors_list.append(door_sprite)

        # Шкафы
        from ..closet import ClosetSprite
        self.closets_list = arcade.SpriteList()
        for closet in self.scene["closets"]:
            closet_sprite = ClosetSprite(closet.position, closet.texture)
            self.closets_list.append(closet_sprite)

            clone_for_hitbox = arcade.Sprite(closet.texture, scale=0.8)
            clone_for_hitbox.position = closet.position
            self.scene["collitions"].append(clone_for_hitbox)

        # Генератор
        generator = self.scene["generator"][0]
        clone_for_hitbox = arcade.Sprite(generator.texture, scale=0.8)
        clone_for_hitbox.position = generator.position
        self.scene["collitions"].append(clone_for_hitbox)

        # Виньетка
        self.scene["dark"].alpha_normalized = 0

        self.vignette_list = arcade.SpriteList()
        self.vignette = arcade.Sprite()
        self.vignette1_texture = arcade.load_texture("././assets/images/vignettes/vignette1.png")
        self.vignette_flashlight_texture = arcade.load_texture("././assets/images/vignettes/vignette_flashlight.png")
        self.vignette_uf_texture = arcade.load_texture("././assets/images/vignettes/vignette_uf.png")
        self.vignette.texture = self.vignette1_texture
        self.vignette_list.append(self.vignette)

        # Свет
        self.is_lightning = False
        self.threshold_max = 220
        self.threshold_min = 0
        self.threshold = self.threshold_max

        # Рассудок
        self.sanity_timer = 5 * 60

        self.gui_camera = arcade.Camera2D()

    def spawn_ghost_in_room(self):
        ghost_room = self.ghost.room[0]

        if ghost_room:
            padding = 20
            x = random.uniform(ghost_room.left + padding, ghost_room.right - padding)
            y = random.uniform(ghost_room.bottom + padding, ghost_room.top - padding)
        else:
            x = random.uniform(100, self.map_width - 100)
            y = random.uniform(100, self.map_height - 100)

        self.ghost.physics.x = x
        self.ghost.physics.y = y
        self.ghost.sprite.center_x = x
        self.ghost.sprite.center_y = y

    def get_voice_level(self):
        return min(5, max(1, int(self.mic_manager.voice_volume * 5)))

    def draw_voice_level(self):
        colors = [
            arcade.color.YELLOW,
            arcade.color.DARK_YELLOW
        ]

        from main import GameWindow
        lvl = self.get_voice_level()

        for i in range(1, 6):
            color = colors[1 if lvl < i else 0]
            arcade.draw_line(40 * i, 10, 40 * i, 100, color=color, line_width=4)

    def on_draw(self) -> bool | None:
        self.clear()

        self.camera_shake.update_camera()
        self.world_camera.use()

        self.scene["ground"].draw(pixelated=True)
        self.scene["floor"].draw(pixelated=True)
        self.scene["carpet"].draw(pixelated=True)
        self.scene["walls"].draw(pixelated=True)
        self.doors_list.draw(pixelated=True)
        self.closets_list.draw(pixelated=True)
        self.scene["furniture_back"].draw(pixelated=True)
        self.scene["generator"].draw(pixelated=True)
        self.ghost.sprite.particles.draw(pixelated=True)
        self.player_sprite.footstep_particles.draw(pixelated=True)
        self.ghost_sprite_list.draw(pixelated=True)
        self.player_list.draw(pixelated=True)
        if self.player_sprite.visible:
            self.items_sprite_list.draw(pixelated=True)
        else:
            self.free_items_sprite_list.draw(pixelated=True)
        self.scene["furniture_front"].draw(pixelated=True)

        self.footprints_list.draw(pixelated=True)

        for item in self.items_list:
            if item.id == 'incense':
                item.smoke_particles.draw(pixelated=True)

        self.camera_shake.readjust_camera()

        self.scene["roof"].draw(pixelated=True)
        self.scene["roof_tent"].draw(pixelated=True)
        self.scene["dark"].draw(pixelated=True)
        self.vignette_list.draw(pixelated=True)

        self.gui_camera.use()
        self.draw_voice_level()

        self.manager.draw(pixelated=True)

    def on_update(self, delta_time: float) -> bool | None:
        self.mic_manager.update(delta_time)

        self.player_sprite.update()
        self.player_sprite.footstep_particles.update(delta_time)

        # Обновляем отпечатки
        self.footprints_list.update(delta_time)
        self.check_footprint_spawning(delta_time)

        from ..ghosts import Muling, Banshee, Siren

        self.physics_engine.update()
        self.camera_shake.update(delta_time)

        pos = (
            self.player_sprite.center_x,
            self.player_sprite.center_y
        )
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            pos,
            0.5
        )

        if arcade.check_for_collision_with_list(self.player_sprite, self.scene['roof']):

            # Пытаемся сменить комнату призрака
            self.ghost.try_change_room(self.scene, self.rooms, delta_time)

            self.ghost_sprite_list.update(delta_time)
            self.ghost.do_ghost_event(self.player_sprite.center_x, self.player_sprite.center_y)

            self.ghost.start_hunt(delta_time)

            if self.ghost.is_charging:
                self.close_main_door()

            if self.ghost.is_hunt or self.ghost.is_charging:
                self.game.was_hunt = True

                if not hasattr(self.ghost, 'hunt_initialized'):
                    self.ghost.hunt_initialized = True
                    self.spawn_ghost_in_room()

                player_in_closet = not self.player_sprite.visible
                # Данные об игроке
                voice_level = self.get_voice_level()  # 1-5
                is_mic_on = voice_level > 0

                # Проверка электронных предметов
                is_using_electronic = False
                for item in self.player.inventory:
                    if item.id in ('emf', 'mic', 'dict', 'flash-light', 'low_light'):
                        if item.is_turn_on:
                            is_using_electronic = True
                            break

                walls_layer = self.scene['ghost_wall']

                self.ghost.update_hunt(
                    delta_time,
                    self.player_sprite.center_x,
                    self.player_sprite.center_y,
                    player_in_closet,
                    walls_layer,
                    voice_level=voice_level,
                    is_mic_on=is_mic_on,
                    is_using_electronic=is_using_electronic
                )

                if self.ghost.is_hunt and not self.ghost.is_charging:
                    if not player_in_closet and not self.player.is_unhittable:
                        if arcade.check_for_collision(self.player_sprite, self.ghost.sprite):
                            self.player_die()

                if self.ghost.is_hunt and not self.ghost.is_charging:
                    self.check_closet_breaking(delta_time)

            if not (self.ghost.is_hunt or self.ghost.is_charging):
                self.open_main_door()

        if self.player.sanity == 0:
            self.game.was_zero_sanity = True

        if arcade.check_for_collision_with_list(self.player_sprite, self.scene['tool_board']):
            if not self.tool_board_use:
                self.open_tool_board()
            self.tool_board_use = True
        else:
            self.tool_board_use = False

        if arcade.check_for_collision_with_list(self.player_sprite, self.scene['sanity']):
            if not self.sanity_screen_use:
                self.open_sanity_screen()
            self.sanity_screen_use = True
        else:
            self.sanity_screen_use = False

        for item in self.items_sprite_list:
            if item._class.id == 'incense' and item._class.is_burning:
                if item._class.check_ghost_collision(self.ghost.sprite):
                    item._class.apply_slow_to_ghost(self.ghost)

            item._class.update_item(self.player_sprite)
            if arcade.check_for_collision_with_list(item, self.ghost.room):
                item._class.in_room = True
            else:
                item._class.in_room = False

        is_hunt_active = self.ghost.is_hunt or self.ghost.is_charging

        # Сбои
        for item in self.items_list:
            if hasattr(item, 'update_malfunction'):
                item.update_malfunction(is_hunt_active, delta_time)

        for item in self.player.inventory:
            if hasattr(item, 'update_malfunction'):
                item.update_malfunction(is_hunt_active, delta_time)

        for item in self.items_list:
            if item.id in ('emf', 'book', 'term'):
                item.use_item(self.evidences)
            elif item.id in ('mic',):
                item.use_item(self.evidences, Muling(), [])
            elif item.id in ('incense',):
                item.update_item(self.player_sprite)
            elif item.id in ('dict',):
                item.use_item(self.player_sprite, ghost=self.game.ghost, evidences=self.evidences)
                if item.is_turn_on:
                    item.update_voice_detection(self.player)

        item_grab = arcade.check_for_collision_with_list(self.player_sprite, self.items_sprite_list)
        for item in item_grab:
            if self.pressed_E and not (any(item._class is it for it in self.player.inventory)):
                self.player.take_item(item._class)

        # Обновление списка предметов, не используемых игроком
        self.free_items_sprite_list.clear()
        for item in self.items_sprite_list:
            if item._class not in self.player.inventory and item not in self.free_items_sprite_list:
                self.free_items_sprite_list.append(item)

        # Двери
        if self.pressed_E and (doors := arcade.check_for_collision_with_list(self.player_sprite, self.doors_list)):
            doors[0].change()
            volume = SettingsManager.get_sound_volume()
            arcade.play_sound(DOOR_OPEN, volume=volume)

        # Шкафы
        if self.pressed_E and (closets := arcade.check_for_collision_with_list(self.player_sprite, self.closets_list)):
            closets[0].interact(self.player_sprite, self.items_list)
            volume = SettingsManager.get_sound_volume()
            arcade.play_sound(CLOSET, volume=volume)

        # Генератор
        if self.pressed_E and (arcade.check_for_collision_with_list(self.player_sprite, self.scene["generator"])):
            self.is_lightning = not self.is_lightning
            if self.threshold == self.threshold_max:
                self.threshold = self.threshold_min
            else:
                self.threshold = self.threshold_max
            volume = SettingsManager.get_sound_volume()
            arcade.play_sound(GENERATOR, volume=volume)

        # Выход из игры
        if arcade.check_for_collision_with_list(self.player_sprite, self.scene["exit"]):
            self.end_game()

        self.pressed_E = False

        # Рендер крыши
        if arcade.check_for_collision_with_list(self.player_sprite, self.scene["roof"]):
            self.is_under_roof = True
        else:
            self.is_under_roof = False
        self.smooth_roof()

        # Рендер крыши
        if arcade.check_for_collision_with_list(self.player_sprite, self.scene["roof_tent"]):
            self.is_under_roof_tent = True
        else:
            self.is_under_roof_tent = False
        self.smooth_roof_tent()

        # Рендер тьмы
        self.smooth_house_dark()

        # Виньетка
        self.vignette.position = self.player_sprite.position

        # Фонарик
        gripped_item = self.player._gripped_item
        if gripped_item is not None and gripped_item.is_turn_on:
            if gripped_item.id == "flash-light":
                self.vignette.texture = self.vignette_flashlight_texture
            elif gripped_item.id == "low_light":
                self.vignette.texture = self.vignette_uf_texture
        else:
            self.vignette.texture = self.vignette1_texture

        # Звук шагов
        if self.player_sprite.is_going:
            if self.player_sprite.animation_timer in (8,):
                if arcade.check_for_collision_with_list(self.player_sprite, self.scene['carpet']):
                    if self.player_sprite.bottom >= 16 * 3:
                        volume = SettingsManager.get_sound_volume()
                        arcade.play_sound(CARPET_FOOTSTEPS, volume=volume)
                    else:
                        volume = SettingsManager.get_sound_volume()
                        arcade.play_sound(GROUND_FOOTSTEPS, volume=volume)

                elif arcade.check_for_collision_with_list(self.player_sprite, self.scene['floor']):
                    volume = SettingsManager.get_sound_volume()
                    arcade.play_sound(GROUND_FOOTSTEPS, volume=volume)

                elif arcade.check_for_collision_with_list(self.player_sprite, self.scene['ground']):
                    volume = SettingsManager.get_sound_volume()
                    arcade.play_sound(GRASS_FOOTSTEPS, volume=volume)

        # Шум света
        if self.is_under_roof and self.is_lightning:
            volume = SettingsManager.get_sound_volume()
            arcade.play_sound(LIGHTNING_NOISE, volume=volume)

        # Моргание света
        if self.time_blinking > 0 and self.is_lightning:
            self.time_blinking -= 1
            if self.time_blinking % 60 == 0:
                is_blink = randint(0, 1)
                if is_blink:
                    sound = choice(
                        [LIGHTNING_BLINK_1, LIGHTNING_BLINK_2, LIGHTNING_BLINK_3])
                    volume = SettingsManager.get_sound_volume()
                    arcade.play_sound(sound, volume=volume)
                self.scene["dark"].alpha = self.threshold_max * is_blink

        # Падение рассудка
        if self.sanity_timer > 0 and self.is_under_roof and not self.is_lightning:
            self.sanity_timer -= 1
        if self.sanity_timer == 0:
            self.sanity_timer = 5 * 60
            self.player.sanity = max(0, self.player.sanity - 1)

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        self.player_sprite.is_going = True

        if symbol == arcade.key.UP:
            self.player_sprite.change_y = SPEED * self.player_sprite.speed

        if symbol == arcade.key.DOWN:
            self.player_sprite.change_y = -SPEED * self.player_sprite.speed

        if symbol == arcade.key.LEFT:
            self.player_sprite.change_x = -SPEED * self.player_sprite.speed

        if symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = SPEED * self.player_sprite.speed

        if symbol == arcade.key.E:
            self.pressed_E = True

        if symbol == arcade.key.G:
            self.player.drop_item()

        if symbol == arcade.key.R:
            self.player.turn_on_item()

        if symbol == arcade.key.J:
            self.open_paper()

        if symbol == arcade.key.F10:
            self.open_settings()

    def on_key_release(self, symbol: int, modifiers: int) -> bool | None:
        if symbol in (arcade.key.UP, arcade.key.DOWN):
            self.player_sprite.change_y = 0
        if symbol in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player_sprite.change_x = 0

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int) -> bool | None:
        self.player.change_gripped_item()

    def open_tool_board(self):
        self.player_sprite.change_x = self.player_sprite.change_y = 0
        self.window.show_view(self.tool_board)

    def open_sanity_screen(self):
        self.player_sprite.change_x = self.player_sprite.change_y = 0
        self.window.show_view(self.sanity_screen)

    def open_paper(self, end=False):
        if end:
            self.manager.remove(self.paper)
            self.paper.visible = False
            self.manager.disable()
            return
        if self.paper.visible:
            self.manager.remove(self.paper)
            self.paper.visible = False
            self.manager.disable()
            volume = SettingsManager.get_sound_volume()
            arcade.play_sound(CLOSE_PAPER, volume=volume)
            return
        self.manager.enable()
        self.manager.add(self.paper)
        self.paper.visible = True
        volume = SettingsManager.get_sound_volume()
        arcade.play_sound(OPEN_PAPER, volume=volume)

    def set_end_flags(self):
        selected_ghosts = self.paper.get_circled_ghosts()
        print(*map(lambda x: x.id, selected_ghosts), ' - ', self.game.ghost.id)
        if self.game.was_death:
            self.game.is_win = False
            return

        if not selected_ghosts:
            self.game.is_win = False
            return
        if len(selected_ghosts) != 1 or selected_ghosts[0].id != self.game.ghost.id:
            self.game.is_win = False
            return

        self.game.is_win = True

    def end_game(self):
        self.set_end_flags()

        self.open_paper(end=True)

        from ..views import ResultsView
        res = ResultsView(self.game)
        self.window.show_view(res)

    def player_die(self):
        self.game.was_death = True
        self.end_game()

    def smooth_roof(self):
        if self.is_under_roof:
            if self.scene["roof"].alpha_normalized >= 0:
                self.scene["roof"].alpha_normalized -= 0.05
        else:
            if self.scene["roof"].alpha_normalized <= 1:
                self.scene["roof"].alpha_normalized += 0.05

    def smooth_roof_tent(self):
        if self.is_under_roof_tent:
            if self.scene["roof_tent"].alpha_normalized >= 0:
                self.scene["roof_tent"].alpha_normalized -= 0.05
        else:
            if self.scene["roof_tent"].alpha_normalized <= 1:
                self.scene["roof_tent"].alpha_normalized += 0.05

    def smooth_house_dark(self):
        if self.is_under_roof:
            if self.scene["dark"].alpha == self.threshold:
                pass
            elif self.scene["dark"].alpha > self.threshold:
                self.scene["dark"].alpha -= 5
            elif self.scene["dark"].alpha < self.threshold:
                self.scene["dark"].alpha += 5
        else:
            if self.scene["dark"].alpha >= 0:
                self.scene["dark"].alpha -= 5

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> bool | None:
        width, height = arcade.get_display_size()
        x0 = x - width // 2 + 0.001
        y0 = y - height // 2 + 0.001

        if x0 >= 0:
            deg = degrees(atan(y0 / x0))
        else:
            deg = degrees(atan(y0 / x0)) + 180

        deg = (-deg + 90) % 360
        self.vignette.angle = deg

    def block_door(self):
        door = arcade.get_sprites_at_point(self.scene["main_door"][0].position, self.doors_list)[0]
        door.block()

    def unblock_door(self):
        door = arcade.get_sprites_at_point(self.scene["main_door"][0].position, self.doors_list)[0]
        door.unblock()

    def do_light_blinking(self, time_blinking):
        self.time_blinking = time_blinking * 60

    def close_main_door(self):
        door = arcade.get_sprites_at_point(
            self.scene["main_door"][0].position,
            self.doors_list
        )[0]

        if not door.closed:
            door.change()
            volume = SettingsManager.get_sound_volume()
            arcade.play_sound(DOOR_OPEN, volume=volume)

        door.block()

    def open_main_door(self):
        door = arcade.get_sprites_at_point(
            self.scene["main_door"][0].position,
            self.doors_list
        )[0]

        door.unblock()

    def check_closet_breaking(self, delta_time):
        BASE_BREAK_CHANCE_PER_SECOND = 0.15

        for closet in self.closets_list:
            if closet.is_broken:
                continue

            if arcade.check_for_collision(self.ghost.sprite, closet):
                chance_per_frame = BASE_BREAK_CHANCE_PER_SECOND * delta_time

                if random.random() < chance_per_frame:
                    self.break_closet(closet)
                    return

    def break_closet(self, closet):
        closet.broke()

        if closet.player_sprite:
            closet.player_sprite.visible = True
            closet.player_sprite.speed = 1
            closet.player_sprite = None

        volume = SettingsManager.get_sound_volume()
        arcade.play_sound(CLOSET, volume=volume)

    def check_footprint_spawning(self, delta_time):
        if 'uf' not in self.evidences:
            return
        self.footprint_timer += delta_time

        if self.footprint_timer >= self.footprint_interval:
            self.footprint_timer = 0

            if random.random() < 0.0007 * 60:
                self.spawn_footprint_in_ghost_room()

            if self.ghost.is_hunt and not self.ghost.is_charging:
                self.spawn_footprint_near_broken_closets()

    def spawn_footprint_in_ghost_room(self):
        if not self.ghost.room or len(self.ghost.room) == 0:
            return

        room = self.ghost.room[0]

        padding = 50
        x = random.uniform(room.left + padding, room.right - padding)
        y = random.uniform(room.bottom + padding, room.top - padding)

        from .. import Footprint
        footprint = Footprint(x, y, lifetime=random.uniform(25, 30))
        self.footprints_list.append(footprint)

    def spawn_footprint_near_broken_closets(self):
        broken_closets = [c for c in self.closets_list if c.is_broken]

        if not broken_closets:
            return

        if random.random() < 0.1:
            closet = random.choice(broken_closets)

            offset_x = random.uniform(-40, 40)
            offset_y = random.uniform(-40, 40)

            x = closet.center_x + offset_x
            y = closet.center_y + offset_y

            footprint = Footprint(x, y, lifetime=random.uniform(25, 30))
            self.footprints_list.append(footprint)

    def open_settings(self):
        volume = SettingsManager.get_sound_volume()
        arcade.play_sound(SETTINGS, volume=volume)
        self.player_sprite.change_x = self.player_sprite.change_y = 0

        from ..views import SettingsView
        settings_view = SettingsView(back_callback=lambda: self.window.show_view(self))
        self.window.show_view(settings_view)
