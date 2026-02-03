#  Запуск программы отсюда
import arcade
import os
import pyglet.image


class GameWindow(arcade.Window):
    """Главный класс игры"""

    def __init__(self):
        super().__init__(
            title='Parafect',
            fullscreen=True
        )

        # Иконка
        self.set_icon(pyglet.image.load('./assets/images/icons/parafect.ico'))

        self.center_window()

    def on_close(self):
        # Удаляем файл временного инвентаря при закрытии окна
        game_state_file = '././database/_game.json'
        if os.path.exists(game_state_file):
            os.remove(game_state_file)

        super().on_close()


def main():
    window = GameWindow()

    # Подгружаем настройки
    from scripts.views import SettingsManager
    SettingsManager.load()

    # Начальный экран
    from scripts.views import Screensaver
    screensaver = Screensaver()
    window.show_view(screensaver)

    # Запуск
    arcade.run()


if __name__ == '__main__':
    main()
