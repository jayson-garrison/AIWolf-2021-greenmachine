'''
Team greenmachine agent Driver.
Used to connect to server to assign behavior classes

Ground up begin by Jayson C. Garrison
'''

# import resources
import aiwolfpy
import aiwolfpy.contentbuilder as cb

# all 
import grnVillager as Villager

# Jayson
import grnSeer as Seer
import grnMedium as Medium
import grnBodyguard as Bodyguard

# Grey
import grnPossessed as Possessed
import grnWerewolf as Werewolf

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
