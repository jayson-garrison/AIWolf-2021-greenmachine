"""
    Contains Posessed Class
    07/'21
    James Hale
    Grey Bodi
"""
import aiwolfpy
from aiwolfpy import contentbuilder as cb
import grnVillager
import random
import logging, json

class Possessed(grnVillager.Villager):
    def __init__(self, my_name):
        super().__init__(my_name)
        self.name = my_name
        self.previousDivined = dict()
        self.daily_divine = True
        self.daily_vote = 0
        self.daily_wwhuman = random.randint(1,100)

    def initialize(self, base_info, diff_data, game_setting):
        super().initialize(base_info, diff_data, game_setting)

    def update(self, base_info, diff_data, request):
        super().update(base_info, diff_data, request)
        for player in self.previousDivined:
            if player in self.dead:
                self.previousDivined.pop(player)
        #heuristics:
        #no one else can be possessed

    def dayStart(self):
        super().dayStart()
        self.daily_vote = 0
        self.daily_divine = True
        self.daily_wwhuman = random.randint(1,100)

    def talk(self):
        logging.debug("# TALK") # not sure where we need to put this 
        if self.talkTurn < 10: # max of 10 talks 
            self.talkTurn += 1
            if self.currentDay == 1:
                if not self.hasCO:
                    self.hasCO = True
                    return cb.comingout(self.idx, self.idx, 'SEER')
                elif self.daily_divine:
                    self.daily_divine = False
                    return self.fakedivine("HUMAN")
                else:
                    return cb.over()
            elif self.currentDay == 2:
                if self.daily_divine:
                    self.daily_divine = False
                    #this target should be likely human
                    return self.fakedivine("WEREWOLF")
                elif self.daily_vote < 4:
                    self.daily_vote += 1
                    return cb.vote(self.idx, list(self.previousDivined.keys)[-1]) #CHECK IF WORKS
                else:
                    return cb.over()
            else: #day 3+
                if self.daily_divine:
                    self.daily_divine = False
                    #divine a human or werewolf..
                    if self.daily_wwhuman <= 35 and len(self.previousDivined) < 4: #numbers here TBD
                        #going to divine as werewolf
                        return self.fakedivine("WEREWOLF")
                    else:
                        #going to divine as human
                        return self.fakedivine("HUMAN")
                elif self.daily_vote < 4:
                    self.daily_vote += 1
                    for player in self.previousDivined:
                        if self.previousDivined[player] == "WEREWOLF":
                            return cb.vote(self.idx, player)
                    return cb.over()
                        



                return cb.over()
        else: return cb.over()

    def vote(self):
        for player in self.previousDivined:
            if self.previousDivined[player] == "WEREWOLF":
                return cb.vote(self.idx, player)
        for player in self.COs:
            if "SEER" in self.COs[player]:
                return cb.vote(self.idx, player)
        #if no accused werewolves and no other seers, vote someone random


    def finish(self):
        super().finish()

    def fakedivine(self, role):
        try:
            target = random.choice(list(self.alive.difference(set(self.idx)).difference(self.likely_seer).difference(set(self.previousDivined.keys()))))
        except: #empty list
            return cb.skip()
        self.previousDivined[target] = role
        return cb.divined(self.idx, target, role)