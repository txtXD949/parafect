import arcade
from re import search


class ItemData:
    """Данные о предмете"""

    def __init__(self, item_id, name, price, description,
                 max_in_game, image_path, is_stationary=False):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.description = description
        self.max_in_game = max_in_game
        self.is_stationary = is_stationary
        self.image_path = image_path

        self.in_inventory = 0
        self.selected = 0


ITEM_DATABASE = {
    'emf': ItemData(
        item_id='emf',
        name='ЭМП',
        price=200,
        description='Ловит сигнал там, где призрак взаимодействовал',
        max_in_game=2,
        image_path='././assets/images/itms/emf.png'
    ),
    'uf': ItemData(
        item_id='uf',
        name='УФ-ФОНАРИК',
        price=150,
        description='Показывает отпечатки',
        max_in_game=2,
        image_path='././assets/images/itms/uf.png'
    ),
    'book': ItemData(
        item_id='book',
        name='БЛОКНОТ',
        price=200,
        description='Стационарный. Призрак оставляет в нем следы',
        max_in_game=2,
        is_stationary=True,
        image_path='././assets/images/itms/book1.png'
    ),
    'mic': ItemData(
        item_id='mic',
        name='НАПР-ЫЙ МИКРОФОН',
        price=200,
        description='Дает услышать шипение призрака',
        max_in_game=2,
        image_path='././assets/images/itms/mic.png'
    ),
    'dict': ItemData(
        item_id='dict',
        name='ДИКТОФОН',
        price=200,
        description='Записывает звук',
        max_in_game=2,
        image_path='././assets/images/itms/dict.png'
    ),
    'term': ItemData(
        item_id='term',
        name='ТЕРМОМЕТР',
        price=150,
        description='Показывает температуру',
        max_in_game=2,
        image_path='././assets/images/itms/term_norm.png'
    ),
    'flash_light': ItemData(
        item_id='flash_light',
        name='ФОНАРИК',
        price=150,
        description='Дает дополнительный свет',
        max_in_game=4,
        image_path='././assets/images/itms/flash_light.png'
    ),
    'camera': ItemData(
        item_id='camera',
        name='ФОТОКАМЕРА',
        price=300,
        description='Фотографирует призрака',
        max_in_game=4,
        image_path='././assets/images/itms/cam.png'
    ),
    'incense': ItemData(
        item_id='incense',
        name='БЛАГОВОНИЯ',
        price=150,
        description='Отпугивают призрака',
        max_in_game=4,
        image_path='././assets/images/itms/blag.png'
    ),
    'lighter': ItemData(
        item_id='lighter',
        name='ЗАЖИГАЛКА',
        price=50,
        description='Дает зажечь благовония',
        max_in_game=4,
        image_path='././assets/images/itms/light.png'
    ),
    'pills': ItemData(
        item_id='pills',
        name='УСПОКОИТЕЛЬНОЕ',
        price=150,
        description='Приведет в себя',
        max_in_game=4,
        image_path='././assets/images/itms/pills.png'
    )
}


