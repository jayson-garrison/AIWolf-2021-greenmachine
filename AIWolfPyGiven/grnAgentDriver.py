'''
Team greenmachine agent Driver.
Used to connect to server to assign behavior classes

Ground up begin by Jayson C. Garrison
'''

# import resources
# import aiwolfpy
from aiwolfpy import contentbuilder
# import AIWolfPyGiven.grnAgent
import aiwolfpy
# import grnAgent

from aiwolfpy import contentbuilder as cb

# all 
import grnVillager as Villager

# Jayson
import grnSeer as Seer
import grnMedium as Medium
import grnBodyguard as Bodyguard

# Grey
import grnPossessed as Possessed
import grnWerewolf as Werewolf

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
        if self.game_setting['playerNum'] == 15:  # this should always be the case I think
            if myRole == 'SEER':
                self.role = Seer.Seer(self.myName)
            elif myRole == 'MEDIUM':
                self.role = Medium.Medium(self.myName)
            elif myRole == 'BODYGUARD':
                self.role = Bodyguard.BodyGuard(self.myName)
            elif myRole == 'POSSESSED':
                self.role = Possessed.Possessed(self.myName)
            elif myRole == 'WEREWOLF':
                self.role = Werewolf.Werewolf(self.myName)
            else:
                self.role = Villager.Villager(self.myName)

    # action functions, if an exception occurs, perform a standard action
    
    def update(self, base_info, diff_data, request):
        try:
            self.role.update(base_info, diff_data, request)
        except Exception:
            pass
    
    def dayStart(self):
        pass
        try:
            self.role.dayStart()
        except Exception:
            pass

    def talk(self):
        try:
            return self.role.talk()
        except Exception as err:
            print(err)
            return cb.over()

    def vote(self):
        try:
            return self.role.vote()
        except Exception:
            return 1

    def divine(self):
        return 1
        try:
            return self.role.divine()
        except Exception:
            return 1

    def guard(self):
        return 1
        try:
            return self.role.guard()
        except Exception:
            return 1

    def whisper(self):
        return cb.over()
        try:
            return self.role.whisper()
        except Exception:
            return cb.over()

    def attack(self):
        return 1
        try:
            return self.role.attack()
        except Exception:
            return 1

    def finish(self):
        return None
        # return self.role.finish()


if __name__ == '__main__':
    # run the agent, needs verification
    aiwolfpy.connect_parse(grnAgent(name))

