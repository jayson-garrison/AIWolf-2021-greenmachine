"""
    Contains Werewolf Class
    James Hale
"""
import aiwolfpy
from aiwolfpy import contentbuilder as cb
import grnVillager

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
        self.allyCOSeer = False
        self.allyCOMedium = False
        self.attackVote = []
        self.ally_whispers = []
        self.allyProposedAttack = []


    def update(self, base_info, diff_data, request):
        super().update(base_info, diff_data, request)

        # secondary reset
        if not (self.currentDay == int( self.base_info['day']) ):
            self.nthWhisper = -1
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
        return 1

    def divine(self):
        pass

    def guard(self):
        return 1

    def whisper(self): # new
        return "Over"

    def attack(self): # new
        pass

    def finish(self):
        super().finish()
