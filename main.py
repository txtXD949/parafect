#  Запуск программы отсюда
import arcade
import os
import pyglet.image


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(
            title='Parafect',
            fullscreen=True
        )

        self.set_icon(pyglet.image.load('./assets/images/icons/parafect.ico'))

        self.center_window()

    def on_close(self):
        game_state_file = '././database/_game.json'
        if os.path.exists(game_state_file):
            os.remove(game_state_file)

        super().on_close()


def main():
    window = GameWindow()

    from scripts.views import SettingsManager
    SettingsManager.load()

    from scripts.views import Screensaver
    screensaver = Screensaver()
    window.show_view(screensaver)

    arcade.run()


if __name__ == '__main__':
    main()
