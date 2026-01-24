import random
import arcade

from .ghosts import GHOSTS


class Game:
    def __init__(self, player, map_id='test', difficulty_id='test', inventory=None, profile=None, account=None, window=None):
        self.player = player
        self.profile = profile
        self.account = account
        self.player_name = player.name
        self.map_id = map_id
        self.dif_id = difficulty_id
        self.inv = inventory
        self.ghost = random.choice(GHOSTS)()

        self.map = None

        self.dif = None
        self.sanity = None
        self.broke_chance = None
        self.roomchange_chance = None
        self.roomchange_chance = None
        self.evidence_count = None

        self.window = window

        self.choose_difficult(difficulty_id)
        self.choose_map(map_id)

        # Конец игры
        self.is_win = None
        self.was_death = None
        self.was_hunt = None
        self.was_zero_sanity = None
        self.was_first_death = None

    def choose_difficult(self, dif_id):
        from .views import DIFFICULTY_DATABASE

        self.dif = DIFFICULTY_DATABASE[dif_id]

        self.sanity = int(self.dif.sanity[:-1])
        self.add_sanity = int(self.dif.add_sanity[:-1])
        self.broke_chance = int(self.dif.broke_chance[:-1]) / 100_000
        self.roomchange_chance = int(self.dif.roomchange_chance[:-1]) / 100_000
        self.evidence_count = int(self.dif.evidence_count)

    def choose_map(self, map_id):
        from .maps.test_map import TestMap
        maps = {
            'dom_1': ...,
            'dom_3': ...,
            'kv_no96': ...,
            'caffe': ...,
            'school': ...,
            'bunker': ...,
            'test': TestMap
        }
        self.map = maps[map_id](self)

    def open_map(self):
        self.window.show_view(self.map)
