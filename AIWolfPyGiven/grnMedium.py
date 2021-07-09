"""
    Contains Medium Class
    07/'21
    James Hale
    Proportion of times werewolves attack who they vote for
    Voting compared with kill choice (Do the werewolves act stupid?)
    Trust reduction for people who voted for me
"""

import aiwolfpy
from aiwolfpy import contentbuilder as cb
import grnVillager


class Medium(grnVillager.Villager):
    def __init__(self, my_name):
        super().__init__(my_name)
        self.name = my_name
        self.idx = -1  # Our agent ID
        self.to_report = list()
        self.hasComeOut = False
        self.id_player_roles = {}
        self.accuse_as_werewolf = list()
        self.to_vote = list()

    def initialize(self, base_info, diff_data, game_setting):
        super().initialize(base_info, diff_data, game_setting)

    def update(self, base_info, diff_data, request):
        """
            I think i need to reset between rounds
        :param base_info:
        :param diff_data:
        :param request:
        :return:
        """

        if self.idx < 0:
            self.idx = base_info['agentIdx']
        print(request)
        print(diff_data)
        for i in range(len(diff_data["type"])):
            if diff_data["type"][i] == "identify":
                agent_id = diff_data["agent"][i]
                agent_role = diff_data["text"][i].split()[-1]
                self.to_report.append((agent_id, agent_role))
                if agent_role in self.id_player_roles.keys():
                    self.id_player_roles[agent_role].append(agent_id)
                else:
                    self.id_player_roles[agent_role] = [agent_id]
            elif diff_data["type"][i] == "talk":
                split_text = diff_data["text"][i].split()
                if "COMINGOUT" in split_text and split_text[-1] == "MEDIUM" and int(diff_data["agent"][i]) != self.idx:
                    self.accuse_as_werewolf.append((diff_data["agent"][i], "WEREWOLF"))
                    self.to_vote.append(diff_data["agent"][i])
        super().update(base_info, diff_data, request)


    def dayStart(self):
        super().dayStart()

    def talk(self):
        if int(self.base_info['day']) == 1 and not self.hasComeOut:  # We take precedence to come out on day 1
            self.hasComeOut = True
            return cb.comingout(self.idx, self.idx, "MEDIUM")
        elif len(self.to_report):  # If we have anything to report, report it
            curr = self.to_report.pop(0)  # I guess we identify the executed players but not the attacked
            return cb.identified(self.idx, curr[0], curr[1])
        elif len(self.accuse_as_werewolf):
            curr = self.accuse_as_werewolf.pop(0)
            return cb.estimate(self.idx, curr[0], curr[1])
        return super().talk()  # If nothing else, return the original talk() (may come out as villager)

    def vote(self):
        if len(self.to_vote):
            print("HIIIIII")
            return int(self.to_vote.pop(0))
        return super().vote()  # If we have noone in mind, vote as villager

    def divine(self):
        return super().divine()

    def guard(self):
        return super().guard()

    def whisper(self):
        return super().whisper()

    def attack(self):
        return super().attack()

    def finish(self):
        return super().finish()
