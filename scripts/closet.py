import arcade

class ClosetSprite(arcade.Sprite):
    def __init__(self, position, texture):
        super().__init__()
        self.position = position
        self.texture_base = texture
        self.texture_broken = arcade.load_texture("./assets/sprites_2/pngs/closet_broken.png")

        self.texture = self.texture_base
        self.player_sprite = None

        self.is_player_in = False
        self.is_broken = False

    def interact(self, player_sprite):
        if self.is_broken:
            return

        if self.player_sprite == player_sprite:
            self.player_sprite.visible = True
            self.player_sprite.speed_scale = 1
            self.player_sprite = None

        elif self.player_sprite is None:
            self.player_sprite = player_sprite
            self.player_sprite.visible = False
            self.player_sprite.speed_scale = 0

        return

    def broke(self):
        if self.player_sprite:
            self.player_sprite.visible = True
            self.player_sprite.speed_scale = 1
            self.player_sprite = None

        self.is_broken = True
        self.texture = self.texture_broken

