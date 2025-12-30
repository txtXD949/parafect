#  Запуск программы отсюда
from scripts.views import Screensaver

# TODO: сделать спрайт таблеток

def main():
    import arcade
    window = arcade.Window(title='Parafect')
    window.set_fullscreen(True)

    screensaver = Screensaver()
    window.show_view(screensaver)

    arcade.run()


if __name__ == '__main__':
    main()
