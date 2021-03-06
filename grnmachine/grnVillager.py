
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
from CheatCodes import CheatCodes
from probabilityTable import ProbabilityTable
import re

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
        #everyone who said they divined someone, paired with [who they divined, human/werewolf]
        self.divined = dict() 
        #everyone who said they identified someone, paired with [who they identified, human/werewolf]
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
        self.seers = dict() # key: seer, value: an integer cooresponding to how any werewolf divines there are
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
        # never take a man's word
        self.forbidden = ['OR', 'XOR', 'NOT', 'BECAUSE', 'AND', 'SKIP', 'OVER', 'REQUEST', 'INQUIRE', 'DAY', 'VOTED', 'ATTACKED', 'AGREE', 'DISAGREE']
        # counting votes 
        self.estimate_votes = {player: set() for player in self.alive}
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

        #self.pt = CheatCodes({ "WEREWOLF":3, "POSSESSED":1, "SEER":1, "MEDIUM":1, "V/BG":9 })
        self.pt = ProbabilityTable({"Werewolf": 3, "Possessed": 1, "Villager": 8, "Bodyguard": 1, "Medium": 1, "Seer": 1}, 15)
        self.alpha = .1
        self.beta = .15
        self.gamma = .2
        self.delta = .25
        self.epsilon = .3
        
        self.prev_estimate_votes = {player: set() for player in self.alive}
        self.prev_voted_out = -1
        self.votes = {player: set() for player in self.alive}
        self.prev_votes = {player: set() for player in self.alive}
        self.prev_dead = -1

        #set of each player that hasn't satisfied a heuristic, indexed by heuristic number (up to 13, total heuristics)
        self.heuristics = [{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15} for i in range(13)]
        

        self.repeatMediumLogic = 0 #?


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
                #print("REACHED EXECUTE")
                self.executed.add( int(getattr(row, 'agent')) )
                self.dead.add( int(getattr(row, 'agent')) )
                self.alive.remove( int(getattr(row, 'agent')) )
                self.prev_voted_out = int(getattr(row, 'agent'))

            # update dead players
            elif type == 'dead':
                #print("REACHED DEAD")
                self.killed.add( int(getattr(row, 'agent')) )
                self.dead.add( int(getattr(row, 'agent')) )
                self.alive.remove( int(getattr(row, 'agent')) )
                self.prev_dead = int(getattr(row, 'agent'))

            #update voting 
            elif type == 'vote': # then...
                voter = int(getattr(row, 'idx'))
                voted = int(getattr(row, 'agent'))
                self.votes[voted].add(voter)

            # update the talk list
            elif type == 'talk': # then gather the text
                #if not ('SKIP' in text.upper() or 'OVER' in text.upper() ):
                if not any(phrase in text.upper() for phrase in self.forbidden):
                    talkList = [int(getattr(row, 'turn')), int( getattr(row, 'agent') ) , str(text) ]
                    self.agent_talks.append(talkList)
                    print('new talks')

        # for new talks do:
        #endPos = len(self.agent_talks)
        while self.nthTalk < len(self.agent_talks) and not len(self.agent_talks) == 0:
            
            self.nthTalk += 1
            print( 'nth talk' + str(self.nthTalk) )
            # never take a man's word
            # if 'BECAUSE' or 'XOR' or 'OR' or 'AND' or 'REQUEST' or 'ESTIMATE' or 'DAY' or 'INQUIRE' or 'ATTACKED' or 'VOTED' in self.agent_talks[self.nthTalk][2]:
            #     pass
            # agent 0

            #to get the target list
            targ_list = list(map(int, re.findall(r'\d+', self.agent_talks[self.nthTalk][2])))
            string_list = self.agent_talks[self.nthTalk][2].split()
            # gets [6, 6] from "Agent6 COMINGOUT Agent6 SEER"

            if "VOTE" in self.agent_talks[self.nthTalk][2]:
                print('reached VOTE')
                voter = self.agent_talks[self.nthTalk][1]
                voted = targ_list[-1] #int( self.agent_talks[self.nthTalk][2][11:13] )
                for key_voted in self.estimate_votes:
                    if voter in self.estimate_votes[key_voted]:
                        self.estimate_votes[key_voted].remove(voter)
                self.estimate_votes[voted].add(voter)
                print(self.estimate_votes) #

            elif "COMINGOUT" in self.agent_talks[self.nthTalk][2]:
                print('reached COs') #
                who = self.agent_talks[self.nthTalk][1]
                # print(who)
                whot = targ_list[-1]
                subject = string_list[-1] #int( self.agent_talks[self.nthTalk][2][16:18] )
                # print(subject)

                if who == whot:
                    #self.COs[who].add(self.agent_talks[self.nthTalk][2][20:])
                    self.COs[who].add(subject)
                    # consider else if an agent CO for another is significant
                    #if self.agent_talks[self.nthTalk][2][20:] == "SEER" and not (who in self.seers):
                    if subject == "SEER" and not (who in self.seers):
                        #self.seers.add(self.agent_talks[self.nthTalk][1])
                        self.seers[self.agent_talks[self.nthTalk][1]] = 0
                        print('seers:')
                        print(self.seers) #

                    # elif self.agent_talks[self.nthTalk][2][20:] == "MEDIUM" and not (who in self.mediums):
                    elif subject == "MEDIUM" and not (who in self.mediums):
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
                target = targ_list[-1] #int(self.agent_talks[self.nthTalk][2][14:16])
                species = string_list[-1] #self.agent_talks[self.nthTalk][2][18:]
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
                target = targ_list[-1] #int(self.agent_talks[self.nthTalk][2][17:19])
                species = string_list[-1] #self.agent_talks[self.nthTalk][2][21:]
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
                pass
                #self.bodyguards.add(self.agent_talks[self.nthTalk][2][6:8])
        
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

        print('[0]')
        # estimate roles
        if self.role == "VILLAGER":
            print("[H] set player villager")
            #self.pt.setu(self.idx, "V/BG", 1)
            self.pt.wwa_prob(self.idx, 0)
            self.pt.pos_prob(self.idx, 0)

        print('[1]')
        # if only 1 medium CO that medium is trustworthy
        if len(self.mediums) == 1 and self.currentDay != 1:
            print("[H] if only 1 medium CO that medium is trustworthy: " + str(next(iter(self.mediums.keys()))))
            self.likely_medium.add( next(iter(self.mediums.keys())) )
            self.likely_human.add( next(iter(self.mediums.keys())) )
            #self.pt.setu(next(iter(self.mediums.keys())), "MEDIUM", 1)
            self.pt.wwa_prob(next(iter(self.mediums.keys())), 0)
            self.pt.pos_prob(next(iter(self.mediums.keys())), 0)
        
        # if only 1 seer CO that seer is trustworthy
        if len(self.seers) == 1 and self.currentDay != 1:
            print("[H] if only 1 seer CO that seer is trustworthy")
            self.likely_seer.add( next(iter(self.seers.keys())) )
            self.likely_human.add( next(iter(self.seers.keys())) )
            #self.pt.setu(next(iter(self.seers.keys())), "SEER", 1)
            self.pt.wwa_prob(next(iter(self.seers.keys())), 0)
            self.pt.pos_prob(next(iter(self.seers.keys())), 0)

        print('[2]')
        # those who div on day 1 WW are suspicous - 3/14 RNG
        if len(self.seers) > 1 and self.currentDay == 1:
            print("[H] those who div on day 1 WW are suspicous - 3/14 RNG")
            for sus in self.seers:
                if self.seers[sus] > 0:
                    self.likely_possessed.add(sus)
                    self.likely_werewolf.add(sus)
                    #self.pt.update(sus, "WEREWOLF", .5)
                    #self.pt.update(sus, "POSSESSED", .5)
                    self.pt.wwa_prob(sus, 11/14-self.pt.get_prob(sus)[0])
                    self.pt.pos_prob(sus, 11/14-self.pt.get_prob(sus)[1])
        print('[3]')
        # seers who CO and were killed are deemed innocent, the others are suspicous
        if len(self.seers) > 1:
            for inno in self.seers:
                if inno in self.killed:
                    print("[H] seers who CO and were killed are deemed innocent, the others are suspicous")
                    susSeers = self.seers.copy()  
                    susSeers.pop(inno)
                    for sus in susSeers:
                        self.likely_werewolf.add(sus)
                        #self.pt.update(sus, "POSSESSED", .25)
                        #self.pt.update(sus, "WEREWOLF", .25)
                        self.pt.wwa_prob(sus, self.beta * (1-self.pt.get_prob(sus)[0]))
                        self.pt.pos_prob(sus, self.beta * (1-self.pt.get_prob(sus)[0]))
                        

        print('[4]')
        # if someone divined us as WW they are likely WW or POS
        if self.currentDay > 1 and self.role == "VILLAGER":
            for sus in self.divined:
                if self.divined[sus] == [self.idx, 'WEREWOLF']:
                    print("[H] if someone divined us as WW they are likely WW or POS")
                    self.likely_werewolf.add(sus)
                    self.likely_possessed.add(sus)
                    #self.pt.update(sus, "POSSESSED", .5)
                    #self.pt.update(sus, "WEREWOLF", .5)
                    self.pt.wwa_prob(sus, 1)
                    self.pt.pos_prob(sus, .8 - self.pt.get_prob(sus)[1])

        print('[5]')
        # if killed, prob human 1
        for player in self.killed:
            self.likely_human.add(player)
            #self.pt.setu(player, "V/BG", 1)
            self.pt.wwa_prob(player, 0)
            self.pt.pos_prob(player, 0)
        
        print('[6]')
        if self.currentDay == 1 and len(self.seers) == 2:
            print("[H] 2 seers....")
            seersIter = iter(self.seers)
            seer1 = next(seersIter)
            seer2 = next(seersIter)
            if self.seers[seer1] == self.seers[seer2]:
                # self.pt.setu(localSeers[0], "SEER", .5)
                # self.pt.setu(localSeers[0], "POSSESSED", .25)
                # self.pt.setu(localSeers[0], "WEREWOLF", .25)
                # self.pt.setu(localSeers[1], "SEER", .5)
                # self.pt.setu(localSeers[1], "POSSESSED", .25)
                # self.pt.setu(localSeers[1], "WEREWOLF", .25)
                self.pt.wwa_prob(seer1, .5-self.pt.get_prob(seer1)[0])
                self.pt.wwa_prob(seer2, .5-self.pt.get_prob(seer2)[0])
                self.pt.pos_prob(seer1, .5-self.pt.get_prob(seer1)[1])
                self.pt.pos_prob(seer2, .5-self.pt.get_prob(seer2)[1])
            elif self.seers[seer1] > 0: #0 divined the werewolf..
                # self.pt.setu(localSeers[0], "SEER", 3/14)
                # self.pt.setu(localSeers[0], "POSSESSED", (11/14)/2)
                # self.pt.setu(localSeers[0], "WEREWOLF", (11/14)/2)
                # self.pt.setu(localSeers[1], "SEER", 11/14)
                # self.pt.setu(localSeers[1], "POSSESSED", (3/14)/2)
                # self.pt.setu(localSeers[1], "WEREWOLF", (3/14)/2)
                self.pt.wwa_prob(seer1, 11/14-self.pt.get_prob(seer1)[0])
                self.pt.wwa_prob(seer2, 3/14-self.pt.get_prob(seer2)[0])
                self.pt.pos_prob(seer1, 11/14-self.pt.get_prob(seer1)[1])
                self.pt.pos_prob(seer2, 3/14-self.pt.get_prob(seer2)[1])
            else: #1 divined the werewolf..
                # self.pt.setu(localSeers[1], "SEER", 3/14)
                # self.pt.setu(localSeers[1], "POSSESSED", (11/14)/2)
                # self.pt.setu(localSeers[1], "WEREWOLF", (11/14)/2)
                # self.pt.setu(localSeers[0], "SEER", 11/14)
                # self.pt.setu(localSeers[0], "POSSESSED", (3/14)/2)
                # self.pt.setu(localSeers[0], "WEREWOLF", (3/14)/2)
                self.pt.wwa_prob(seer2, 11/14-self.pt.get_prob(seer2)[0])
                self.pt.wwa_prob(seer1, 3/14-self.pt.get_prob(seer1)[0])
                self.pt.pos_prob(seer2, 11/14-self.pt.get_prob(seer2)[1])
                self.pt.pos_prob(seer1, 3/14-self.pt.get_prob(seer1)[1])
        
        print('[7]')
        #If a seer div the other as WW, increase p to be WW aligned as true seers do not need to divine the other fake seer as they know they are fake
        for seer in list(self.divined.keys()):
            if (self.divined[seer][0] in list(self.seers.keys())) and (self.divined[seer][1] == "WEREWOLF"):
                print("[H] If a seer div the other as WW, increase p to be WW aligned as true seers do not need to divine the other fake seer as they know they are fake")
                self.likely_possessed.add(seer)
                self.likely_werewolf.add(seer)
                #self.pt.update(seer, "WEREWOLF", .2)
                #self.pt.update(seer, "POSSESSED", .2)
                self.pt.wwa_prob(seer, .6 * (1-self.pt.get_prob(seer)[0]))
                self.pt.pos_prob(seer, .6 * (1-self.pt.get_prob(seer)[1]))

        #print('[7]')
        # #An agent is killed who was almost executed p HU??increase
        # if self.currentDay > 1:
        #     for targ in self.prev_estimate_votes:
        #         if len(self.prev_estimate_votes[self.prev_voted_out]) - len(self.prev_estimate_votes[targ]) < 2 and targ in self.killed: #almost voted out and killed
        #             print("[H] An agent is killed who was almost executed p HU??increase")
        #             #self.update(targ, "V/BG", .2)
        
        print('[8]')
        #An agent does not vote for who they say they were going to increase WW aligned
        #take union of each player estimate and votes
        try:
            liarList = [] 
            for player in self.votes:
                if player in self.estimate_votes:
                    liarUnion = self.votes[player].union(self.estimate_votes[player])
                    if len(liarUnion) > 0:
                        for liarUnionItem in liarUnion:
                            liarList.append(int(liarUnionItem))
            liarDuplicates = set([x for x in liarList if liarList.count(x) > 1])
            for liar in liarDuplicates:
                self.likely_possessed.add(liar)
                self.likely_werewolf.add(liar)
                #self.pt.update(liar, "WEREWOLF", .15)
                #self.pt.update(liar, "POSSESSED", .15)
                self.pt.wwa_prob(liar, self.beta * (1-self.pt.get_prob(liar)[0]))
                self.pt.pos_prob(liar, self.beta * (1-self.pt.get_prob(liar)[1]))
            print("LiarList: " + str(liarList))
            print("LiarDuplicates: " + str(liarDuplicates))
        except Exception: 
            print('Unrecoverable error regarding 8')
        

        print('[9]')
        #A seer is killed, likely true seer, earlier in the game is more uncertain
        for seer in self.seers:
            if seer in self.killed:
                print("[H] A seer is killed, likely true seer, earlier in the game is more uncertain [killed]")
                # if self.currentDay > 3:
                #     self.pt.update(liar, "SEER", .5)
                # else: #early game
                #     self.pt.update(liar, "SEER", .2)
                
                if len(self.seers) == 2: #other seer sus
                    #self.pt.update(next(iter(set(self.seers.keys()).difference({liar}))), "POSSESSED", .35)
                    self.pt.wwa_prob(next(iter(set(self.seers.keys()).difference({seer}))), .7-self.pt.get_prob(next(iter(set(self.seers.keys()).difference({seer}))))[0])
                    self.pt.pos_prob(next(iter(set(self.seers.keys()).difference({seer}))), .7-self.pt.get_prob(next(iter(set(self.seers.keys()).difference({seer}))))[1])
            if seer in self.executed:
                print("[H] A seer is killed, likely true seer, earlier in the game is more uncertain [executed]")
                self.pt.wwa_prob(seer, .7 * (1 - self.pt.get_prob(seer)[0]))
                self.pt.pos_prob(seer, .7 * (1 - self.pt.get_prob(seer)[1]))

        
        print('[10]')
        #A medium is executed, likely not true medium
        for medium in self.mediums:
            if medium in self.killed:
                print("[H] A medium is killed/executed [killed], likely true medium: " + str(medium))

                # if len(self.mediums) == 2: #other med sus
                #     #self.pt.update(next(iter(set(self.seers.keys()).difference({liar}))), "POSSESSED", .35)
                #     self.pt.wwa_prob(next(iter(set(self.mediums.keys()).difference({medium}))), .75 * (1-self.pt.get_prob(next(iter(set(self.seers.keys()).difference({medium}))))[0]))
                #     self.pt.pos_prob(next(iter(set(self.mediums.keys()).difference({medium}))), .75 * (1-self.pt.get_prob(next(iter(set(self.seers.keys()).difference({medium}))))[1]))
                #self.pt.update(medium, "MEDIUM", .5)
                if len(self.mediums) == 2: #other med sus
                    #self.pt.update(next(iter(set(self.seers.keys()).difference({liar}))), "POSSESSED", .35)
                    self.pt.wwa_prob(next(iter(set(self.mediums.keys()).difference({medium}))), .8-self.pt.get_prob(next(iter(set(self.mediums.keys()).difference({medium}))))[0])
                    self.pt.pos_prob(next(iter(set(self.mediums.keys()).difference({medium}))), .8-self.pt.get_prob(next(iter(set(self.mediums.keys()).difference({medium}))))[1])
            if medium in self.executed:
                print("[H] A seer is killed, likely true seer, earlier in the game is more uncertain [executed]")
                self.pt.wwa_prob(medium, .8 - self.pt.get_prob(medium)[0])
                self.pt.pos_prob(medium, .8  - self.pt.get_prob(medium)[1])

        print('[11]') #+ str(self.votes) + str(self.prev_votes) + "prevdead: " + str(self.prev_dead))
        #An agent votes for an accepted medium or seer, likely WW
        for player in self.alive:
            for medium in self.likely_medium:
                if medium in self.votes and player in self.votes[medium]:
                    print("[H] An agent votes for an accepted medium or seer, likely WW [M]")
                    #self.pt.update(liar, "WEREWOLF", .2)
                    #self.pt.update(liar, "POSSESSED", .2)
                    self.pt.wwa_prob(player, self.delta * (1-self.pt.get_prob(player)[0]))
                    self.pt.pos_prob(player, self.delta * (1-self.pt.get_prob(player)[1]))
            for seer in self.likely_seer:
                if seer in self.votes and player in self.votes[seer]:
                    print("[H] An agent votes for an accepted medium or seer, likely WW [S]")
                    #self.pt.update(liar, "WEREWOLF", .2)
                    #self.pt.update(liar, "POSSESSED", .2)
                    self.pt.wwa_prob(player, self.delta * (1-self.pt.get_prob(player)[0]))
                    self.pt.pos_prob(player, self.delta * (1-self.pt.get_prob(player)[1]))

        print('[12]')
        #An agent votes for someone who was executed next round
        if self.prev_dead in self.prev_votes and self.prev_dead != -1:
            if self.prev_dead in self.prev_votes.keys():
                for voter in self.prev_votes[self.prev_dead]:
                    print("[H] An agent votes for someone who was killed next round:" + voter)
                    #self.pt.update(voter, "POSSESSED", .3)
                    #self.pt.update(voter, "WEREWOLF", .3)
                    self.pt.wwa_prob(voter, self.epsilon * (1-self.pt.get_prob(voter)[0]))
                    self.pt.pos_prob(voter, self.epsilon * (1-self.pt.get_prob(voter)[0]))

        print('[13]')
        #A seer divines a werewolf as human (werewolf status declared by medium)
        
        for seer in self.divined:
            for seerPair in  self.divined[seer]:
                for medium in self.identified:
                    for mediumPair in self.identified[medium]:
                        if seerPair[0] == mediumPair[0] and seerPair[1] != mediumPair[1]: #same name different identities
                            print("[H] A seer divines a werewolf as human (werewolf status declared by medium)")
                            print(' - seer: ' + str(seer) + " medium: " + str(medium) + "target:" + str(seerPair[0]))
                            #self.pt.setu(seer, "POSSESSED", .5)
                            #self.pt.setu(seer, "WEREWOLF", .5) 
                            self.pt.wwa_prob(seer, 1)
                            self.pt.pos_prob(seer, 1)


        print("[+] reached end of update")
        # # role specific identification (in other classes)

            
    # Start of the day (no return)
    def dayStart(self):
        # keep track of number of times we have talked today 
        self.pt.display()
        self.talkTurn = 0 
        logging.debug("# DAYSTART")
        print('----------------------------------REACHED RESET---------------------------------- CURRENT DAY: ' + str(self.currentDay)) 
        print(self.alive) #
        print('DEAD:') #
        print(self.dead) #
        print('KILLED:') #
        print(self.killed) #
        print('EXECUTED:') #
        print(self.executed) #

        print('DIVINED')
        print(self.divined)
        print('SEERS')
        print(self.seers)
        print('IDENTIFIED')
        print(self.identified)

        # resets
        self.nthTalk = -1
        self.agent_talks = []
        self.prev_estimate_votes = self.estimate_votes.copy()
        self.estimate_votes = {player: set() for player in self.alive}
        self.votes = {player: set() for player in self.alive}
        self.prev_votes = self.votes.copy()
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
            print("DAY")
            print(int(self.base_info['day']))
            # day 1 talking logic
            if int(self.base_info['day']) == 1:
                #return cb.skip()
                # 30% CO Villager
                if not self.hasCO and self.role == 'VILLAGER' and len(self.requesters) == 0 and self.behavior <= 30:
                    self.hasCO = True
                    return cb.comingout('', self.idx, 'VILLAGER')
                elif self.talkTurn < 5:
                    if len(self.seers) > 1:
                        for targ in self.seers:
                            if self.seers[targ] > 0:
                                return cb.vote('', targ)
                        return cb.skip()
                    else:
                        return cb.skip()
                else: return cb.over()
            # day 2 talk logic
            elif int(self.base_info['day']) == 2:
                #return cb.skip()
                if len(self.seers) > 1:
                    for targ in self.seers:
                        if self.seers[targ] > 0 and targ in self.unaccused:
                            self.unaccused.remove(targ)
                            self.likely_werewolf.add(targ)
                            self.will_vote.append(targ)
                            return cb.logicalxor(self.idx, cb.estimate(self.idx, targ, "POSSESSED"), cb.estimate(self.idx, targ, "WEREWOLF"))
                    return cb.skip()
                elif len(self.seers) == 1 and next(iter(self.seers.values())) in self.unaccused:
                    self.unaccused.remove(next(iter(self.seers.values())))
                    self.likely_human.add(next(iter(self.seers.values())))
                    return cb.estimate('', next(iter(self.seers.values())), "SEER")
                else:
                    return cb.skip()
                
                    
            # late game logic
            #if int(self.base_info['day']) > 2:
            else:
                # if only one medium then estimate true medium 
                if len(self.likely_medium) == 1:
                    if self.true_medium_state == 0:
                        self.true_medium_state += 1
                        return cb.estimate('', list(self.likely_medium)[0], 'MEDIUM' )
                    #if self.true_medium_state == 1:
                    else:
                        self.repeatMediumLogic += 1
                        return cb.because(self.idx, cb.estimate(self.idx, list(self.likely_medium)[0], 'MEDIUM' ), cb.comingout(list(self.likely_medium)[0], list(self.likely_medium)[0], 'MEDIUM') )
                # if only one seer then estimate true seer
                elif len(self.likely_seer) == 1:
                    if self.true_seer_state == 0:
                        self.true_seer_state += 1
                        return cb.estimate('', list(self.likely_seer)[0], 'SEER' )
                    #if self.true_seer_state == 1:
                    else:
                        self.true_seer_state += 1
                        return cb.because(self.idx, cb.estimate(self.idx, list(self.likely_seer[0], 'SEER' )), cb.comingout(list(self.likely_seer)[0], list(self.likely_medium)[0], 'SEER') )
                # claim to vote someone, need probTable
                elif self.daily_push_vote < 3: 
                    # self.daily_push_vote += 1
                    # return cb.vote('', 1)
                    pass
                else: return cb.over() # talk
            return cb.over() # JH: You need this extra one because the 'if/else' structure allowed some situations where nothing returned
        else:
            return cb.over() # by default, ret over

    # targetted actions: Require the id of the target
    # agent as the return
    # act based on the lists
    def vote(self):
        logging.debug("# VOTE")
        self.pt.display()
        max = -1
        maxP = -1 #player with max value
        #second = -1

        for player in self.alive:
            if self.pt.get_prob(player)[0] > max:
                max = self.pt.get_prob(player)[0]
                maxP = player

        return maxP
                
        #first loop find max
        # for player in self.alive:
        #     if self.pt.get(player, "WEREWOLF") > max:
        #         max = self.pt.get(player, "WEREWOLF")
        #         maxP = player

        #     #remove if columns w & p merge
        #     if self.pt.get(player, "POSSESSED") > max:
        #         max = self.pt.get(player, "POSSESSED")
        #         maxP = player
        
        # #second loop find second max
        # for player in self.alive:
        #     if self.pt.get(player, "WEREWOLF") > second and self.pt.get(player, "WEREWOLF") != max:
        #         second = self.pt.get(player, "WEREWOLF")

        #     #remove if columns w & p merge
        #     if self.pt.get(player, "POSSESSED") > second and self.pt.get(player, "POSSESSED") != max:
        #         second = self.pt.get(player, "POSSESSED")
        
        #finally compare and decide if voting in majority
        
        # if max - second < .5 and self.currentDay < 4:
        #     #if day num low and difference small, vote majority
        #     majority = -1
        #     majorityP = -1
        #     for player in self.estimate_votes:
        #         if len(self.estimate_votes[player]) > majority:
        #             majority = len(self.estimate_votes[player])
        #             majorityP = player
        #     return majorityP

        # else:
        #     #difference great or day num high enough to have sufficient data..
        #     return maxP

        '''
        #OLD VOTE FUNCT
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
        '''

    # Finish (no return)
    def finish(self):
        logging.debug("# FINISH")
        return None