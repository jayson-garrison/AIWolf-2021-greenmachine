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
        self.current_div_as_WW = set()
        self.current_div_as_HU = set()
        self.targets = set()
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
                        self.current_div_as_HU.add( int(getattr(row, 'agent')) )
                    else:
                        self.divWW.add( int(getattr(row, 'agent')) )
                        self.current_div_as_WW.add( int(getattr(row, 'agent')) )
        
        self.all_divs = self.divHU.union(self.divWW)
        print('seer div all:')
        print(self.all_divs)
        print('seer div HUs:')
        print(self.divHU)
        print('seer div WWs:')
        print(self.divWW)
        
        # update targets
        self.targets = self.divWW.copy()
        self.targets = self.targets.intersection(self.alive)
        print('TARGETS TO VOTE )))))))))))))))))))')
        print(self.targets)
        print('CURRENT DIV HU:')
        print(self.current_div_as_HU)
        print('CURRENT DIV WW:')
        print(self.current_div_as_WW)
        
    def dayStart(self):
        super().dayStart()
        self.daily_push_vote = 0
        self.daily_div_claim = False
        self.div_WW_today = False
        #self.current_div_as_HU = set()
        #self.current_div_as_WW = set()
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
            elif len(self.divWW) != 0: # if div WW then skip
                self.divined_WW_day_0 = True
                print("DIV WW 0 TRUE")
                return cb.skip()
            else:
                return cb.over()

        # day 2 logic
        elif self.currentDay == 2:
            print('DAY 2 REACHED')
            if not self.daily_div_claim and ( self.divined_WW_day_0 or len(self.divWW) != 0 ):
                print('CASE 1 REACHED: DIV WW DAY 0/1 - REPORT')
                self.div_WW_today = True
                self.daily_div_claim = True
                return cb.divined(self.idx, list(self.divWW)[0], 'WEREWOLF')
            elif not ( self.daily_div_claim ): # self.divined_WW_day_0 and 
                print('CASE 2 REACHED: DIV ONLY HUs REPORT ONE')
                self.daily_div_claim = True
                return cb.divined(self.idx, list(self.divHU)[0], 'HUMAN') # div 2 WW in day 0 and 1; this is from day 0
            elif self.daily_div_claim and self.daily_push_vote < 2 and self.div_WW_today:
                print('CASE 3 REACHED: PUSH VOTE WW DIV')
                 # print("#################### VOTE CLAIM")
                self.daily_push_vote += 1
                return cb.vote(self.idx, list(self.divWW)[0])
            elif self.daily_push_vote == 2:
                print('CASE 4 REACHED: SKIP AFTER PUSH VOTE')
                return cb.skip()
            else:
                return cb.over()
        elif self.currentDay > 2:
            print('N DAY REACHED')
            if len(self.current_div_as_WW) != 0:
                print('CURRENT DIV WW')
                werewolf = self.current_div_as_WW.pop() 
                self.current_div_as_WW.add(werewolf)
                if not self.daily_div_claim:
                    self.daily_div_claim = True
                    return cb.divined(self.idx, werewolf, 'WEREWOLF')
                elif self.daily_div_claim and self.daily_push_vote < 2:
                    print('VOTE DIV WW')
                    self.daily_push_vote += 1
                    return cb.vote(self.idx, werewolf)
                elif self.daily_push_vote == 2:
                    self.daily_push_vote += 1
                    print('VOTE TARG FIN')
                    return cb.vote( self.idx, list(self.targets)[0] )
                else:
                    print('CASE X DONE')
                    self.current_div_as_WW.clear()
                    return cb.skip()
                    
            elif len(self.current_div_as_HU) != 0:
                print('CURRENT DIV HU') 
                human = self.current_div_as_HU.pop()
                self.current_div_as_HU.add(human)
                if not self.daily_div_claim:
                    self.daily_div_claim = True
                    return cb.divined(self.idx, human, 'HUMAN')
                elif len(self.targets) != 0 and self.daily_push_vote < 2:
                    print('VOTE TARGS')
                    self.daily_push_vote += 1
                    return cb.vote(self.idx, list(self.targets)[0] )
                else:
                    print('CASE Y DONE')
                    self.current_div_as_HU.clear()
                    return cb.skip()
            else:
                return cb.over()
        else: 
            return cb.over()
        

    def vote(self):
        if self.currentDay < 2:
            return super().vote()
        else:
            return self.targets[0]

    def divine(self):
        # div rand on day 0

        if self.currentDay == -1: # needs work
            return 2
        elif True: 
            return random.choice( list( self.alive.difference(self.meSet).difference(self.all_divs) ) )

        # on day 1 and on there is no need to div copy seers / mediums as we know they are evil

    def finish(self):
        return super().finish(self)
