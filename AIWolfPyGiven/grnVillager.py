
'''
Contains Villager Class
07/'21
James Hale
Jayson C. Garrison
Grey Bodi
'''
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
import random

myname = 'greenmachine'

class Villager(object):
    def __init__(self, agent_name):
        self.myname = agent_name # agent name 
        self.idx = -1  # Our agent ID
        # initialize log 
        logging.basicConfig(filename=self.myname+".log",
                            level=logging.DEBUG,
                            format='')

    def getName(self):
        logging.debug("# GETNAME")
        return self.myname

    # new game (no return)
    def initialize(self, base_info, diff_data, game_setting):
        self.base_info = base_info
        self.game_setting = game_setting

        self.role = self.base_info['myRole']
        
        self.behavior = random.randint(1,100)

        if self.idx < 0:
            self.idx = base_info['agentIdx']
        
        logging.debug("# INITIALIZE")
        logging.debug("Game Setting:")
        logging.debug(json.dumps(game_setting, indent=2))
        logging.debug("Base Info:")
        logging.debug(json.dumps(base_info, indent=2))
        logging.debug("Diff Data:")
        logging.debug(diff_data)

        self.hasCO = False
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
        self.others = self.alive.copy() 
        self.others.remove(self.idx)
        # all other players who tend to agree with me
        self.agreers = {player: 0 for player in self.others} 
        # ^^ but disagree
        self.disagreers = {player: 0 for player in self.others} 
        self.dead = set()
        self.executed = set()
        # make sure executed + killed = dead
        self.killed = set() 
        self.seers = dict()
        self.mediums = dict()
        self.bodyguards = set()
        self.likely_human = set()
        self.likely_werewolf = set()
        self.likely_seer = set()
        self.likely_medium = set()
        self.likely_possessed = set()
        self.likely_bodyguard = set()
        # not sure if likely human or werewolf. Make sure likely_human + likely_werewolf + unknown = others
        self.unknown = self.others.copy()
        # agents who request something of me
        self.requesters = [] 
        # 2d list of agent talks of the day
        # format:
        # [ [0: turn, 1: agent, 2: text] ]
        self.agent_talks = [] 
        # counting votes 
        self.estimate_votes = {player: [] for player in self.alive}
        # keeping track of temp info
        self.nthTalk = -1
        self.currentDay = -1
        self.repeatTalk = False
        self.unaccused = self.alive.copy()
        self.will_vote = []
        self.talk_cases = set()
        self.estimate = 0
        self.accuse = 0
        # if these ever equal 2 then villager has estimated and logically claimed that there is a true role
        self.true_medium_state = 0
        self.true_seer_state = 0
        self.daily_push_vote = 0



    # new information (no return)
    # add to lists (majority of the work)
    def update(self, base_info, diff_data, request):
        # print('reached update') #
        print(self.agent_talks)
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
        # if not (self.currentDay == int( self.base_info['day']) ):
            

        self.currentDay = int(self.base_info['day'])

        for row in diff_data.itertuples():
            type = getattr(row,"type")
            text = getattr(row,"text")
            # print('reached for')
            # print(self.COs) #
            # update executed players
            if type == 'execute':
                self.executed.add( int(getattr(row, 'agent')) )
                self.dead.add( int(getattr(row, 'agent')) )
                self.alive.remove( int(getattr(row, 'agent')) )

            # update dead players
            if type == 'dead':
                self.killed.add( int(getattr(row, 'agent')) )
                self.dead.add( int(getattr(row, 'agent')) )
                self.alive.remove( int(getattr(row, 'agent')) )

            # update voting 
            if type == 'vote': # then...
                pass

            # update the talk list
            if type == 'talk': # then gather the text
                if not ('SKIP' in text.upper() or 'OVER' in text.upper() ):
                    talkList = [int(getattr(row, 'turn')), int( getattr(row, 'agent') ) , str(text) ]
                    self.agent_talks.append(talkList)
                    print('new talks')

        # for new talks do:
        #endPos = len(self.agent_talks)
        while self.nthTalk < len(self.agent_talks) and not len(self.agent_talks) == 0:

            self.nthTalk += 1
            print( 'nth talk' + str(self.nthTalk) )

            # agent 0
            if "VOTE" in self.agent_talks[self.nthTalk][2]:
                print('reached VOTE')
                voter = self.agent_talks[self.nthTalk][1]
                voted = int( self.agent_talks[self.nthTalk][2][11:13] )
                for key_voted in self.estimate_votes:
                    if voter in self.estimate_votes[key_voted]:
                        self.estimate_votes[key_voted].remove(voter)
                self.estimate_votes[voted].append(voter)
                print(self.estimate_votes) #

            elif "COMINGOUT" in self.agent_talks[self.nthTalk][2]:
                print('reached COs') #
                who = self.agent_talks[self.nthTalk][1]
                # print(who)
                subject = int( self.agent_talks[self.nthTalk][2][16:18] )
                # print(subject)

                if who == subject:
                    self.COs[who].add(self.agent_talks[self.nthTalk][2][20:])
                    # consider else if an agent CO for another is significant
                    if self.agent_talks[self.nthTalk][2][20:] == "SEER" and not (who in self.seers):
                        #self.seers.add(self.agent_talks[self.nthTalk][1])
                        self.seers[self.agent_talks[self.nthTalk][1]] = 0
                        print('seers:')
                        print(self.seers) #

                    elif self.agent_talks[self.nthTalk][2][20:] == "MEDIUM" and not (who in self.mediums):
                        #self.mediums.add(self.agent_talks[self.nthTalk][1])
                        self.mediums[self.agent_talks[self.nthTalk][1]] = 0
                        print('mediums:')
                        print(self.mediums) #

                    print(self.COs) #

            #elif "ESTIMATE" in self.agent_talks[self.nthTalk][2]:
                #pass # add to requestors and evaluate if a reasonable request
            
            elif "DIVINED" in self.agent_talks[self.nthTalk][2]:
                print('reached DIV')
                # add to diviners
                target = int(self.agent_talks[self.nthTalk][2][14:16])
                species = self.agent_talks[self.nthTalk][2][18:]
                if self.agent_talks[self.nthTalk][1] in self.divined: #not the first divine
                    self.divined[self.agent_talks[self.nthTalk][1]].append([target, species])
                else: #first divine
                    self.divined[self.agent_talks[self.nthTalk][1]] = [[target, species]]

                if self.agent_talks[self.nthTalk][1] not in self.seers:
                    self.seers[self.agent_talks[self.nthTalk][1]] = 0
                elif species == "WEREWOLF":
                    self.seers[self.agent_talks[self.nthTalk][1]] += 1

                print(self.divined) #
                print('seers:')
                print(self.seers) #

            elif "IDENTIFIED" in self.agent_talks[self.nthTalk][2]:
                print('reached IDE')
                # add to likely mediums 
                target = int(self.agent_talks[self.nthTalk][2][17:19])
                species = self.agent_talks[self.nthTalk][2][21:]
                if self.agent_talks[self.nthTalk][1] in self.identified: #not the first divine
                    self.identified[self.agent_talks[self.nthTalk][1]].append([target, species])
                else: #first divine
                    self.identified[self.agent_talks[self.nthTalk][1]] = [[target, species]]
                if self.agent_talks[self.nthTalk][1] not in self.mediums:
                    self.mediums[self.agent_talks[self.nthTalk][1]] = 0
                elif species == "WEREWOLF":
                    self.mediums[self.agent_talks[self.nthTalk][1]] += 1

                print(self.identified) #
                print('mediums:') #
                print(self.mediums) #

            elif "GUARDED" in self.agent_talks[self.nthTalk][2]:
                # add to likely bodyguard
                self.bodyguards.add(self.agent_talks[self.nthTalk][2][6:8])
        
            '''
            # agent 0.5
            if "INQUIRE" in self.agent_talks[self.nthTalk][2]:
                pass # add to estimators and assign roles accordingly
            if "REQUEST" in self.agent_talks[self.nthTalk][2]:
                pass

            # agent 1
            if "BECAUSE" in self.agent_talks[self.nthTalk][2]:
                pass
            if "NOT" in self.agent_talks[self.nthTalk][2]:
                pass
            if "AND" in self.agent_talks[self.nthTalk][2]:
                pass
            if "OR" in self.agent_talks[self.nthTalk][2]:
                pass
            if "XOR" in self.agent_talks[self.nthTalk][2]:
                pass
            '''
            # estimate roles

            # if only 1 medium CO that medium is trustworthy
            if len(self.mediums) == 1 and self.currentDay != 1:
                self.likely_medium.add( next(iter(self.mediums.values())) )
                self.likely_human.add( next(iter(self.mediums.values())) )
            
            # if only 1 seer CO that seer is trustworthy
            if len(self.seers) == 1 and self.currentDay != 1:
                self.likely_seer.add( next(iter(self.seers.values())) )
                self.likely_human.add( next(iter(self.seers.values())) )

            # those who div on day 1 WW are suspicous - 3/14 RNG
            if len(self.seers) > 1 and self.currentDay == 1:
                for sus in self.seers:
                    if self.seers[sus] > 0:
                        self.likely_possessed.add(sus)
                        self.likely_werewolf.add(sus)
            
            # seers who CO and were killed are deemed innocent, the others are suspicous
            if len(self.seers) > 1:
                for inno in self.seers:
                    if inno in self.killed:
                        susSeers = self.seers.copy()  
                        susSeers.pop(inno)
                        for sus in susSeers:
                            self.likely_werewolf.add(sus)

            # if someone divined us as WW they are likely WW or POS
            if self.currentDay > 1 and self.role:
                for sus in self.divined:
                    if self.divined[sus] == [self.idx, 'WEREWOLF']:
                        self.likely_werewolf.add(sus)
                        self.likely_possessed.add(sus)

            # role specific identification (in other classes)

            
    # Start of the day (no return)
    def dayStart(self):
        # keep track of number of times we have talked today 
        self.talkTurn = 0 
        logging.debug("# DAYSTART")
        print('----------------------------------REACHED RESET----------------------------------') #
        print('ALIVE:') #
        print(self.alive) #
        print('DEAD:') #
        print(self.dead) #
        print('KILLED:') #
        print(self.killed) #
        print('EXECUTED:') #
        print(self.executed) #

        # resets
        self.nthTalk = -1
        self.agent_talks = []
        self.estimate_votes = {player: [] for player in self.alive}
        self.repeatTalk = False
        self.unaccused = self.alive.copy()
        self.estimate = 0
        self.accuse = 0
        return None

    # conversation actions: require a properly formatted
    # protocol string as the return.
    # act based on the lists
    def talk(self):
        logging.debug("# TALK") # not sure where we need to put this 
        if self.talkTurn < 10: # max of 10 talks 
            self.talkTurn += 1

            # day 1 talking logic
            if int(self.base_info['day']) == 1:
                # 30% CO Villager
                if not self.hasCO and self.role == 'VILLAGER' and len(self.requesters) == 0 and self.behavior <= 30:
                    self.hasCO = True
                    return cb.comingout(self.idx, self.idx, 'VILLAGER')
                elif self.talkTurn < 5:
                    if len(self.seers) > 1:
                        for targ in self.seers:
                            if self.seers[targ] > 0:
                                return cb.vote(self.idx, targ)
                    else:
                        cb.skip()
                else: return cb.over()

            # day 2 talk logic
            if int(self.base_info['day']) == 2:
                if len(self.seers) > 1:
                    for targ in self.seers:
                        if self.seers[targ] > 0 and targ in self.unaccused:
                            self.unaccused.remove(targ)
                            self.likely_werewolf.add(targ)
                            self.will_vote.append(targ)
                            return cb.logicalxor(self.idx, cb.estimate(self.idx, targ, "POSSESSED"), cb.estimate(self.idx, targ, "WEREWOLF"))
                elif len(self.seers) == 1 and next(iter(self.seers.values())) in self.unaccused:
                    self.unaccused.remove(next(iter(self.seers.values())))
                    self.likely_human.add(next(iter(self.seers.values())))
                    return cb.estimate(self.idx, next(iter(self.seers.values())), "SEER")
                else:
                    return cb.skip()
                    
            # late game logic
            if int(self.base_info['day']) > 2:
                # if only one medium then estimate true medium 
                if len(self.likely_medium) == 1:
                    if self.true_medium_state == 0:
                        self.true_medium_state += 1
                        return cb.estimate(self.idx, list(self.likely_medium)[0], 'MEDIUM' )
                    if self.true_medium_state == 1:
                        self.repeatMediumLogic += 1
                        return cb.because(self.idx, cb.estimate(self.idx, list(self.likely_medium)[0], 'MEDIUM' ), cb.comingout(list(self.likely_medium)[0], list(self.likely_medium)[0], 'MEDIUM') )
                # if only one seer then estimate true seer
                elif len(self.likely_seer) == 1:
                    if self.true_seer_state == 0:
                        self.true_seer_state += 1
                        return cb.estimate(self.idx, list(self.likely_seer)[0], 'SEER' )
                    if self.true_seer_state == 1:
                        self.true_seer_state += 1
                        return cb.because(self.idx, cb.estimate(self.idx, list(self.likely_seer[0], 'SEER' )), cb.comingout(list(self.likely_seer)[0], list(self.likely_medium)[0], 'SEER') )
                # claim to vote someone, need probTable
                elif self.daily_push_vote < 3: 
                    self.daily_push_vote += 1
                    return cb.vote(self.idx, 1)
                else: return cb.over() # talk 
        else:
            return cb.over() # by default, ret over

    # targetted actions: Require the id of the target
    # agent as the return
    # act based on the lists
    def vote(self):
        logging.debug("# VOTE")
        max = -1
        maxWW = -1
        voteWW = -1
        voteHim = -1
        for player in self.estimate_votes:
            if len(self.estimate_votes[player]) > max:
                max = len(self.estimate_votes[player])
                voteHim = player
            if len(self.estimate_votes[player]) > maxWW and player in self.alive.union(self.likely_werewolf):
                    maxWW = len(self.estimate_votes[player])
                    voteWW = player
        if voteHim in self.likely_werewolf or self.currentDay < 4:
            return voteHim

        else:
            return voteWW

    # Finish (no return)
    def finish(self):
        logging.debug("# FINISH")
        return None