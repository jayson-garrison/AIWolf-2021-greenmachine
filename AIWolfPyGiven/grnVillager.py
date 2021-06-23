
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
        # our own COs would be self.COs[self.base_info['agentIdx']]
        self.COs = {player: set() for player in self.alive} 
        # players who voted for me
        self.votedme = set() 
        #everyone who said they divined someone, paired with who they divined
        self.divined = dict() 
        #everyone who said they identified someone, paired with who they identified
        self.identified = dict() 
        #self.initialized_broadcasts = set()
        # when our own data is not needed
        self.others = self.alive.copy().remove(self.base_info['agentIdx']) 
        # all other players who tend to agree with me
        self.agreers = {player: 0 for player in self.others} 
        # ^^ but disagree
        self.disagreers = {player: 0 for player in self.other} 
        self.dead = set()
        self.executed = set()
        # make sure executed + killed = dead
        self.killed = set() 
        self.seers = set()
        self.mediums = set()
        self.likely_human = set()
        self.likely_werewolf = set()
        # not sure if likely human or werewolf. Make sure likely_human + likely_werewolf + unknown = others
        self.unknown = self.others.copy()
        # agents who request something of me
        self.requesters = set() 
        # 2d list of agent talks of the day
        # format:
        # [ [0: turn, 1: agent, 2: text] ]
        self.agent_talks = [] 
        self.nthTalk = 0
        self.estimate_votes = {player: [] for player in self.alive}
        self.currentDay = 0




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

        # if a new day. reset the talks, estimate votes
        if not (self.currentDay == int( self.base_info['day']) ):
            self.agent_talks = []
            self.estimate_votes = {player: [] for player in self.alive}

        self.currentDay = int(self.base_info['day'])
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
                talkList = [int(getattr(row, 'turn')), "{0:02d}".format( int(getattr(row, 'agent')) ), str(text) ]
                self.agent_talks.append(talkList)

                '''
                turn = 
                talker =  "{0:02d}".format( int(getattr(row, 'agent')) ) 
                #rowCount = int( getattr(row, 'turn') )
                talkString = str(talker) + ' ' + str(text)
                #self.agent_talks[rowCount].append(talkString)
                self.agent_talks.append(talkString)
                '''

        

        # for new talks do:
        #endPos = len(self.agent_talks)
        while self.nthTalk < len(self.agent_talks):

            # agent 0
            if "VOTE" in self.agent_talks[self.nthTalk]:
                
                voter = self.agent_talks[self.nthTalk][1]
                voted = int( self.agent_talks[self.nthTalk][2][11:13] )
                for key_voted in self.estimate_votes:
                    if voter in self.estimate_votes[key_voted]:
                        self.estimate_votes[key_voted].remove(voter)
                self.estimate_votes[voted].append(voter)
                    
            if "COMINGOUT" in self.agent_talks[self.nthTalk]:
                who = self.agent_talks[self.nthTalk][1]
                subject = int( self.agent_talks[self.nthTalk][2][17:19] )
                if who == subject:
                    self.COs[who].add(self.agent_talks[self.nthTalk][2][20:])
                    # consider else if an agent CO for another is significant

            if "ESTIMATE" in self.agent_talks[self.nthTalk]:
                pass # add to estimators and assign roles accordingly
                pass # add to requestors and evaluate if a reasonable request
            if "DIVINED" in self.agent_talks[self.nthTalk]:
                # add to diviners
                target = int(self.agent_talks[self.nthTalk][2][14:16])
                species = self.agent_talks[self.nthTalk][2][19:]
                if self.agent_talks[self.nthTalk][1] in self.divined: #not the first divine
                    self.divined[self.agent_talks[self.nthTalk][1]].add([target, species])
                else: #first divine
                    self.divined[self.agent_talks[self.nthTalk][1]] = [[target, species]]
                if self.agent_talks[self.nthTalk][1] not in self.seers: self.seers.add(self.agent_talks[self.nthTalk][1])

            if "IDENTIFIED" in self.agent_talks[self.nthTalk]:
                # add to likely mediums 
                target = int(self.agent_talks[self.nthTalk][2][17:19])
                species = self.agent_talks[self.nthTalk][2][22:]
                if self.agent_talks[self.nthTalk][1] in self.identified: #not the first divine
                    self.identified[self.agent_talks[self.nthTalk][1]].add([target, species])
                else: #first divine
                    self.identified[self.agent_talks[self.nthTalk][1]] = [[target, species]]
                if self.agent_talks[self.nthTalk][1] not in self.mediums: self.mediums.add(self.agent_talks[self.nthTalk][1])
                
            if "GUARDED" in self.agent_talks[self.nthTalk]:
                pass # add to likely bodyguard

            # agent 0.5
            if "INQUIRE" in self.agent_talks[self.nthTalk]:
                pass # add to estimators and assign roles accordingly
            if "REQUEST" in self.agent_talks[self.nthTalk]:
                pass

            # agent 1
            if "BECAUSE" in self.agent_talks[self.nthTalk]:
                pass
            if "NOT" in self.agent_talks[self.nthTalk]:
                pass
            if "AND" in self.agent_talks[self.nthTalk]:
                pass
            if "OR" in self.agent_talks[self.nthTalk]:
                pass
            if "XOR" in self.agent_talks[self.nthTalk]:
                pass
            self.nthTalk += 1


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



