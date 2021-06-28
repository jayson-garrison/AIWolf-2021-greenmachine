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
        self.accuse = 0
    def update(self, base_info, diff_data, request):
        super().update(base_info, diff_data, request)

        # catergorize / group fakes 
        for poser in self.seers:
            if poser[0] != self.idx:
                self.fake_seers.add(poser[0])
                self.certain_ww_aligned.add(poser[0])
            

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
        self.accuse = 0
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
            # div HU day 0, report
            if len(self.divHU) != 0 and not self.daily_div_claim: 
                self.daily_div_claim = True
                return cb.divined(self.idx, list(self.divHU)[0], 'HUMAN')
            # if div WW then skip
            elif len(self.divWW) != 0: 
                self.divined_WW_day_0 = True
                print("DIV WW 0 TRUE")
                return cb.skip()
            elif len(self.certain_ww_aligned) != 0 and self.accuse < 1:
                self.accuse += 1
                return cb.logicalor(self.idx, cb.estimate(self.idx, list(self.certain_ww_aligned)[0], 'POSSESSED'), cb.estimate(self.idx, list(self.certain_ww_aligned)[0], 'WEREWOLF'))
            elif self.accuse < 2:
                self.accuse += 1
                return cb.because(self.idx, cb.comingout(self.idx, self.idx, 'SEER'), cb.comingout(self.idx,list(self.certain_ww_aligned)[0], 'SEER' ))
            else:
                return cb.over()

        # day 2 logic
        elif self.currentDay == 2:
            print('DAY 2 REACHED')
            # case 1, div ww day 0/1
            if not self.daily_div_claim and ( self.divined_WW_day_0 or len(self.divWW) != 0 ):
                # print('CASE 1 REACHED: DIV WW DAY 0/1 - REPORT')
                self.div_WW_today = True
                self.daily_div_claim = True
                return cb.divined(self.idx, list(self.divWW)[0], 'WEREWOLF')
            # case 2 div hu
            elif not ( self.daily_div_claim ): # self.divined_WW_day_0 and 
                # print('CASE 2 REACHED: DIV ONLY HUs REPORT ONE')
                self.daily_div_claim = True
                return cb.divined(self.idx, list(self.divHU)[0], 'HUMAN') # div 2 WW in day 0 and 1; this is from day 0
            # cont case 1, push vote WW
            elif self.daily_div_claim and self.daily_push_vote < 2 and self.div_WW_today:
                # print('CASE 3 REACHED: PUSH VOTE WW DIV')
                # print("#################### VOTE CLAIM")
                self.daily_push_vote += 1
                return cb.vote(self.idx, list(self.divWW)[0])
            elif self.daily_push_vote == 2:
                # print('CASE 4 REACHED: SKIP AFTER PUSH VOTE')
                return cb.skip()
            # accuse other fake seers
            elif len(self.certain_ww_aligned) != 0 and self.accuse < 1:
                self.accuse += 1
                return cb.logicalor(self.idx, cb.estimate(self.idx, list(self.certain_ww_aligned)[0], 'POSSESSED'), cb.estimate(self.idx, list(self.certain_ww_aligned)[0], 'WEREWOLF'))
            elif self.accuse < 2:
                return cb.because(self.idx, cb.comingout(self.idx, self.idx, 'SEER'), cb.comingout(self.idx,list(self.certain_ww_aligned)[0], 'SEER' ))
            else:
                return cb.over()
        # for the nth day after 2 (late game)
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
        if len(self.targets) == 0:
            super.vote()
        else:
            return list(self.targets)[0] # vote the targeted player

    def divine(self):
        # div rand on day 0
        return random.choice( list( self.alive.difference(self.meSet).difference(self.all_divs) ) )

        # on day 1 and on there is no need to div copy seers / mediums as we know they are evil

    def finish(self):
        return super().finish(self)
