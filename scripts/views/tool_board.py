import random

import arcade


class ToolBoard(arcade.View):
    def __init__(self, inv, map, player, bias_scale=1):
        super().__init__()

        self.map = map
        self.player = player

        self.inv = inv

        self.gui_camera = None
        self.world_camera = None

        self.bias_scale = bias_scale

        self.setup()
        self.set_tools()

    def setup(self):
        # Камеры
        self.world_camera = arcade.Camera2D(
            projection=arcade.rect.XYWH(0, 0, 800, 600),
            position=(400, 300)
        )
        self.gui_camera = arcade.Camera2D()

    def set_tools(self):
        self.tools_sprites = arcade.SpriteList()
        self.tools = []

        from ..items import Thermometer, Microphone, EMF, Book, Pills, Lighter, Incense, Dictaphone, FlashLight, UF

        emfs = [EMF(self.bias_scale) for _ in range(self.inv['emf'])]
        try:
            emf1 = emfs[0]
            emf1.create_board_sprite()
            emf1.create_sprite(1.0)
            self.map.emf1 = emf1
            self.map.items_sprite_list.append(emf1.sprite)
            emf1.board_sprite.center_x, emf1.board_sprite.center_y = 100, 450
            self.tools_sprites.append(emf1.board_sprite)
            self.tools.append(emf1)

            emf2 = emfs[1]
            emf2.create_board_sprite()
            emf2.create_sprite(1.0)
            self.map.emf2 = emf2
            self.map.items_sprite_list.append(emf2.sprite)
            emf2.board_sprite.center_x, emf2.board_sprite.center_y = 100 + 50, 450
            self.tools_sprites.append(emf2.board_sprite)
            self.tools.append(emf2)

        except IndexError:
            pass

        ufs = [UF(self.bias_scale) for _ in range(self.inv['uf'])]
        try:
            uf1 = ufs[0]
            uf1.create_board_sprite()
            uf1.create_sprite(1.0)
            self.map.uf1 = uf1
            self.map.items_sprite_list.append(uf1.sprite)
            uf1.board_sprite.center_x, uf1.board_sprite.center_y = 125, 370
            self.tools_sprites.append(uf1.board_sprite)
            self.tools.append(uf1)

            uf2 = ufs[1]
            uf2.create_board_sprite()
            uf2.create_sprite(1.0)
            self.map.uf2 = uf2
            self.map.items_sprite_list.append(uf2.sprite)
            uf2.board_sprite.center_x, uf2.board_sprite.center_y = 125, 320
            self.tools_sprites.append(uf2.board_sprite)
            self.tools.append(uf2)

        except IndexError:
            pass

        books = [Book(self.bias_scale) for _ in range(self.inv['book'])]
        try:
            book1 = books[0]
            book1.create_board_sprite()
            book1.create_sprite(1.0)
            self.map.book1 = book1
            self.map.items_sprite_list.append(book1.sprite)
            book1.board_sprite.center_x, book1.board_sprite.center_y = 230, 450
            self.tools_sprites.append(book1.board_sprite)
            self.tools.append(book1)

            book2 = books[1]
            book2.create_board_sprite()
            book2.create_sprite(1.0)
            self.map.book2 = book2
            self.map.items_sprite_list.append(book2.sprite)
            book2.board_sprite.center_x, book2.board_sprite.center_y = 320, 450
            self.tools_sprites.append(book2.board_sprite)
            self.tools.append(book2)

        except IndexError:
            pass

        mics = [Microphone(self.bias_scale) for _ in range(self.inv['mic'])]
        try:
            mic1 = mics[0]
            mic1.create_board_sprite()
            mic1.create_sprite(0.8)
            self.map.mic1 = mic1
            self.map.items_sprite_list.append(mic1.sprite)
            mic1.board_sprite.center_x, mic1.board_sprite.center_y = 530, 450
            self.tools_sprites.append(mic1.board_sprite)
            self.tools.append(mic1)

            mic2 = mics[1]
            mic2.create_board_sprite()
            mic2.create_sprite(0.8)
            self.map.mic2 = mic2
            self.map.items_sprite_list.append(mic2.sprite)
            mic2.board_sprite.center_x, mic2.board_sprite.center_y = 625, 450
            self.tools_sprites.append(mic2.board_sprite)
            self.tools.append(mic2)

        except IndexError:
            pass

        dicts = [Dictaphone(self.bias_scale) for _ in range(self.inv['dict'])]
        try:
            dict1 = dicts[0]
            dict1.create_board_sprite()
            dict1.create_sprite(1.0)
            self.map.dict1 = dict1
            self.map.items_sprite_list.append(dict1.sprite)
            dict1.board_sprite.center_x, dict1.board_sprite.center_y = 400, 450
            self.tools_sprites.append(dict1.board_sprite)
            self.tools.append(dict1)

            dict2 = dicts[1]
            dict2.create_board_sprite()
            dict2.create_sprite(1.0)
            self.map.dict2 = dict2
            self.map.items_sprite_list.append(dict2.sprite)
            dict2.board_sprite.center_x, dict2.board_sprite.center_y = 450, 450
            self.tools_sprites.append(dict2.board_sprite)
            self.tools.append(dict2)

        except IndexError:
            pass

        terms = [Thermometer(self.bias_scale) for _ in range(self.inv['term'])]
        try:
            term1 = terms[0]
            term1.create_board_sprite()
            term1.create_sprite(1.0)
            self.map.term1 = term1
            self.map.items_sprite_list.append(term1.sprite)
            term1.board_sprite.center_x, term1.board_sprite.center_y = 430, 370
            self.tools_sprites.append(term1.board_sprite)
            self.tools.append(term1)

            term2 = terms[1]
            term2.create_board_sprite()
            term2.create_sprite(1.0)
            self.map.term2 = term2
            self.map.items_sprite_list.append(term2.sprite)
            term2.board_sprite.center_x, term2.board_sprite.center_y = 430, 320
            self.tools_sprites.append(term2.board_sprite)
            self.tools.append(term2)

        except IndexError:
            pass

        flash_lights = [FlashLight(self.bias_scale) for _ in range(self.inv['flash_light'])]
        try:
            flash_light1 = flash_lights[0]
            flash_light1.create_board_sprite()
            flash_light1.create_sprite(0.7)
            self.map.flash_light1 = flash_light1
            self.map.items_sprite_list.append(flash_light1.sprite)
            flash_light1.board_sprite.center_x, flash_light1.board_sprite.center_y = 230, 320
            self.tools_sprites.append(flash_light1.board_sprite)
            self.tools.append(flash_light1)

            flash_light2 = flash_lights[1]
            flash_light2.create_board_sprite()
            flash_light2.create_sprite(0.7)
            self.map.flash_light2 = flash_light2
            self.map.items_sprite_list.append(flash_light2.sprite)
            flash_light2.board_sprite.center_x, flash_light2.board_sprite.center_y = 230, 370
            self.tools_sprites.append(flash_light2.board_sprite)
            self.tools.append(flash_light2)

            flash_light3 = flash_lights[2]
            flash_light3.create_board_sprite()
            flash_light3.create_sprite(0.7)
            self.map.flash_light3 = flash_light3
            self.map.items_sprite_list.append(flash_light3.sprite)
            flash_light3.board_sprite.center_x, flash_light3.board_sprite.center_y = 320, 320
            self.tools_sprites.append(flash_light3.board_sprite)
            self.tools.append(flash_light3)

            flash_light4 = flash_lights[3]
            flash_light4.create_board_sprite()
            flash_light4.create_sprite(0.7)
            self.map.flash_light4 = flash_light4
            self.map.items_sprite_list.append(flash_light4.sprite)
            flash_light4.board_sprite.center_x, flash_light4.board_sprite.center_y = 320, 370
            self.tools_sprites.append(flash_light4.board_sprite)
            self.tools.append(flash_light4)

        except IndexError:
            pass

        incenses = [Incense(self.bias_scale) for _ in range(self.inv['incense'])]
        try:
            incense1 = incenses[0]
            incense1.create_board_sprite()
            incense1.create_sprite(1.0)
            self.map.incense1 = incense1
            self.map.items_sprite_list.append(incense1.sprite)
            incense1.board_sprite.center_x, incense1.board_sprite.center_y = 125, 250
            incense1.board_sprite.angle = 90
            self.tools_sprites.append(incense1.board_sprite)
            self.tools.append(incense1)

            incense2 = incenses[1]
            incense2.create_board_sprite()
            incense2.create_sprite(1.0)
            self.map.incense2 = incense2
            self.map.items_sprite_list.append(incense2.sprite)
            incense2.board_sprite.center_x, incense2.board_sprite.center_y = 125, 200
            incense2.board_sprite.angle = 90
            self.tools_sprites.append(incense2.board_sprite)
            self.tools.append(incense2)

            incense3 = incenses[2]
            incense3.create_board_sprite()
            incense3.create_sprite(1.0)
            self.map.incense3 = incense3
            self.map.items_sprite_list.append(incense3.sprite)
            incense3.board_sprite.center_x, incense3.board_sprite.center_y = 125, 150
            incense3.board_sprite.angle = 90
            self.tools_sprites.append(incense3.board_sprite)
            self.tools.append(incense3)

            incense4 = incenses[3]
            incense4.create_board_sprite()
            incense4.create_sprite(1.0)
            self.map.incense4 = incense4
            self.map.items_sprite_list.append(incense4.sprite)
            incense4.board_sprite.center_x, incense4.board_sprite.center_y = 125, 100
            incense4.board_sprite.angle = 90
            self.tools_sprites.append(incense4.board_sprite)
            self.tools.append(incense4)

        except IndexError:
            pass

        lighters = [Lighter(self.bias_scale) for _ in range(self.inv['lighter'])]
        try:
            lighter1 = lighters[0]
            lighter1.create_board_sprite()
            lighter1.create_sprite(0.3)
            self.map.lighter1 = lighter1
            self.map.items_sprite_list.append(lighter1.sprite)
            lighter1.board_sprite.center_x, lighter1.board_sprite.center_y = 215, 230
            lighter1.board_sprite.angle = random.randint(0, 360)
            self.tools_sprites.append(lighter1.board_sprite)
            self.tools.append(lighter1)

            lighter2 = lighters[1]
            lighter2.create_board_sprite()
            lighter2.create_sprite(0.3)
            self.map.lighter2 = lighter2
            self.map.items_sprite_list.append(lighter2.sprite)
            lighter2.board_sprite.center_x, lighter2.board_sprite.center_y = 255, 215
            lighter2.board_sprite.angle = random.randint(0, 360)
            self.tools_sprites.append(lighter2.board_sprite)
            self.tools.append(lighter2)

            lighter3 = lighters[2]
            lighter3.create_board_sprite()
            lighter3.create_sprite(0.3)
            self.map.lighter3 = lighter3
            self.map.items_sprite_list.append(lighter3.sprite)
            lighter3.board_sprite.center_x, lighter3.board_sprite.center_y = 280, 225
            lighter3.board_sprite.angle = random.randint(0, 360)
            self.tools_sprites.append(lighter3.board_sprite)
            self.tools.append(lighter3)

            lighter4 = lighters[3]
            lighter4.create_board_sprite()
            lighter4.create_sprite(0.3)
            self.map.lighter4 = lighter4
            self.map.items_sprite_list.append(lighter4.sprite)
            lighter4.board_sprite.center_x, lighter4.board_sprite.center_y = 325, 220
            lighter4.board_sprite.angle = random.randint(0, 360)
            self.tools_sprites.append(lighter4.board_sprite)
            self.tools.append(lighter4)

        except IndexError:
            pass

        pills = [Pills(self.map.game.add_sanity, self.bias_scale) for _ in range(self.inv['pills'])]
        try:
            pills1 = pills[0]
            pills1.create_board_sprite()
            pills1.create_sprite(1.0)
            self.map.pills1 = pills1
            self.map.items_sprite_list.append(pills1.sprite)
            pills1.board_sprite.center_x, pills1.board_sprite.center_y = 210, 130
            pills1.board_sprite.angle = random.randint(0, 360)
            self.tools_sprites.append(pills1.board_sprite)
            self.tools.append(pills1)

            pills2 = pills[1]
            pills2.create_board_sprite()
            pills2.create_sprite(1.0)
            self.map.pills2 = pills2
            self.map.items_sprite_list.append(pills2.sprite)
            pills2.board_sprite.center_x, pills2.board_sprite.center_y = 245, 120
            pills2.board_sprite.angle = random.randint(0, 360)
            self.tools_sprites.append(pills2.board_sprite)
            self.tools.append(pills2)

            pills3 = pills[2]
            pills3.create_board_sprite()
            pills3.create_sprite(1.0)
            self.map.pills3 = pills3
            self.map.items_sprite_list.append(pills3.sprite)
            pills3.board_sprite.center_x, pills3.board_sprite.center_y = 285, 135
            pills3.board_sprite.angle = random.randint(0, 360)
            self.tools_sprites.append(pills3.board_sprite)
            self.tools.append(pills3)

            pills4 = pills[3]
            pills4.create_board_sprite()
            pills4.create_sprite(1.0)
            self.map.pills4 = pills4
            self.map.items_sprite_list.append(pills4.sprite)
            pills4.board_sprite.center_x, pills4.board_sprite.center_y = 311, 118
            pills4.board_sprite.angle = random.randint(0, 360)
            self.tools_sprites.append(pills4.board_sprite)
            self.tools.append(pills4)

        except IndexError:
            pass

        self.phantom_items = arcade.SpriteList()
        self.gray_items = arcade.SpriteList()
        for it in self.tools_sprites[:]:
            self.phantom_items.append(it)

            if it._class.id == 'lighter':
                continue
            gray_sprite = arcade.Sprite(it.texture.file_path, scale=it.scale)
            gray_sprite.center_x, gray_sprite.center_y = it.center_x, it.center_y
            gray_sprite.angle = it._angle
            gray_sprite.color = (118, 118, 118, 230)

            self.gray_items.append(gray_sprite)

        self.map.items_list = self.tools

        for item in self.map.items_sprite_list:
            item.scale = self.bias_scale

    def on_draw(self) -> bool | None:
        self.clear()

        self.world_camera.use()
        arcade.draw_rect_filled(arcade.rect.LBWH(20, 20, 760, 560),
                                color=arcade.color.Color.from_hex_string('#C8C8C8'))

        for i in range(16):
            for j in range(13):
                arcade.draw_line(40 + 55 * i - 2, 50 + 55 * j - 2, 40 + 55 * i + 2, 50 + 55 * j + 2,
                                 color=arcade.color.BLACK, line_width=0.1)
                arcade.draw_line(40 + 55 * i + 2, 50 + 55 * j - 2, 40 + 55 * i - 2, 50 + 55 * j + 2,
                                 color=arcade.color.BLACK, line_width=0.1)

        arcade.draw_rect_filled(arcade.rect.LRBT(190, 360, 200, 250),
                                color=arcade.color.Color.from_hex_string('#5b5b5b'))

        arcade.draw_rect_filled(arcade.rect.LRBT(190, 360, 100, 150),
                                color=arcade.color.Color.from_hex_string('#5b5b5b'))

        self.gray_items.draw(pixelated=True)
        self.tools_sprites.draw(pixelated=True)

        # Закрыть тулборд
        arcade.draw_rect_filled(
            arcade.rect.XYWH(400, 30, 50, 20),
            color=(118, 118, 118)
        )
        arcade.draw_line(400, 25, 410, 30, color=arcade.color.BLACK)
        arcade.draw_line(400, 25, 390, 30, color=arcade.color.BLACK)

    def on_show_view(self) -> None:
        arcade.play_sound(arcade.load_sound('././assets/sounds/effects/board1(lobby).wav'))

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        world_cords = self.world_camera.unproject((x, y))

        if 375 < world_cords.x < 425 and 20 < world_cords.y < 40:
            self.close()
            return

        sprites = (
            arcade.get_sprites_at_point(world_cords, self.tools_sprites),
            arcade.get_sprites_at_point(world_cords, self.phantom_items)
        )
        if len(sprites) == 2 and all(sprites):
            self.take_tool(sprites[0][0]._class)

        if sprites[1] and not sprites[0]:
            self.put_tool(sprites[1][0]._class)

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.ESCAPE:
            self.close()

    def take_tool(self, item):
        if item.id in ('lighter',):
            if not self.player.has_lighter:
                self.player.take_item(item)
                self.tools_sprites.remove(item.board_sprite)
                return
            else:
                return

        if len(self.player.inventory) == 2:
            return

        self.player.take_item(item)
        self.tools_sprites.remove(item.board_sprite)
        try:
            self.map.items_sprite_list.append(item.sprite)
        except ValueError:
            pass

    def put_tool(self, item):
        if item.id in ('lighter',):
            return

        if not self.player.put_item(item):
            return
        self.map.items_sprite_list.remove(item.sprite)
        self.tools_sprites.append(item.board_sprite)

    def close(self):
        arcade.play_sound(arcade.load_sound('././assets/sounds/effects/board1(lobby).wav'))
        self.window.show_view(self.map)
