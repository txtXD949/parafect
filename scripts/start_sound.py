import arcade
from scripts.sounds import ENTRY_BACKGROUND
from scripts.views.settings import SettingsManager

volume = SettingsManager.get_sound_volume()
ENTRY_BACKGROUND_SOUND = arcade.play_sound(ENTRY_BACKGROUND, loop=True, volume=volume)
ENTRY_BACKGROUND_SOUND.pause()
