"""
    Contains Werewolf Class
    James Hale
"""
import aiwolfpy
from aiwolfpy import contentbuilder as cb
import grnVillager
import logging, json
import random

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
        self.allyCOSeer = False
        self.allyCOMedium = False
        self.attackVote = []
        self.ally_whispers = []
        self.allyProposedAttack = []
        self.grnAttack = -1


    def update(self, base_info, diff_data, request):
        super().update(base_info, diff_data, request)

        # secondary reset
        if not (self.currentDay == int( self.base_info['day']) ):
            self.nthWhisper = -1
            self.daily_vote = -1
            self.daily_estimate = -1
            self.ally_whispers = []
            self.attackVote = []
            self.allyProposedAttack = []
            

        # parse whisper
        for row in diff_data.itertuples():
            type = getattr(row,"type")
            text = getattr(row,"text")
            if type == 'whisper':
            # update the talk list
                if type == 'talk': # then gather the text
                    if self.currentDay != 0 and not ('SKIP' in text.upper() or 'OVER' in text.upper() ):
                        whisperList = [int(getattr(row, 'turn')), int( getattr(row, 'agent') ) , str(text) ]
                        self.ally_whispers.append(whisperList)
                        print('new talks')
                    else:
                        whisperList = [int(getattr(row, 'turn')), int( getattr(row, 'agent') ) , str(text) ]
                        self.ally_whispers.append(whisperList)
                        print('new talks')
        
        while self.nthWhisper < len(self.ally_whispers and not len(self.ally_whispers) == 0):

            self.nthWhisper += 1

            if "VOTE" in self.ally_whispers[self.nthTalk][2]:
                for twolist in self.attackVote:
                    if twolist[0] == self.ally_whispers[self.nthWhisper][1]:
                        self.attackVote.remove(twolist)
                self.attackVote.append([ self.ally_whispers[self.nthWhisper][1], self.ally_whispers[self.nthWishper][2][11:13] ])

            elif "COMINGOUT" in self.ally_whispers[self.nthTalk][2]:
                who = self.ally_whispers[self.nthTalk][1]
                # print(who)
                subject = int( self.ally_whispers[self.nthTalk][2][16:18] )
                # print(subject)
                if who == subject:
                    if self.ally_whispers[self.nthTalk][2][20:] == "SEER":
                        self.allyCOSeer = True
                    if self.ally_whispers[self.nthTalk][2][20:] == "MEDIUM":
                        self.allyCOMedium = True

            elif "ESTIMATE" in self.ally_whispers[self.nthTalk][2]:
                pass

        # update ally alive status
        for ally in self.WWs:
            if ally not in self.alive:
                self.WWs.remove(ally)

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

        if self.daily_vote:
            if len(self.attackVote) > 1:
                self.grnAttack = self.attackVote[0][1]
                return cb.vote(self.idx, self.grnAttack)
            elif self.currentDay < 3:
                self.grnAttack = random.choice(self.alive.difference(self.WWs).difference(self.likely_medium).difference(self.likely_seer))
                return cb.vote(self.idx, self.grnAttack)
        
        
        return "Over"

    def attack(self): # new
        return cb.attack(self.idx, self.grnAttack)

    def finish(self):
        super().finish()
