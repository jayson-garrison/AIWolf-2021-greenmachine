"""
    Contains Werewolf Class
    James Hale
"""
import aiwolfpy
from aiwolfpy import contentbuilder as cb
import grnVillager

class Werewolf(grnVillager.Villager):
    def __init__(self, my_name):
        super().__init__(my_name)

    def initialize(self, base_info, diff_data, game_setting):
        super().initialize(base_info, diff_data, game_setting)

    def update(self, base_info, diff_data, request):
        pass

    def dayStart(self):
        pass

    def talk(self):
        return "Over"

    def vote(self):
        return 1

    def divine(self):
        pass

    def guard(self):
        return 1

    def whisper(self):
        return "Over"

    def attack(self):
        pass

    def finish(self):
        pass
