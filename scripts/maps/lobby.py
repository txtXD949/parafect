import random

import arcade

CAMERA_LERP = 0.3
SPEED = 1


class LobbyView(arcade.View):
    def __init__(self, account_manager):
        super().__init__()

        # Звук
        self.sound_player = None

        # Сцены
        self.map_board = None

        # Вспомогательное
        self.main_board_use = False
        self.map_board_use = False
        self.market_use = False

        # Шансы
        self.sound_ghost_chance = 0.0003

        # Файлики
        self.account_manager = account_manager
        self.game_state_path = '././database/_game.json'

        self.setup()

    def setup(self):
        from ..player import PlayerSprite

        # Фоновый звук
        self.sound_player = arcade.load_sound('././assets/sounds/background/lobby(1).mp3')
        self.sound_player.play(loop=True, volume=0.2)

        # Файлик
        self.create_game_state_file()

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

        from ..views import MapBoard
        self.map_board = MapBoard(lobby=self, account_manager=self.account_manager)

    def on_draw(self) -> bool | None:
        self.clear()

        self.world_camera.use()

        self.scene.draw(pixelated=True)
        self.player_list.draw(pixelated=True)
        self.player.footstep_particles.draw(pixelated=True)

    def on_update(self, delta_time: float) -> bool | None:
        # Всё обновляем
        self.physics_engine.update()
        self.player_list.update(delta_time)
        self.player.footstep_particles.update(delta_time)

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

        # Звук призрака
        if random.random() < self.sound_ghost_chance:
            sound = random.randint(0, 1)
            if sound:
                arcade.play_sound(arcade.load_sound('././assets/sounds/effects/sad_ghost1(lobby).wav'))
            else:
                arcade.play_sound(arcade.load_sound('././assets/sounds/effects/sad_ghost2(lobby).wav'))

        # Звук шагов
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
        arcade.play_sound(arcade.load_sound('././assets/sounds/effects/board1(lobby).wav'))
        self.player.change_x = self.player.change_y = 0

        from ..views import MainBoard
        main_board = MainBoard(lobby=self, account_manager=self.account_manager)
        self.window.show_view(main_board)

    def open_map_board(self):
        arcade.play_sound(arcade.load_sound('././assets/sounds/effects/board2(lobby).wav'))
        self.player.change_x = self.player.change_y = 0

        self.window.show_view(self.map_board)

    def open_market(self):
        arcade.play_sound(arcade.load_sound('././assets/sounds/effects/market(lobby).wav'), volume=0.03)
        self.player.change_x = self.player.change_y = 0

        from ..views import MarketView
        market = MarketView(lobby=self, account_manager=self.account_manager)
        self.window.show_view(market)

    def create_game_state_file(self):
        """Создает файл состояния игры при входе в лобби"""
        import json

        # Базовый набор предметов
        game_inventory = {
            'flash_light': 1,
            'emf': 1,
            'uf': 1,
            'dict': 1,
            'camera': 0,
            'term': 1,
            'mic': 1,
            'book': 1,
            'incense': 0,
            'lighter': 0,
            'pills': 0
        }

        game_state = {
            'inventory': game_inventory,
            'map': None,
            'difficulty': None
        }

        with open(self.game_state_path, 'w', encoding='utf-8') as f:
            json.dump(game_state, f, ensure_ascii=False, indent=2)
