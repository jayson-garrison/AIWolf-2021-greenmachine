"""
    Contains Werewolf Class
    07/'21
    Grey Bodi
    Jayson C. Garrison
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
        self.WWs = set(map(lambda i: int(i), self.base_info["roleMap"].keys()))
        self.medium_target = set()
        self.seer_target = set()
        self.bodyguard_target = set()
        self.nthWhisper = -1
        self.daily_vote = True
        self.daily_estimate = True
        self.allyCOSeer = False
        self.allyCOMedium = False
        self.attackVote = []
        self.ally_whispers = []
        self.allyProposedAttack = []
        self.grnAttack = -1


    def update(self, base_info, diff_data, request):
        super().update(base_info, diff_data, request)
        print('$$$$$$$$$ WW WHISPERS $$$$$$$$$') #
        print(self.ally_whispers)
        # secondary reset
        # if not (self.currentDay == int( self.base_info['day']) ):
            # pass
            
        # parse whisper
        if request == 'WHISPER':
            for row in diff_data.itertuples():
                print('step ', end = '')
                type = getattr(row,"type")
                text = getattr(row,"text")

                # get ally WWs, do not add me to the set
                if type == 'initialize':
                    print('INIT reached') #
                    # phrase = str(text)
                    if self.idx != int( getattr(row, 'agent') ):
                        print( int( getattr(row, 'agent') ) )
                        self.WWs.add( int(getattr(row, 'agent')) )
                
                # update the talk list
                if type == 'whisper': # then gather the text
                    print('WW gather whisper reached') #
                    # if not ('SKIP' in text.upper() or 'OVER' in text.upper() ):
                    print('IF reached')
                    whisperList = [int(getattr(row, 'turn')), int( getattr(row, 'agent') ) , str(text) ]
                    self.ally_whispers.append(whisperList)
                    print('new whispers')
            
        # super().update(base_info, diff_data, request)

        # parsing whisperList
        while self.nthWhisper < len(self.ally_whispers and not len(self.ally_whispers) == 0):

            self.nthWhisper += 1

            if "ATTACK" in self.ally_whispers[self.nthTalk][2]:
                pass

            if "VOTE" in self.ally_whispers[self.nthTalk][2]:
                print("WW vote reached") #
                for twolist in self.attackVote:
                    if twolist[0] == self.ally_whispers[self.nthWhisper][1]:
                        self.attackVote.remove(twolist)
                self.attackVote.append([ self.ally_whispers[self.nthWhisper][1], self.ally_whispers[self.nthWhisper][2][11:13] ])

            elif "COMINGOUT" in self.ally_whispers[self.nthTalk][2]:
                print('WW CO reached')
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
        print('WEREWOLVES:')
        print(self.WWs)

        #

        #

        # heuristics

    def dayStart(self):
        super().dayStart()
        self.nthWhisper = -1
        self.daily_vote = True
        self.daily_estimate = True
        self.ally_whispers = []
        self.attackVote = []
        self.allyProposedAttack = []

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

    def whisper(self): # new
        print('WW Whisper reached') #
        if not self.hasCO:
            self.hasCO = True
            return cb.comingout(self.idx, self.idx, "VILLAGER")

        if self.daily_vote:
            self.daily_vote = False
            if len(self.attackVote) > 1:
                self.grnAttack = self.attackVote[0][1]
                return cb.vote(self.idx, self.grnAttack)
            elif self.currentDay < 3:
                self.grnAttack = random.choice(list(self.alive.difference(self.WWs).difference(self.likely_medium).difference(self.likely_seer)))
                return cb.vote(self.idx, self.grnAttack)
        
        
        return "Over"

    def attack(self): # new
        print('WW Attack reached') #
        return self.grnAttack
        # return cb.attack(self.idx, self.grnAttack)

    def finish(self):
        return super().finish()
