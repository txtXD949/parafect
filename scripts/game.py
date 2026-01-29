import random
import arcade

from .ghosts import GHOSTS


class Game:
    def __init__(self, player, map_id='test', difficulty_id='test', inventory=None, profile=None, account=None,
                 window=None):
        self.player = player
        self.profile = profile
        self.account = account
        self.player_name = player.name
        self.map_id = map_id
        self.dif_id = difficulty_id
        self.inv = inventory
        self.ghost = random.choice(GHOSTS)()

        self.evidences = self.ghost.evidences[:]

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
        self.is_win = False
        self.was_death = False
        self.was_hunt = False
        self.was_zero_sanity = False
        self.was_first_death = False

    def choose_difficult(self, dif_id):
        from .views import DIFFICULTY_DATABASE

        self.dif = DIFFICULTY_DATABASE[dif_id]

        self.sanity = int(self.dif.sanity[:-1])
        self.add_sanity = int(self.dif.add_sanity[:-1])
        self.broke_chance = int(self.dif.broke_chance[:-1]) / 100_000
        self.roomchange_chance = int(self.dif.roomchange_chance[:-1]) / 100_000
        self.evidence_count = int(self.dif.evidence_count)

        if self.evidence_count < 3:
            self.remove_evidences()

    def remove_evidences(self):
        new_evidences = []
        if self.evidence_count in (1, 2):
            c = self.evidence_count
            if self.ghost.main_evidence and c:
                new_evidences.append(self.ghost.main_evidence)
                self.evidences.remove(self.ghost.main_evidence)
                c -= 1
            for i in range(c):
                new_evidences.append(random.choice(self.evidences))

        self.evidences = new_evidences

    def choose_map(self, map_id):
        from .maps.test_map import TestMap
        from .maps import Dom1
        from .maps import Dom3
        from .maps import Kv96
        maps = {
            'dom_1': Dom1,
            'dom_3': Dom3,
            'kv_no96': Kv96,
            'caffe': ...,
            'school': ...,
            'bunker': ...,
            'test': TestMap
        }
        self.map = maps[map_id](self)

    def open_map(self):
        self.window.show_view(self.map)
