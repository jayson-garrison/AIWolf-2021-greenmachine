"""
    Contains Werewolf Class
    James Hale
"""
import aiwolfpy
from aiwolfpy import contentbuilder as cb
import grnVillager
import logging, json

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
        self.daily_vote = -1
        self.daily_estimate = -1

    def update(self, base_info, diff_data, request):
        super().update(base_info, diff_data, request)

        # secondary reset
        if not (self.currentDay == int( self.base_info['day']) ):
            self.nthWhisper = -1
            self.daily_vote = -1
            self.daily_estimate = -1

        # parse whisper

        #
        
        #

        #

        # heuristics

        



    def dayStart(self):
        pass

    def talk(self): # new
        return "Over"

    def vote(self): # new
        logging.debug("# VOTE")
        max = -1
        maxWW = -1
        vote = -1
        voteWW = -1
        
        for player in self.estimate_votes:
            if len(self.estimate_votes[player]) > max and player not in self.WWs: #debug try "and not (player in self.WWs)"
                max = len(self.estimate_votes[player])
                vote = player
                if player in self.alive.union(self.likely_werewolf):
                    maxWW = len(self.estimate_votes[player])
                    voteWW = player
        if vote in self.likely_werewolf or self.currentDay < 4:
            return vote

        else:
            return voteWW

    def divine(self):
        pass

    def guard(self):
        return 1

    def whisper(self): # new
        if not self.hasCO:
            self.hasCO = True
            return cb.comingout(self.idx, self.idx, "VILLAGER")

        if len(proposedAttack)
        elif self.currentDay < 3:
            pass
            #vote random villiager
        
        
        return "Over"

    def attack(self): # new
        pass

    def finish(self):
        super().finish()
