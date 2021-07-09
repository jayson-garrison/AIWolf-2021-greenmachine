"""
    Contains Body Guard Class
    07/'21
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
        return super().dayStart()

    def talk(self):
        return super().talk()

    def vote(self):
        return super.vote()

    def divine(self):
        return super.divine()

    def guard(self):
        if self.mediums.keys():
            return int(random.choice(list(self.mediums.keys())))
        return int(random.sample(self.alive, 1)[0])

    def whisper(self):
        return super().whisper()

    def attack(self):
        return super().attack()

    def finish(self):
        return super().finish()

