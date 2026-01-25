from arcade.future.light import LightLayer, Light

from .. import Game

import arcade
from arcade.gui import UIManager

SPEED = 1


class Dom1(arcade.View):
    def __init__(self, game):
        super().__init__()

        self.game = game

        self.pressed_E = False

        self.is_under_roof = False

        self.evidences = self.game.ghost.evidences
        print(self.evidences, self.game.ghost)

        self.setup()

    def setup(self):
        # Микрофон (игрока)
        from .. import MicManager
        self.mic_manager = MicManager()
        self.mic_manager.start()

        # Карта
        self.tile_map = arcade.load_tilemap('././assets/maps/house1.tmx', scaling=1.0)

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

        self.player_sprite.center_x, self.player_sprite.center_y = 18 * 16, 3 * 16

        self.player.sprite = self.player_sprite

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        # Физ.движок
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.scene['collitions'])

        # Предметы
        self.items_sprite_list = arcade.SpriteList()
        self.items_list = []

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
            16 * 12,
            9 * 12
        )

        self.world_camera.viewport_width = self.width
        self.world_camera.viewport_height = self.height

        self.world_camera.position = (
            self.map_width / 2,
            self.map_height / 2
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

        # Звуки
        self.grass_footsteps = arcade.load_sound('././assets/sounds/effects/grass_footsteps.wav')
        self.carpet_footsteps = arcade.load_sound('././assets/sounds/effects/carpet_footsteps.wav')

        self.gui_camera = arcade.Camera2D()

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

        self.world_camera.use()

        self.scene["ground"].draw(pixelated=True)
        self.scene["floor"].draw(pixelated=True)
        self.scene["carpet"].draw(pixelated=True)
        self.scene["walls"].draw(pixelated=True)
        self.doors_list.draw(pixelated=True)
        self.closets_list.draw(pixelated=True)
        self.scene["furniture_back"].draw(pixelated=True)
        self.player_sprite.footstep_particles.draw(pixelated=True)
        self.player_list.draw(pixelated=True)
        self.items_sprite_list.draw(pixelated=True)
        self.scene["furniture_front"].draw(pixelated=True)
        self.scene["roof"].draw(pixelated=True)


        for item in self.items_list:
            if item.id == 'incense':
                item.smoke_particles.draw(pixelated=True)

        self.gui_camera.use()
        self.draw_voice_level()

        self.manager.draw(pixelated=True)

    def on_update(self, delta_time: float) -> bool | None:
        self.mic_manager.update(delta_time)

        self.player_sprite.update()
        self.player_sprite.footstep_particles.update(delta_time)

        from .. import Muling, Banshee, Siren

        self.physics_engine.update()

        pos = (
            self.player_sprite.center_x,
            self.player_sprite.center_y
        )
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            pos,
            0.5
        )

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

        # for item in self.items_sprite_list:
        #     item._class.update_item(self.player_sprite)
        #     if arcade.check_for_collision_with_list(item, self.scene['room']):
        #         item._class.in_room = True
        #     else:
        #         item._class.in_room = False

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

        # Двери
        if self.pressed_E and (doors := arcade.check_for_collision_with_list(self.player_sprite, self.doors_list)):
            doors[0].change()

        # Шкафы
        if self.pressed_E and (closets := arcade.check_for_collision_with_list(self.player_sprite, self.closets_list)):
            closets[0].interact(self.player_sprite)
        self.pressed_E = False

        # Рендер крыши
        if arcade.check_for_collision_with_list(self.player_sprite, self.scene["roof"]):
            self.is_under_roof = True
        else:
            self.is_under_roof = False
        self.smooth_roof()

        # Звук шагов
        if self.player_sprite.is_going:
            if self.player_sprite.animation_timer in (8,):
                if arcade.check_for_collision_with_list(self.player_sprite, self.scene['carpet']):
                    if self.player_sprite.bottom >= 16 * 3:
                        arcade.play_sound(self.carpet_footsteps,
                                          volume=0.03)
                    else:
                        arcade.play_sound(self.grass_footsteps,
                                          volume=0.03)
                elif arcade.check_for_collision_with_list(self.player_sprite, self.scene['ground']):
                    arcade.play_sound(self.grass_footsteps, volume=0.03)


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

    def smooth_roof(self):
        if self.is_under_roof:
            if self.scene["roof"].alpha_normalized > 0:
                self.scene["roof"].alpha_normalized -= 0.05
        else:
            if self.scene["roof"].alpha_normalized < 1:
                self.scene["roof"].alpha_normalized += 0.05