class ItemInfoWidget:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.current_item = None
        self.ui_elements = []

        # Для картинки
        self.image_sprite_list = arcade.SpriteList()
        self.image_sprite = None

    def add_to_manager(self, manager):
        """Добавляем UI элементы в менеджер"""
        # Заголовок
        title = arcade.gui.UILabel(
            text='ИНФОРМАЦИЯ',
            font_name='Courier New',
            font_size=18,
            text_color=arcade.color.WHITE,
            align='center'
        )
        title.center_x = self.x + self.width // 2
        title.top = self.y - 20
        manager.add(title)
        self.ui_elements.append(title)

        # Название предмета
        self.name_label = arcade.gui.UILabel(
            text='',
            font_name='Courier New',
            font_size=20,
            text_color=arcade.color.WHITE,
            align='center',
            width=self.width - 20
        )
        self.name_label.center_x = self.x + self.width // 2
        self.name_label.top = self.y - 170
        manager.add(self.name_label)
        self.ui_elements.append(self.name_label)

        # Цена
        self.price_label = arcade.gui.UILabel(
            text='Цена: ',
            font_name='Courier New',
            font_size=16,
            text_color=arcade.color.WHITE,
            align='left',
            width=self.width - 20
        )
        self.price_label.left = self.x + 10
        self.price_label.top = self.y - 200
        manager.add(self.price_label)
        self.ui_elements.append(self.price_label)

        # Максимум в игру
        self.max_game_label = arcade.gui.UILabel(
            text='В игру: ',
            font_name='Courier New',
            font_size=16,
            text_color=arcade.color.WHITE,
            align='left',
            width=self.width - 20
        )
        self.max_game_label.left = self.x + 10
        self.max_game_label.top = self.y - 230
        manager.add(self.max_game_label)
        self.ui_elements.append(self.max_game_label)

        # В инвентаре
        self.inventory_label = arcade.gui.UILabel(
            text='В инвентаре: ',
            font_name='Courier New',
            font_size=16,
            text_color=arcade.color.WHITE,
            align='left',
            width=self.width - 20
        )
        self.inventory_label.left = self.x + 10
        self.inventory_label.top = self.y - 260
        manager.add(self.inventory_label)
        self.ui_elements.append(self.inventory_label)

        # С собой
        self.taken_label = arcade.gui.UILabel(
            text='С собой: ',
            font_name='Courier New',
            font_size=16,
            text_color=arcade.color.WHITE,
            align='left',
            width=self.width - 20
        )
        self.taken_label.left = self.x + 10
        self.taken_label.top = self.y - 290
        manager.add(self.taken_label)
        self.ui_elements.append(self.taken_label)

        # Описание
        self.desc_label = arcade.gui.UILabel(
            text='',
            font_name='Courier New',
            font_size=12,
            text_color=arcade.color.LIGHT_GRAY,
            align='left',
            width=self.width - 20,
            multiline=True,
            height=60
        )
        self.desc_label.left = self.x + 10
        self.desc_label.top = self.y - 320
        manager.add(self.desc_label)
        self.ui_elements.append(self.desc_label)

    def update_info(self, item_data):
        self.current_item = item_data

        self.image_sprite_list.clear()
        self.image_sprite = None

        if not item_data:
            self.name_label.text = 'ВЫБЕРИТЕ ТОВАР'
            self.price_label.text = 'Цена: '
            self.max_game_label.text = 'В игру: '
            self.inventory_label.text = 'В инвентаре: '
            self.taken_label.text = 'С собой: '
            self.desc_label.text = ''
            return

        # Обновляем текстовые поля
        self.name_label.text = item_data.name
        self.price_label.text = f'Цена: {item_data.price}$'
        self.max_game_label.text = f'В игру: {item_data.max_in_game}'
        self.inventory_label.text = f'В инвентаре: {item_data.in_inventory}'
        self.taken_label.text = f'С собой: {item_data.selected}'
        self.desc_label.text = item_data.description

        # Загружаем картинку в спрайт
        image_path = getattr(item_data, 'images_path', None) or getattr(item_data, 'image_path', None)

        if search(r'light.png', image_path):
            self.image_sprite = arcade.Sprite(image_path, scale=3.0)
        elif search(r'blag.png', image_path):
            self.image_sprite = arcade.Sprite(image_path, scale=1.7)
        else:
            self.image_sprite = arcade.Sprite(image_path, scale=5.0)

        self.image_sprite.center_x = self.x + self.width // 2
        self.image_sprite.center_y = self.y - 90

        self.image_sprite_list.append(self.image_sprite)

    def draw_background(self):
        """Рисуем фон (картинка рисуется отдельно)"""
        arcade.draw_lrbt_rectangle_filled(
            left=self.x,
            right=self.x + self.width,
            bottom=self.y - self.height - 40,
            top=self.y - 10,
            color=(30, 30, 30)
        )

    def draw_image(self):
        """Рисуем картинку предмета"""
        if self.image_sprite_list:
            self.image_sprite_list.draw()
