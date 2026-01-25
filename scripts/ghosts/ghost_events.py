import random
import arcade


class GhostEvent:
    def __init__(self, timer, sound, ghost):
        self.ghost = ghost

        self.ge_timer = timer
        self.timer = self.ge_timer
        self.sound = sound
        self.is_ge = False

        self.is_played = False

    def do_ghost_event(self, player_x, player_y):
        if self.is_ge:
            color = random.randint(230, 255)
            self.ghost.sprite.color = (color, color, color)
            if not self.is_played:
                self.ghost.sound_player_g = arcade.play_sound(self.sound)
                self.ghost.sound_player_h = arcade.play_sound(arcade.load_sound('././assets/sounds/effects/heartbeat.wav'), loop=True)
                self.is_played = True
            if self.timer <= 0:
                self.ghost.game.player.sanity -= self.ghost.drop_sanity
                self.is_ge = False
                self.ghost.sprite.visible = False
                self.ghost.sprite.color = (255, 255, 255, 255)
                self.ghost.sprite.ghost_event = None
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
    SOUNDS = [
        arcade.load_sound('././assets/sounds/effects/sudden_ghost_event1.wav'),
        arcade.load_sound('././assets/sounds/effects/sudden_ghost_event2.wav'),
        arcade.load_sound('././assets/sounds/effects/sudden_ghost_event3.wav')
    ]

    def __init__(self, ghost):
        super().__init__(timer=6.0, sound=random.choice(self.SOUNDS), ghost=ghost)

    def do_ghost_event(self, player_x, player_y):
        super().do_ghost_event(player_x, player_y)

        if self.is_ge and not self.is_played:
            self.ghost.game.map.camera_shake.start()



class BreathGhostEvent(GhostEvent):
    SOUNDS = [
        arcade.load_sound('././assets/sounds/effects/breath_ghost_event1.wav'),
        arcade.load_sound('././assets/sounds/effects/breath_ghost_event2.wav')
    ]

    def __init__(self, ghost):
        super().__init__(timer=8.5, sound=random.choice(self.SOUNDS), ghost=ghost)


class WheezingGhostEvent(GhostEvent):
    SOUNDS = [
        arcade.load_sound('././assets/sounds/effects/wheezing_ghost_event1.wav'),
        arcade.load_sound('././assets/sounds/effects/wheezing_ghost_event2.wav'),
        arcade.load_sound('././assets/sounds/effects/wheezing_ghost_event3.wav'),
        arcade.load_sound('././assets/sounds/effects/wheezing_ghost_event4.wav')
    ]

    def __init__(self, ghost):
        super().__init__(timer=5.5, sound=random.choice(self.SOUNDS), ghost=ghost)


class WheezingGhostEvenShadow(GhostEvent):
    SOUNDS = [
        arcade.load_sound('././assets/sounds/effects/wheezing_shadow_ghost_event1.wav'),
        arcade.load_sound('././assets/sounds/effects/wheezing_shadow_ghost_event2.wav'),
        arcade.load_sound('././assets/sounds/effects/wheezing_shadow_ghost_event3.wav'),
        arcade.load_sound('././assets/sounds/effects/wheezing_shadow_ghost_event4.wav'),
        arcade.load_sound('././assets/sounds/effects/wheezing_shadow_ghost_event5.wav')
    ]

    def __init__(self, ghost):
        super().__init__(timer=4.5, sound=random.choice(self.SOUNDS), ghost=ghost)

    def do_ghost_event(self, player_x, player_y):
        if self.is_ge:
            color = random.randint(0, 40)
            self.ghost.sprite.color = (color, color, color)
            if not self.is_played:
                self.ghost.sound_player = arcade.play_sound(self.sound)
                self.is_played = True
            if self.timer <= 0:
                self.ghost.game.player.sanity -= self.ghost.drop_sanity
                self.is_ge = False
                self.ghost.sprite.visible = False
                self.ghost.sprite.color = (255, 255, 255, 255)
                self.ghost.sprite.ghost_event = None
            return
        if random.random() <= self.ghost.ghost_event_chance:
            self.timer = self.ge_timer
            self.ghost.sprite.center_x = player_x + random.uniform(-5.0, 5.0)
            self.ghost.sprite.center_y = player_y + random.uniform(-5.0, 5.0)
            self.is_ge = True
            self.ghost.sprite.visible = True
            self.is_played = False


class WhisperGhostEvent(GhostEvent):
    SOUNDS = [
        arcade.load_sound('././assets/sounds/effects/whisper_ghost_event1.wav'),
        arcade.load_sound('././assets/sounds/effects/whisper_ghost_event2.wav')
    ]

    def __init__(self, ghost):
        super().__init__(timer=6.0, sound=random.choice(self.SOUNDS), ghost=ghost)


class LaughGhostEvent(GhostEvent):
    SOUNDS = [
        arcade.load_sound('././assets/sounds/effects/laugh_ghost_event.wav')
    ]

    def __init__(self, ghost):
        super().__init__(timer=2.7, sound=random.choice(self.SOUNDS), ghost=ghost)


GHOST_EVENTS = [
    SuddenGhostEvent, BreathGhostEvent, WheezingGhostEvent, WheezingGhostEvenShadow, WhisperGhostEvent, LaughGhostEvent
]
