"""
    Contains Posessed Class
    James Hale
    Grey Bodi
"""
import aiwolfpy
from aiwolfpy import contentbuilder as cb
import grnVillager

class Possessed(grnVillager.Villager):
    def __init__(self, my_name):
        super().__init__(my_name)
        self.name = my_name

    def initialize(self, base_info, diff_data, game_setting):
        super().initialize(base_info, diff_data, game_setting)

    def update(self, base_info, diff_data, request):
        super().update(base_info, diff_data, request)

    def dayStart(self):
        super().dayStart()

    def talk(self):
        super().talk()

    def vote(self):
        return 1


    def finish(self):
        super().finish()
