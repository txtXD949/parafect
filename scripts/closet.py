import arcade

class ClosetSprite(arcade.Sprite):
    def __init__(self, position, texture):
        self.position = position
        self.texture = texture

        self.player_in = None

    def interact(self, ):