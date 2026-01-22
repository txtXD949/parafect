#  Запуск программы отсюда
from scripts.views import Screensaver
from scripts.views import LoginMenu
from scripts.views import GameLoading
import arcade
import os


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(
            title='Parafect',
            fullscreen=True
        )

        self.center_window()

    def on_close(self):
        game_state_file = '././database/_game.json'
        if os.path.exists(game_state_file):
            os.remove(game_state_file)

        super().on_close()


def main():
    window = GameWindow()

    screensaver = Screensaver()
    window.show_view(screensaver)

    # login = LoginMenu(None)
    # window.show_view(login)

    arcade.run()


if __name__ == '__main__':
    main()

# TODO: Сделать настройки
