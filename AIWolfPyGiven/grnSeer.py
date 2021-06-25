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
        self.divs = [] # [ [who, species] ], by day where first is day 0, may not need this
        self.meSet = {self.idx}
        self.certain_ww_aligned = set() # others who CO seer that is not me etc
        self.fake_seers = set() # others who CO as seer that is not me
        self.divWW = set()
        self.divHU = set()
        self.all_divs = set()
        self.divined_WW_day_0 = False
        self.daily_push_vote = 0
        self.daily_div_claim = False
        self.div_WW_today = False
    def update(self, base_info, diff_data, request):
        super().update(base_info, diff_data, request)

        # catergorize / group fakes 
        for poser in self.seers:
            if poser != self.idx:
                self.fake_seers.add(poser)
                self.certain_ww_aligned.add(poser)
            

        # parse diff_data for divs
        if request == 'DAILY_INITIALIZE':
            for row in diff_data.itertuples():
                type = getattr(row,"type")
                text = getattr(row,"text")
                # adding to sets based on divs
                if type == 'divine':
                    if text[18:] == 'HUMAN':
                        self.divHU.add( int(getattr(row, 'agent')) )
                    else:
                        self.divWW.add( int(getattr(row, 'agent')) )
        
        self.all_divs = self.divHU.union(self.divWW)
        print('seer div all:')
        print(self.all_divs)
        print('seer div HUs:')
        print(self.divHU)
        print('seer div WWs:')
        print(self.divWW)
        
        
    def dayStart(self):
        super().dayStart()
        self.daily_push_vote = 0
        self.daily_div_claim = False
        self.div_WW_today = False
        return None

    def talk(self):
        #super().talk()

        # day 1 logic
        if self.currentDay == 1:
            # always CO as seer
            if not self.hasCO:
                self.hasCO = True
                return cb.comingout(self.idx, self.idx, 'SEER')
            if len(self.divHU) != 0 and not self.daily_div_claim: # div HU day 0, report
                self.daily_div_claim = True
                return cb.divined(self.idx, list(self.divHU)[0], 'HUMAN')
            else: # if div WW then skip
                self.divined_WW_day_0 = True
                return cb.skip()

        # day 2 logic
        elif self.currentDay == 2:
            if not ( self.daily_div_claim ) and ( self.divined_WW_day_0 or len(self.divWW) != 0 ):
                print('DAY 2 REACHED')
                self.div_WW_today = True
                self.daily_div_claim = True
                return cb.divined(self.idx, list(self.divWW)[0], 'WEREWOLF')
            elif not ( self.divined_WW_day_0 and self.daily_div_claim ):
                self.daily_div_claim = True
                return cb.divined(self.idx, list(self.divHU)[0], 'HUMAN') # div 2 WW in day 0 and 1; this is from day 0
            elif self.daily_div_claim and self.daily_push_vote < 2 and self.div_WW_today:
                 # print("#################### VOTE CLAIM")
                self.daily_push_vote += 1
                return cb.vote(self.idx, list(self.divWW)[0])
            elif self.daily_push_vote == 2:
                return cb.skip()
            else:
                return cb.over()
        else: 
            return cb.over()
        

    def vote(self):
        return super().vote()

    def divine(self):
        # div rand on day 0

        if self.currentDay == -1: # needs work
            return 2
        elif True: 
            return random.choice( list( self.alive.difference(self.meSet).difference(self.all_divs) ) )

        # on day 1 and on there is no need to div copy seers / mediums as we know they are evil

    def finish(self):
        return super().finish(self)
