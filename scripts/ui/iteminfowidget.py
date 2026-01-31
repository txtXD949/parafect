import arcade
from re import search


class ItemData:
    """Данные о предмете"""

    def __init__(self, item_id, name, price, description,
                 max_in_game, image_path, is_stationary=False, on_level=1):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.description = description
        self.max_in_game = max_in_game
        self.is_stationary = is_stationary
        self.on_level = on_level
        self.image_path = image_path

        self.in_inventory = 0
        self.selected = 0


ITEM_DATABASE = {
    'emf': ItemData(
        item_id='emf',
        name='ЭМП',
        price=200,
        description='Замеряет аномалии электрического поля.',
        max_in_game=2,
        image_path='././assets/images/itms/emf_off.png',
    ),
    'low_light': ItemData(
        item_id='low_light',
        name='СЛАБЫЙ ФОНАРИК',
        price=100,
        description='Достаточно света.',
        max_in_game=2,
        image_path='././assets/images/itms/uf.png'
    ),
    'book': ItemData(
        item_id='book',
        name='БЛОКНОТ',
        price=200,
        description='Стационарный. В нем без причины могут появиться записи.',
        max_in_game=2,
        is_stationary=True,
        image_path='././assets/images/itms/book1.png'
    ),
    'mic': ItemData(
        item_id='mic',
        name='НАПР-ЫЙ МИКРОФОН',
        price=200,
        description='Дает услышать странное шипение.',
        max_in_game=2,
        image_path='././assets/images/itms/mic_off.png'
    ),
    'dict': ItemData(
        item_id='dict',
        name='РАДИОПРИЕМНИК',
        price=200,
        description='Можно услышать голоса.',
        max_in_game=2,
        image_path='././assets/images/itms/dict_off.png'
    ),
    'term': ItemData(
        item_id='term',
        name='ТЕРМОМЕТР',
        price=150,
        description='Показывает температуру.',
        max_in_game=2,
        image_path='././assets/images/itms/term_norm.png'
    ),
    'flash_light': ItemData(
        item_id='flash_light',
        name='ФОНАРИК',
        price=350,
        description='Дает дополнительный свет.',
        max_in_game=4,
        image_path='././assets/images/itms/flash_light.png',
        on_level=20
    ),
    'incense': ItemData(
        item_id='incense',
        name='БЛАГОВОНИЯ',
        price=150,
        description='Защитит от паранормальных явлений.',
        max_in_game=4,
        image_path='././assets/images/itms/incense.png',
        on_level=15
    ),
    'lighter': ItemData(
        item_id='lighter',
        name='ЗАЖИГАЛКА',
        price=50,
        description='Дает зажечь благовония.',
        max_in_game=4,
        image_path='././assets/images/itms/light.png',
        on_level=10
    ),
    'pills': ItemData(
        item_id='pills',
        name='УСПОКОИТЕЛЬНОЕ',
        price=150,
        description='Приведет в себя.',
        max_in_game=4,
        image_path='././assets/images/itms/pills.png',
        on_level=20
    )
}

import arcade
from re import search


