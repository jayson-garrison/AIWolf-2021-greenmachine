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

    def initialize(self, base_info, diff_data, game_setting): # new variables
        super().initialize(base_info, diff_data, game_setting)
        self.WWs = set()
        self.medium_target = set()
        self.seer_target = set()
        self.bodyguard_target = set()
        self.nthWhisper = -1

    def update(self, base_info, diff_data, request):
        super().update(base_info, diff_data, request)

        # 

    def dayStart(self):
        pass

    def talk(self): # new
        return "Over"

    def vote(self): # new
        return 1

    def divine(self):
        pass

    def guard(self):
        return 1

    def whisper(self): # new
        return "Over"

    def attack(self): # new
        pass

    def finish(self):
        super().finish()
