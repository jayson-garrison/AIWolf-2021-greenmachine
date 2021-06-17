'''
Team greenmachine agent Driver.
Used to connect to server to assign behavior classes

Ground up begin by Jayson C. Garrison
'''

# import resources
from ..aiwolfpy import contentbuilder
import AIWolfPyGiven
import AIWolfPyGiven.grnAgent
import AIWolfPyGiven.aiwolfpy
#import AIWolfPyGiven.grnAgent

import AIWolfPyGiven.aiwolfpy.contentbuilder as cb

# all 
import AIWolfPyGiven.grnAgent.grnVillager as Villager

# Jayson
import AIWolfPyGiven.grnAgent.grnSeer as Seer
import AIWolfPyGiven.grnAgent.grnMedium as Medium
import AIWolfPyGiven.grnAgent.grnBodyguard as Bodyguard

# Grey
import AIWolfPyGiven.grnAgent.grnPossessed as Possessed
import AIWolfPyGiven.grnAgent.grnWerewolf as Werewolf

# name the agent as our team name 

name = 'grnmachine'

class grnAgent(object):

    # initialize
    def __init__(self, agentName):
        self.myName = agentName # our name 
        self.role = None # no role yet by default
    
    # get the name
    def getName(self):
        return self.myName
    
    # proper initialization
    def initialize(self, base_info, diff_data, game_setting):

        # add more initialization
        self.base_info = base_info
        self.diff_data = diff_data
        self.game_setting = game_setting

        # assign role behavior
        myRole = base_info['myRole']
        if self.game_setting['playerNum'] == 15: # this should always be the case I think
            if myRole == 'SEER':
                self.role = Seer(self.myName)
            elif myRole == 'MEDIUM':
                self.role = Medium(self.myName)
            elif myRole == 'BODYGUARD':
                self.role = Bodyguard(self.myName)
            elif myRole == 'POSSESSED':
                self.role = Possessed(self.myName)
            elif myRole == 'WEREWOLF':
                self.role = Werewolf(self.myName)
            else:
                self.role = Villager(self.myName)

    # action functions, if an exception occurs, perform a standard action
    
    def update(self, base_info, diff_data, request):
        try:
            self.role.update(base_info, diff_data, request)
        except Exception:
            pass
    
    def dayStart(self):
        try:
            self.role.dayStart()
        except Exception:
            pass

    def talk(self):
        try:
            return self.role.talk()
        except Exception:
            return cb.over()

    def vote(self):
        try:
            return self.role.vote()
        except Exception:
            return 1

    def divine(self):
        try:
            return self.role.divine()
        except Exception:
            return 1

    def guard(self):
        try:
            return self.role.guard()
        except Exception:
            return 1

    def whisper(self):
        try:
            return self.role.whisper()
        except Exception:
            return cb.over()

    def attack(self):
        try:
            return self.role.attack()
        except Exception:
            return 1

    def finish(self):
        return self.role.finish()

# run the agent, needs verification

agent = grnAgent(name)

# connect and run 

if __name__ == '__main__':
    AIWolfPyGiven.aiwolfpy.connect_parse(agent)
    