class ItemInfoWidget:
    def __init__(self, x, y, width, height, player_level):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.current_item = None
        self.ui_elements = []
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0

        self.image_sprite_list = arcade.SpriteList()
        self.image_sprite = None

        self.player_level = player_level

    def add_to_manager(self, manager):
        """Добавляем UI элементы в менеджер"""
        # Заголовок
        title = arcade.gui.UILabel(
            text='ИНФОРМАЦИЯ',
            font_name='Courier New',
            font_size=int(18 * self.scale),
            text_color=arcade.color.WHITE,
            align='center'
        )
        title.center_x = self.x + self.width // 2
        title.top = self.y - 35 * self.scale
        manager.add(title)
        self.ui_elements.append(title)

        # Название
        self.name_label = arcade.gui.UILabel(
            text='',
            font_name='Courier New',
            font_size=int(19 * self.scale),
            text_color=arcade.color.WHITE,
            align='center',
            width=self.width - 35 * self.scale
        )
        self.name_label.center_x = self.x + self.width // 2
        self.name_label.top = self.y - 160 * self.scale
        manager.add(self.name_label)
        self.ui_elements.append(self.name_label)

        # Цена
        self.price_label = arcade.gui.UILabel(
            text='Цена: ',
            font_name='Courier New',
            font_size=int(15 * self.scale),
            text_color=arcade.color.WHITE,
            align='left',
            width=self.width - 35 * self.scale
        )
        self.price_label.left = self.x + 18 * self.scale
        self.price_label.top = self.y - 170 * self.scale
        manager.add(self.price_label)
        self.ui_elements.append(self.price_label)

        # Максимум в игру
        self.on_level_ = arcade.gui.UILabel(
            text='В игру: ',
            font_name='Courier New',
            font_size=int(15 * self.scale),
            text_color=arcade.color.WHITE,
            align='left',
            width=self.width - 35 * self.scale
        )
        self.on_level_.left = self.x + 18 * self.scale
        self.on_level_.top = self.y - 200 * self.scale
        manager.add(self.on_level_)
        self.ui_elements.append(self.on_level_)

        # В инвентаре
        self.inventory_label = arcade.gui.UILabel(
            text='В инвентаре: ',
            font_name='Courier New',
            font_size=int(15 * self.scale),
            text_color=arcade.color.WHITE,
            align='left',
            width=self.width - 35 * self.scale
        )
        self.inventory_label.left = self.x + 18 * self.scale
        self.inventory_label.top = self.y - 230 * self.scale
        manager.add(self.inventory_label)
        self.ui_elements.append(self.inventory_label)

        # С собой
        self.taken_label = arcade.gui.UILabel(
            text='С собой: ',
            font_name='Courier New',
            font_size=int(15 * self.scale),
            text_color=arcade.color.WHITE,
            align='left',
            width=self.width - 35 * self.scale
        )
        self.taken_label.left = self.x + 18 * self.scale
        self.taken_label.top = self.y - 260 * self.scale
        manager.add(self.taken_label)
        self.ui_elements.append(self.taken_label)

        # Описание
        self.desc_label = arcade.gui.UILabel(
            text='',
            font_name='Courier New',
            font_size=int(12 * self.scale),
            text_color=arcade.color.LIGHT_GRAY,
            align='left',
            width=self.width - 35 * self.scale,
            multiline=True,
            height=60 * self.scale
        )
        self.desc_label.left = self.x + 18 * self.scale
        self.desc_label.top = self.y - 290 * self.scale
        manager.add(self.desc_label)
        self.ui_elements.append(self.desc_label)

    def update_info(self, item_data):
        self.current_item = item_data

        self.image_sprite_list.clear()
        self.image_sprite = None

        if not item_data:
            self.name_label.text = 'ВЫБЕРИТЕ ТОВАР'
            self.price_label.text = 'Цена: '
            self.on_level_.text = 'На уровне: '
            self.inventory_label.text = 'В инвентаре: '
            self.taken_label.text = 'С собой: '
            self.desc_label.text = ''
            return

        # Обновляем текст
        self.name_label.text = item_data.name
        self.price_label.text = f'Цена: {item_data.price}$'
        self.inventory_label.text = f'В инвентаре: {item_data.in_inventory}'
        self.taken_label.text = f'С собой: {item_data.selected}/{item_data.max_in_game}'
        self.desc_label.text = item_data.description

        if item_data.on_level > self.player_level:
            self.on_level_.text = f'На уровне: {item_data.on_level}'
        else:
            self.on_level_.text = ''

        # Загружаем картинку в спрайт
        image_path = getattr(item_data, 'images_path', None) or getattr(item_data, 'image_path', None)

        if search(r'light\.png', image_path):
            self.image_sprite = arcade.Sprite(image_path, scale=2.5 * self.scale)
        elif search(r'blag\.png', image_path):
            self.image_sprite = arcade.Sprite(image_path, scale=1.4 * self.scale)
        else:
            self.image_sprite = arcade.Sprite(image_path, scale=4.2 * self.scale)

        self.image_sprite.center_x = self.x + self.width // 2
        self.image_sprite.center_y = self.y - 95 * self.scale

        self.image_sprite_list.append(self.image_sprite)

    def draw_background(self):
        """Рисуем фон"""
        arcade.draw_lrbt_rectangle_filled(
            left=self.x,
            right=self.x + self.width,
            bottom=self.y - self.height - 30 * self.scale,
            top=self.y - 17 * self.scale,
            color=(30, 30, 30)
        )

    def draw_image(self):
        """Рисуем картинку предмета"""
        if self.image_sprite_list:
            self.image_sprite_list.draw()
