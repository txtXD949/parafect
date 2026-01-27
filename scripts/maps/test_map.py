import random

from .. import Game

import arcade
from arcade.gui import UIManager

SPEED = 1


class TestMap(arcade.View):
    def __init__(self, game):
        super().__init__()

        self.game = game

        self.pressed_E = False

        self.evidences = self.game.ghost.evidences
        print(self.evidences, self.game.ghost)

        self.setup()

    def setup(self):
        # Микрофон (игрока)
        from .. import MicManager
        self.mic_manager = MicManager()
        self.mic_manager.start()

        # Карта
        self.tile_map = arcade.load_tilemap('././assets/maps/test_map.tmx', scaling=1.0)

        # Расчет размеров карты с учетом масштаба
        self.map_width = self.tile_map.width * self.tile_map.tile_width
        self.map_height = self.tile_map.height * self.tile_map.tile_height

        # Сцена
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Игрок
        from .. import PlayerSprite, Player
        self.player = self.game.player
        self.player.sanity = self.game.sanity
        self.player_sprite = PlayerSprite(scale=0.6)
        self.player_sprite.center_x, self.player_sprite.center_y = self.map_width / 2, self.map_height / 2

        self.player.sprite = self.player_sprite

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        # Физ.движок
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.scene['walls'])

        # Предметы
        self.items_sprite_list = arcade.SpriteList()
        self.items_list = []

        # Призрак
        self.ghost = self.game.ghost
        self.ghost.game = self.game
        self.ghost_sprite_list = arcade.SpriteList()
        self.ghost_sprite_list.append(self.ghost.sprite)

        self.spawn_ghost_in_room()

        # TODO: убрать
        self.ghost.ghost_event_chance = 0.0

        # Устанавливаем начальную позицию призрака
        self.ghost.physics.x = random.uniform(30, self.map_width - 30)
        self.ghost.physics.y = random.uniform(250, self.map_height - 30)
        self.ghost.sprite.center_x = self.ghost.physics.x
        self.ghost.sprite.center_y = self.ghost.physics.y

        # Сцены
        from ..views import ToolBoard
        self.tool_board = ToolBoard(self.game.inv, self, self.player)
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
            400,
            300
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

        self.gui_camera = arcade.Camera2D()

    def spawn_ghost_in_room(self):
        ghost_room = self.scene['room'][0]

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

        self.scene.draw(pixelated=True)
        self.player_sprite.footstep_particles.draw(pixelated=True)
        self.ghost_sprite_list.draw(pixelated=True)
        self.player_list.draw(pixelated=True)
        self.items_sprite_list.draw(pixelated=True)

        for item in self.items_list:
            if item.id == 'incense':
                item.smoke_particles.draw(pixelated=True)

        self.camera_shake.readjust_camera()

        self.gui_camera.use()
        self.draw_voice_level()

        self.manager.draw(pixelated=True)

    def on_update(self, delta_time: float) -> bool | None:
        self.mic_manager.update(delta_time)

        self.player_sprite.update(delta_time)
        self.player_sprite.footstep_particles.update(delta_time)

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

        # ДОБАВИЛ: Обновление призрака во время охоты
        if self.ghost.is_hunt:
            if not hasattr(self.ghost, 'hunt_initialized'):
                self.ghost.hunt_initialized = True
                self.spawn_ghost_in_room()

            # TODO: Получить реальное значение player_in_closet
            player_in_closet = False  # Заглушка, нужно реализовать

            # Получаем слой стен
            walls_layer = self.scene['ghost_walls']

            # Обновляем позицию призрака
            self.ghost.update_hunt(
                delta_time,
                self.player_sprite.center_x,
                self.player_sprite.center_y,
                player_in_closet,
                walls_layer
            )

        # Обновляем спрайт призрака
        self.ghost_sprite_list.update(delta_time)

        # Существующий вызов гост-ивента (оставляем как было)
        self.ghost.do_ghost_event(self.player_sprite.center_x, self.player_sprite.center_y)

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
            item._class.update_item(self.player_sprite)
            if arcade.check_for_collision_with_list(item, self.scene['room']):
                item._class.in_room = True
            else:
                item._class.in_room = False

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
        self.pressed_E = False

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        self.player_sprite.is_going = True

        if symbol == arcade.key.UP:
            self.player_sprite.change_y = SPEED

        if symbol == arcade.key.DOWN:
            self.player_sprite.change_y = -SPEED

        if symbol == arcade.key.LEFT:
            self.player_sprite.change_x = -SPEED

        if symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = SPEED

        if symbol == arcade.key.E:
            self.pressed_E = True

        if symbol == arcade.key.G:
            self.player.drop_item()

        if symbol == arcade.key.R:
            self.player.turn_on_item()

        if symbol == arcade.key.J:
            self.open_paper()

        if symbol == arcade.key.I:
            self.end_game()

        if symbol == arcade.key.H:
            self.ghost.start_hunt()

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

    def open_paper(self):
        if self.paper.visible:
            self.manager.remove(self.paper)
            self.paper.visible = False
            arcade.play_sound(arcade.load_sound('././assets/sounds/effects/close_paper.wav'))
            return
        self.manager.add(self.paper)
        self.paper.visible = True
        arcade.play_sound(arcade.load_sound('././assets/sounds/effects/open_paper.wav'))

    def set_end_flags(self):
        self.game.was_hunt = True  # TODO: убрать
        self.game.was_zero_sanity = True  # TODO: убрать
        self.game.was_first_death = True  # TODO: убрать
        self.game.was_death = False  # TODO: убрать
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

        self.open_paper()

        from ..views import ResultsView
        res = ResultsView(self.game)
        self.window.show_view(res)
