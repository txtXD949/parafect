#  Запуск программы отсюда
from scripts.views import Screensaver
from scripts.views import MarketView


def main():
    import arcade
    window = arcade.Window(title='Parafect', center_window=True)
    window.set_fullscreen(True)

    # screensaver = Screensaver()
    # window.show_view(screensaver)

    market = MarketView()
    window.show_view(market)

    arcade.run()


if __name__ == '__main__':
    main()
