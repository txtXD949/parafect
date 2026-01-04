import random

import arcade

CAMERA_LERP = 0.3
SPEED = 1


class LobbyView(arcade.View):
    def __init__(self):
        super().__init__()

        self.sound_player = None

        self.main_board_use = False
        self.map_board_use = False
        self.market_use = False

        self.sound_ghost_chance = 0.0003

        self.setup()

    def setup(self):
        from ..player import PlayerSprite

        self.sound_player = arcade.load_sound('././assets/sounds/background/lobby(1).mp3')
        self.sound_player.play(loop=True, volume=0.2)

        # Карта
        self.tile_map = arcade.load_tilemap('././assets/maps/lobby.tmx', scaling=1.0)

        # Расчет размеров карты с учетом масштаба
        self.map_width = self.tile_map.width * self.tile_map.tile_width
        self.map_height = self.tile_map.height * self.tile_map.tile_height

        # Сцена
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Игрок
        self.player = PlayerSprite(scale=0.6)
        self.player.center_x, self.player.center_y = self.map_width / 2, self.map_height / 2

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # Физ.движок
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.scene['collitions'])

        # Камера
        self.world_camera = arcade.Camera2D()
        self.world_camera.zoom = 1.0

        self.world_camera.projection = arcade.rect.XYWH(
            0, 0,
            self.map_width,
            self.map_height
        )

        self.world_camera.viewport_width = self.width
        self.world_camera.viewport_height = self.height

        self.world_camera.position = (
            self.map_width / 2,
            self.map_height / 2
        )

    def on_draw(self) -> bool | None:
        self.clear()

        self.world_camera.use()

        self.scene.draw()
        self.player_list.draw()

    def on_update(self, delta_time: float) -> bool | None:
        self.physics_engine.update()
        self.player_list.update()

        # Доска игры
        hit = arcade.check_for_collision_with_list(self.player, self.scene['main_board'])
        if hit:
            if not self.main_board_use:
                self.open_main_board()
            self.main_board_use = True
        else:
            self.main_board_use = False

        # Доска карт
        hit = arcade.check_for_collision_with_list(self.player, self.scene['map_board'])
        if hit:
            if not self.map_board_use:
                self.open_map_board()
            self.map_board_use = True
        else:
            self.map_board_use = False

        # Маркет
        hit = arcade.check_for_collision_with_list(self.player, self.scene['market'])
        if hit:
            if not self.market_use:
                self.open_market()
            self.market_use = True
        else:
            self.market_use = False

        # звук призрака
        if random.random() < self.sound_ghost_chance:
            sound = random.randint(0, 1)
            if sound:
                arcade.play_sound(arcade.load_sound('././assets/sounds/effects/sad_ghost1(lobby).wav'))
            else:
                arcade.play_sound(arcade.load_sound('././assets/sounds/effects/sad_ghost2(lobby).wav'))

        if self.player.is_going:
            if self.player.animation_timer in (8,):
                if arcade.check_for_collision_with_list(self.player, self.scene['carpet']):
                    if self.player.bottom >= 16 * 3:
                        arcade.play_sound(arcade.load_sound('././assets/sounds/effects/carpet_footsteps.wav'),
                                          volume=0.03)
                    else:
                        arcade.play_sound(arcade.load_sound('././assets/sounds/effects/ground_footsteps.wav'),
                                          volume=0.03)
                elif arcade.check_for_collision_with_list(self.player, self.scene['ground']):
                    arcade.play_sound(arcade.load_sound('././assets/sounds/effects/ground_footsteps.wav'), volume=0.03)

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        self.player.is_going = True

        if symbol == arcade.key.UP:
            self.player.change_y = SPEED

        if symbol == arcade.key.DOWN:
            self.player.change_y = -SPEED

        if symbol == arcade.key.LEFT:
            self.player.change_x = -SPEED

        if symbol == arcade.key.RIGHT:
            self.player.change_x = SPEED

    def on_key_release(self, symbol: int, modifiers: int) -> bool | None:
        if symbol in (arcade.key.UP, arcade.key.DOWN):
            self.player.change_y = 0
        if symbol in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0

    def open_main_board(self):
        # TODO: сделать главную доску
        arcade.play_sound(arcade.load_sound('././assets/sounds/effects/board1(lobby).wav'))
        ...

    def open_map_board(self):
        # TODO: сделать доску карт
        arcade.play_sound(arcade.load_sound('././assets/sounds/effects/board2(lobby).wav'))
        ...

    def open_market(self):
        # TODO: сделать маркет
        arcade.play_sound(arcade.load_sound('././assets/sounds/effects/market(lobby).wav'), volume=0.04)
        ...
