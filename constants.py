import arcade

ENTRY_BACKGROUND_SOUND = arcade.play_sound(arcade.load_sound('././assets/sounds/background/login.mp3'), loop=True,
                                           volume=0.2)
ENTRY_BACKGROUND_SOUND.pause()

MASTER_VOLUME = 1.0
GHOST_VOLUME = 1.0
LANGUAGES = ['ru', 'en']
LANGUAGE_INDEX = 0
