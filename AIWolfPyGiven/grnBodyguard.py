"""
    Contains Body Guard Class
    James Hale
"""
import aiwolfpy
from aiwolfpy import contentbuilder as cb
import random
import grnVillager

class BodyGuard(grnVillager.Villager):
    def __init__(self, my_name):
        super().__init__(my_name)
        
    def initialize(self, base_info, diff_data, game_setting):
        super().initialize(base_info, diff_data, game_setting)

    def update(self, base_info, diff_data, request):
        super().update(base_info, diff_data, request)

    def dayStart(self):
        super().dayStart()

    def talk(self):
        return super().talk()

    def vote(self):
        return 1

    def divine(self):
        pass

    def guard(self):
        if self.mediums.keys():
            return int(random.choice(list(self.mediums.keys())))
        return int(random.sample(self.alive, 1)[0])

    def whisper(self):
        return "Over"

    def attack(self):
        pass

    def finish(self):
        pass
