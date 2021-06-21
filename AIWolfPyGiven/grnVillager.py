
#!/usr/bin/env python
from __future__ import print_function, division

# This sample script connects to the AIWolf server
# and responds appropriately to all server requests.
# It does not say anything and gives itself as the
# target id for any request, resulting in random actions.

# Additionally, it prints to the standard input all the
# information that it received from the server, which can
# be useful when developing your own client.

import aiwolfpy
from aiwolfpy import contentbuilder as cb
import logging, json

myname = 'greenmachine'

class Villager(object):
    def __init__(self, agent_name):
        self.myname = agent_name # agent name 

        # initialize log 
        logging.basicConfig(filename=self.myname+".log",
                            level=logging.DEBUG,
                            format='')

    def getName(self):
        logging.debug("# GETNAME")
        return self.myname

    # new game (no return)
    def initialize(self, base_info, diff_data, game_setting):
        logging.debug("# INITIALIZE")
        logging.debug("Game Setting:")
        logging.debug(json.dumps(game_setting, indent=2))
        logging.debug("Base Info:")
        logging.debug(json.dumps(base_info, indent=2))
        logging.debug("Diff Data:")
        logging.debug(diff_data)
        self.base_info = base_info
        self.game_setting = game_setting
        # print(base_info)
        # print(diff_data)
        self.alive = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}
        self.COs = {player: "" for player in self.alive} #our own COs would be self.COs[self.base_info['agentIdx']]
        self.votedme = set() #players who voted for me
        self.divined_broadcasts = set()
        self.initialized_broadcasts = set()
        self.others = self.alive.copy().remove(self.base_info['agentIdx']) #when our own data is not needed
        self.agreers = {player: 0 for player in self.others} #all other players who tend to agree with me
        self.disagreers = {player: 0 for player in self.other} #^^ but disagree
        self.dead = set()
        self.executed = set()
        self.killed = set() #make sure executed + killed = dead
        self.likely_human = set()
        self.likely_werewolf = set()
        self.unknown = self.others.copy() #not sure if likely human or werewolf. Make sure likely_human + likely_werewolf + unknown = others
        self.requesters = set() #agens who request something of me
        # an empty list that will be used as a 2d array of strings to track agent talks.
        # it resets everyday and is filled in the update fx when server requests the talk fx
        # contents take the form: "[who] [text]" where the row is the turn and the col is the
        # text.
        self.agent_talks = [] 
        #self.rowCount = 0




    # new information (no return)
    # add to lists (majority of the work)
    def update(self, base_info, diff_data, request):
        logging.debug("# UPDATE")
        logging.debug("Request:")
        logging.debug(request)
        logging.debug("Base Info:")
        logging.debug(json.dumps(base_info, indent=2))
        logging.debug("Diff Data:")
        logging.debug(diff_data)

        self.base_info = base_info
        # print(base_info)
        # print(diff_data)

        # scan diff_data for different info based on type
        currentDay = int(self.base_info['day'])
        for row in diff_data.itertuples():
            type = getattr(row,"type")
            text = getattr(row,"text")
            
            # update executed players
            if type == 'execute':
                self.executed.add( int(getattr(row, 'agent')) )
                self.dead.add( int(getattr(row, 'agent')) )

            # update dead players
            if type == 'dead':
                self.killed.add( int(getattr(row, 'agent')) )
                self.dead.add( int(getattr(row, 'agent')) )

            # update voting 
            if type == 'vote': # then...
                pass

            # update the talk list
            if type == 'talk': # then gather the text
                talker = getattr(row, 'agent')
                rowCount = int( getattr(row, 'turn') )
                talkString = str(talker) + text
                self.agent_talks[rowCount].append(talkString)
                
        # if a new day. reset the talks
        if not (currentDay == int( self.base_info['day']) ):
            self.agent_talks = []





    # Start of the day (no return)
    def dayStart(self):
        self.talkTurn = 0 # keep track of number of times we have talked today 
        logging.debug("# DAYSTART")
        return None

    # conversation actions: require a properly formatted
    # protocol string as the return.
    # act based on the lists
    def talk(self):
        logging.debug("# TALK") # not sure where we need to put this 
        if self.talkTurn < 10: # max of 10 talks 
            self.talkTurn += 1
            # if it is day 1, skip talking since there is no info, unless someone
            # requests us to CO, Vote, Agree, etc
            if self.base_info['myRole'] == 'VILLAGER' and len(self.requesters) == 0 and int(self.base_info['day']) == 1:
                return cb.skip()
            return # talk 
        else:
            return cb.over() # by default, ret over

    # targetted actions: Require the id of the target
    # agent as the return
    # act based on the lists
    def vote(self):
        logging.debug("# VOTE")
        for targ in self.COs:
            if "WEREWOLF" in self.COs[targ]:
                return targ

        return self.base_info['agentIdx']

    # Finish (no return)
    def finish(self):
        logging.debug("# FINISH")
        return None

# Do not need this as the driver function initializes it
''' 
agent = grnVillager(myname)

# run
if __name__ == '__main__':
    AIWolfPyGiven.aiwolfpy.connect_parse(agent)
'''



