"""
    Contains Seer Class
    Jayson C. Garrison
"""
import aiwolfpy
from aiwolfpy import contentbuilder as cb
import grnVillager

class Seer(grnVillager.Villager):
    def __init__(self, my_name):
        self.name = my_name

    def initialize(self, base_info, diff_data, game_setting):
        super().initialize(base_info, diff_data, game_setting)

    def update(self, base_info, diff_data, request):
        super().update(base_info, diff_data, request)

    def dayStart(self):
        super().dayStart()
        return None

    def talk(self):
        super().talk()

    def vote(self):
        super().vote()

    def divine(self):
        return 1

    def guard(self):
        return 1

    def whisper(self):
        return "Over"

    def attack(self):
        pass

    def finish(self):
        super().finish(self)
