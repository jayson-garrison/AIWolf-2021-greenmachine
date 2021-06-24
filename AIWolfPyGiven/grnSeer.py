"""
    Contains Seer Class
    Jayson C. Garrison
"""
import aiwolfpy
from aiwolfpy import contentbuilder as cb
import grnVillager
import logging, json
import random

class Seer(grnVillager.Villager):
    def __init__(self, my_name):
        super().__init__(my_name)

    def initialize(self, base_info, diff_data, game_setting):
        super().initialize(base_info, diff_data, game_setting)
        self.divs = [] # [ [who, species] ], by day where first is day 0
        self.meSet = {self.idx}
    def update(self, base_info, diff_data, request):
        super().update(base_info, diff_data, request)

        # parse diff_data for divs
        # group fakes
        
    def dayStart(self):
        super().dayStart()
        return None

    def talk(self):
        #super().talk()
        if self.currentDay == 1:
            if not self.hasCO:
                self.hasCO = True
                return cb.comingout(self.idx, self.idx, 'SEER')
            #if self.divs[0][1] == 'HUMAN':
                #return cb.divined(self.idx, self.divs[0], 'HUMAN')
            else:
                return cb.skip()
        else: return cb.over()
        

    def vote(self):
        return super().vote()

    def divine(self):
        # div rand on day 0
        if self.currentDay == 0:
            investigate = random.randint(1,15)
            return investigate
        else: return 1

        # on day 1 and on there is no need to div copy seers / mediums as we know they are evil

    def finish(self):
        return super().finish(self)
