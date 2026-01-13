#  Запуск программы отсюда
from scripts.views import Screensaver
from scripts.views import LoginMenu
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


fill_cell()

while free_from_up():
    move_up()

while free_from_left():
    move_left()

while True:
    while free_from_down():
        move_down()
        fill_cell()

    if not free_from_right():
        break

    move_right()
    fill_cell()

    while free_from_up():
        move_up()
        fill_cell()

    if not free_from_right():
        break

    move_right()
    fill_cell()


