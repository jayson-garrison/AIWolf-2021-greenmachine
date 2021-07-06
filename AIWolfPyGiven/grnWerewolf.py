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
        # the possessed that is confirmed by signaling
        self.possessed = set()
        self.nthWhisper = -1
        self.identify_possessed = False
        self.fake_estimate_possessed = False
        self.daily_vote = True
        self.daily_estimate = True
        self.allyCOSeer = False
        self.allyCOMedium = False
        self.attackVote = []
        self.ally_whispers = []
        self.allyProposedAttack = []
        self.grnAttack = -1
        self.push_seer_vote = 0
        self.daily_vote_claim = 0


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
            
        # identify the possessed, true seer, true medium
        # if len(self.possessed) == 0:
        # in the case of a fake seer (most likely given past agent conventions):
        for agent, divs in self.divined.items():
            # false divine serves as signal
            if ( divs[0] in self.WWs and divs[1] == 'HUMAN' ) or ( divs[0] in self.alive.difference(self.WWs) and divs[1] == 'WEREWOLF' ):
                self.possessed.add(agent)
                self.seer_target.difference(self.possessed)
            elif divs[0] in self.WWs and divs[1] == 'WEREWOLF':
                self.seer_target.add(agent)
                self.possessed.difference(self.seer_target) # no overlap
            else:
                self.seer_target.add(agent)
                self.possessed.difference(self.seer_target) # no overlap

        # or in the case of a fake medium
        for agent, ids in self.identified.items():
            # false identification serves as signal
            if ( ids[0] in self.WWs and ids[1] == 'HUMAN' ) or ( divs[0] in self.dead and divs[1] == 'WEREWOLF' ):
                self.possessed.add(agent)
            elif ids[0] in self.WWs and ids[1] == 'WEREWOLF':
                self.medium_target.add(agent)

         # update ally alive status
        for ally in self.WWs:
            if ally not in self.alive:
                self.WWs.remove(ally)
        print('WEREWOLVES:')
        print(self.WWs)

        # heuristics

    def dayStart(self):
        super().dayStart()
        self.push_seer_vote = 0
        self.daily_vote_claim = 0
        self.nthWhisper = -1
        self.daily_vote = True
        self.daily_estimate = True
        self.ally_whispers = []
        self.attackVote = []
        self.allyProposedAttack = []

    def talk(self): # talk as villager with vested interest in aligning with fake seer 
        # talk as a villager
        # super.talk()

        if self.currentDay < 2:
            if not self.hasCO and self.role == 'VILLAGER' and len(self.requesters) == 0 and self.behavior <= 30:
                    self.hasCO = True
                    return cb.comingout(self.idx, self.idx, 'VILLAGER')
            elif self.talkTurn < 7:
                self.talkTurn += 1
                # best case, the possessed has signaled day 1
                if len(self.possessed) == 1:
                    if self.divined[  list(self.possessed)[0]  ][self.currentDay - 1][1] == 'WEREWOLF':
                        if not self.fake_estimate_possessed:
                            self.fake_estimate_possessed = True
                            return cb.estimate(self.idx, list(self.seer_target)[0], 'POSSESSED')
                        elif self.daily_vote_claim < 4:
                            self.daily_vote_claim += 1
                            return cb.vote(self.idx, self.divined[ list(self.possessed)[0] ][self.currentDay - 1][0] )
                elif list(self.seer_target)[0] in self.alive and self.push_seer_vote < 3:
                    self.push_seer_vote += 1
                    return cb.vote(self.idx, list(self.seer_target)[0])
                else:
                    return cb.skip()
        if self.currentDay > 2:
            pass
        else:
            pass

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

    def whisper(self): # attack and vote 
        print('WW Whisper reached') #
        if not self.hasCO:
            self.hasCO = True
            return cb.comingout(self.idx, self.idx, "VILLAGER")

        if not self.identify_possessed:
            self.identify_possessed = True
            return cb.estimate(self.idx, list(self.possessed)[0], 'POSSESSED')

        if self.daily_vote:
            self.daily_vote = False
            if len(self.attackVote) > 1:
                self.grnAttack = self.attackVote[0][1]
                return cb.vote(self.idx, self.grnAttack)
            elif self.currentDay < 3:
                self.grnAttack = random.choice(list(self.alive.difference(self.WWs).difference(self.likely_medium).difference(self.likely_seer)))
                return cb.vote(self.idx, self.grnAttack)

        return cb.over()

    def attack(self): # new
        print('WW Attack reached') #
        return self.grnAttack
        # return cb.attack(self.idx, self.grnAttack)

    def finish(self):
        return super().finish()
