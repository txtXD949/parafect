#  Запуск программы отсюда
from scripts.views import Screensaver
from scripts.views import LobbyView


def main():
    import arcade
    window = arcade.Window(title='Parafect', center_window=True)
    window.set_fullscreen(True)

    # screensaver = Screensaver()
    # window.show_view(screensaver)

    lobby = LobbyView()
    window.show_view(lobby)

    arcade.run()


if __name__ == '__main__':
    main()
