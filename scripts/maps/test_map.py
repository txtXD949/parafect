import arcade

SPEED = 1


class TestMap(arcade.View):
    def __init__(self):
        super().__init__()

        self.pressed_E = False
        self.evids = ['emf5', 'mic', 'book', 'cold_temp']

        self.setup()

    def setup(self):
        # self.sound_player = arcade.play_sound(arcade.load_sound('././assets/sounds/effects/sad_ghost2(lobby).wav'), volume=0.1, loop=True)
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

        # Предметы
        self.items_list = arcade.SpriteList()

        from ..items import Thermometer, Microphone, EMF, Book, Pills, Lighter, Incense

        # Термометр
        self.thermometer = Thermometer()
        self.thermometer.create_sprite(1.0)
        self.thermometer.sprite.center_x, self.thermometer.sprite.center_y = self.map_width / 2 + 30, self.map_height / 2
        self.items_list.append(self.thermometer.sprite)

        # Микрофон
        self.mic = Microphone()
        self.mic.create_sprite(0.8)
        self.mic.sprite.center_x, self.mic.sprite.center_y = self.map_width / 2 + 60, self.map_height / 2
        self.items_list.append(self.mic.sprite)

        # Детектор ЭМП
        self.emf = EMF()
        self.emf.create_sprite(1.0)
        self.emf.sprite.center_x, self.emf.sprite.center_y = self.map_width / 2 + 30, self.map_height / 2 + 30
        self.items_list.append(self.emf.sprite)

        # Блокнот
        self.book = Book()
        self.book.create_sprite(1.0)
        self.book.sprite.center_x, self.book.sprite.center_y = self.map_width / 2 + 60, self.map_height / 2 + 60
        self.items_list.append(self.book.sprite)

        # Таблетки
        self.pills = Pills(20)
        self.pills.create_sprite(1.0)
        self.pills.sprite.center_x, self.pills.sprite.center_y = self.map_width / 2 + 60, self.map_height / 2 + 90
        self.items_list.append(self.pills.sprite)

        # Зажигалка
        self.lighter = Lighter()
        self.lighter.create_sprite(0.3)
        self.lighter.sprite.center_x, self.lighter.sprite.center_y = self.map_width / 2 + 90, self.map_height / 2
        self.items_list.append(self.lighter.sprite)

        # Благовония
        self.incense = Incense()
        self.incense.create_sprite(0.3)
        self.incense.sprite.center_x, self.incense.sprite.center_y = self.map_width / 2 + 30, self.map_height / 2 - 30
        self.items_list.append(self.incense.sprite)

    def on_draw(self) -> bool | None:
        self.clear()

        self.world_camera.use()

        self.scene.draw()
        self.player_list.draw()
        self.items_list.draw()

    def on_update(self, delta_time: float) -> bool | None:
        from .. import Muling, Banshee

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

        for item in self.items_list:
            item._class.update_item(self.player_sprite)
            if arcade.check_for_collision_with_list(item, self.scene['room']):
                item._class.in_room = True
            else:
                item._class.in_room = False

        self.emf.use_item(self.evids)
        self.book.use_item(self.evids)
        self.mic.use_item(self.evids, Muling(), [])
        self.thermometer.use_item(self.evids)
        self.incense.update_item(self.player_sprite)

        item_grab = arcade.check_for_collision_with_list(self.player_sprite, self.items_list)
        for item in item_grab:
            if self.pressed_E and not (any(item._class is it for it in self.player.inventory)):
                self.player.take_item(item._class)
        self.pressed_E = False

        print(self.player.has_lighter)

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
