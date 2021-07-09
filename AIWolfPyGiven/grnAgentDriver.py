'''
Team greenmachine agent Driver.
Used to connect to server to assign behavior classes
07/'21
Ground up begin by Jayson C. Garrison
'''

# import resources
# import aiwolfpy
import logging, json
from aiwolfpy import contentbuilder
# import AIWolfPyGiven.grnAgent
import aiwolfpy
# import grnAgent

from aiwolfpy import contentbuilder as cb

# Jayson and Grey
import grnVillager as Villager
import grnWerewolf as Werewolf

# Jayson
import grnSeer as Seer

# Grey
import grnPossessed as Possessed

# James
import grnMedium as Medium
import grnBodyguard as Bodyguard

# name the agent as our team name 

name = 'grnmachine'


class grnAgent(object):
    # initialize
    def __init__(self, agentName):
        self.myName = agentName # our name 
        self.role = None # no role yet by default
        logging.basicConfig(filename=self.myName+".log",
                            level=logging.DEBUG,
                            format='')
    
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
            self.role.initialize(base_info, diff_data, game_setting)
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
        except Exception as err:
            print(err)
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
        return None
        # return self.role.finish()


if __name__ == '__main__':
    # run the agent, needs verification
    aiwolfpy.connect_parse(grnAgent(name))

