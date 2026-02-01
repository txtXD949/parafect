import arcade


class DoorSprite(arcade.Sprite):
    def __init__(self, position, collitions, texture):
        super().__init__()
        self.closed = True
        self.is_blocked = False
        self.collitions = collitions
        self.position = position
        self.texture_closed = texture
        self.texture_opened = arcade.load_texture("./assets/sprites_2/pngs/door_opened.png")
        self.texture = texture
        self.clone_for_hitbox = arcade.Sprite(texture, scale=0.8)
        self.clone_for_hitbox.position = self.position
        collitions.append(self.clone_for_hitbox)

    def change(self):
        """Открытие/закрытие двери"""
        if self.is_blocked:
            return

        if self.closed:
            self.closed = False
            self.collitions.remove(self.clone_for_hitbox)
            self.texture = self.texture_opened
        else:
            self.closed = True
            self.collitions.append(self.clone_for_hitbox)
            self.texture = self.texture_closed

    def block(self):
        self.is_blocked = True

    def unblock(self):
        self.is_blocked = False
