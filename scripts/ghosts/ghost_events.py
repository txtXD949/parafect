import random
import arcade

from ..sounds import *


class GhostEvent:
    """Класс гост-ивента"""

    def __init__(self, timer, sound, ghost):
        self.ghost = ghost

        # Параметры гост-ивента
        self.ge_timer = timer
        self.timer = self.ge_timer
        self.sound = sound
        self.is_ge = False

        self.is_played = False

    def do_ghost_event(self, player_x, player_y, color=(230, 255)):
        """Начинает гост-ивент"""
        if self.is_ge:
            c = random.randint(*color)
            self.ghost.sprite.color = (c, c, c)
            if not self.is_played:
                from ..views import SettingsManager
                volume_ghost = SettingsManager.get_ghost_sound_volume()
                volume_heartbeat = SettingsManager.get_sound_volume()

                self.ghost.sound_player_g = arcade.play_sound(self.sound, volume=volume_ghost)
                self.ghost.sound_player_h = arcade.play_sound(HEARTBEAT, volume=volume_heartbeat, loop=True)

                self.is_played = True
            if self.timer <= 0:
                self.ghost.game.player.sanity = max(0, self.ghost.game.player.sanity - self.ghost.drop_sanity)
                self.is_ge = False
                self.ghost.sprite.visible = False
                self.ghost.sprite.color = (255, 255, 255, 255)
                self.ghost.ghost_event = None
                self.ghost.sound_player_h.pause()
            return
        if random.random() <= self.ghost.ghost_event_chance:
            self.timer = self.ge_timer
            self.ghost.sprite.center_x = player_x + random.uniform(-5.0, 5.0)
            self.ghost.sprite.center_y = player_y + random.uniform(-5.0, 5.0)
            self.is_ge = True
            self.ghost.sprite.visible = True
            self.is_played = False


class SuddenGhostEvent(GhostEvent):
    """Внезапный гост-ивент"""
    SOUNDS = [
        SUDDEN_GHOST_EVENT_1,
        SUDDEN_GHOST_EVENT_2,
        SUDDEN_GHOST_EVENT_3
    ]

    def __init__(self, ghost):
        super().__init__(timer=6.0, sound=random.choice(self.SOUNDS), ghost=ghost)

    def do_ghost_event(self, player_x, player_y, color=None):
        super().do_ghost_event(player_x, player_y)

        if self.is_ge and not self.is_played:
            self.ghost.game.map.camera_shake.start()


class BreathGhostEvent(GhostEvent):
    """Дышащий гост-ивент"""
    SOUNDS = [
        BREATH_GHOST_EVENT_1,
        BREATH_GHOST_EVENT_2
    ]

    def __init__(self, ghost):
        super().__init__(timer=8.5, sound=random.choice(self.SOUNDS), ghost=ghost)


class WheezingGhostEvent(GhostEvent):
    """Хрипящий гост ивент"""
    SOUNDS = [
        WHEEZING_GHOST_EVENT_1,
        WHEEZING_GHOST_EVENT_2,
        WHEEZING_GHOST_EVENT_3,
        WHEEZING_GHOST_EVENT_4
    ]

    def __init__(self, ghost):
        super().__init__(timer=5.5, sound=random.choice(self.SOUNDS), ghost=ghost)


class WheezingGhostEvenShadow(GhostEvent):
    """Хрипящий теневой гост-ивент"""
    SOUNDS = [
        WHEEZING_SHADOW_EVENT_1,
        WHEEZING_SHADOW_EVENT_2,
        WHEEZING_SHADOW_EVENT_3,
        WHEEZING_SHADOW_EVENT_4,
        WHEEZING_SHADOW_EVENT_5
    ]

    def __init__(self, ghost):
        super().__init__(timer=4.5, sound=random.choice(self.SOUNDS), ghost=ghost)

    def do_ghost_event(self, player_x, player_y, color=None):
        super().do_ghost_event(player_x, player_y, (0, 40))


class WhisperGhostEvent(GhostEvent):
    """Шепчущий гост-ивент"""
    SOUNDS = [
        WHISPER_GHOST_EVENT_1,
        WHISPER_GHOST_EVENT_2
    ]

    def __init__(self, ghost):
        super().__init__(timer=6.0, sound=random.choice(self.SOUNDS), ghost=ghost)


class LaughGhostEvent(GhostEvent):
    """Смеющийся гост-ивент"""
    SOUNDS = [
        LAUGH_GHOST_EVENT
    ]

    def __init__(self, ghost):
        super().__init__(timer=2.7, sound=random.choice(self.SOUNDS), ghost=ghost)


# Гост-ивенты
GHOST_EVENTS = [
    SuddenGhostEvent, BreathGhostEvent,
    WheezingGhostEvent, WheezingGhostEvenShadow,
    WhisperGhostEvent, LaughGhostEvent
]
