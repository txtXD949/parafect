from .. import Game

import arcade

SPEED = 1


class TestMap(arcade.View):
    def __init__(self, game):
        super().__init__()

        self.game = game

        self.pressed_E = False

        self.evidences = self.game.ghost.evidences + ['cold_temp']
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
        self.player = Player()
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

        # Сцены
        from ..views import ToolBoard
        self.tool_board = ToolBoard(self.game.inv, self, self.player)
        self.tool_board_use = False

        self.sanity_screen = None
        self.paper = None

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

        self.scene.draw()
        self.player_list.draw()
        self.items_sprite_list.draw()

        self.incense1.smoke_particles.draw()
        self.incense2.smoke_particles.draw()
        self.incense3.smoke_particles.draw()
        self.incense4.smoke_particles.draw()

        self.gui_camera.use()
        self.draw_voice_level()

    def on_update(self, delta_time: float) -> bool | None:
        self.mic_manager.update(delta_time)

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

        for item in self.items_sprite_list:
            item._class.update_item(self.player_sprite)
            if arcade.check_for_collision_with_list(item, self.scene['room']):
                item._class.in_room = True
            else:
                item._class.in_room = False

        self.emf1.use_item(self.evidences)
        self.emf2.use_item(self.evidences)
        self.book1.use_item(self.evidences)
        self.book2.use_item(self.evidences)
        self.mic1.use_item(self.evidences, Muling(), [])
        self.mic2.use_item(self.evidences, Muling(), [])
        self.term1.use_item(self.evidences)
        self.term2.use_item(self.evidences)
        self.incense1.update_item(self.player_sprite)
        self.incense2.update_item(self.player_sprite)
        self.incense3.update_item(self.player_sprite)
        self.incense4.update_item(self.player_sprite)
        self.dict1.use_item(self.player_sprite, ghost=Siren(), evidences=self.evidences)
        self.dict2.use_item(self.player_sprite, ghost=Siren(), evidences=self.evidences)
        if self.dict1.is_turn_on:
            self.dict1.update_voice_detection(self.player)
        if self.dict2.is_turn_on:
            self.dict2.update_voice_detection(self.player)

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
