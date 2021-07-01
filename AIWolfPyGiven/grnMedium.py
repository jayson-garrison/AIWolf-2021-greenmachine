"""
    Contains Medium Class
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
        self.to_report = None
        self.hasComeOut = False

    def initialize(self, base_info, diff_data, game_setting):
        grnVillager.initialize(base_info, diff_data, game_setting)

    def update(self, base_info, diff_data, request):
        if self.idx < 0:
            self.idx = base_info['agentIdx']
        if request == "DAILY_INITIALIZE":
            for i in range(len(diff_data["type"])):
                if diff_data["type"][i] == "identify":
                    self.to_report = (diff_data["agent"][i], diff_data["text"][i].split()[-1])

    def dayStart(self):
        grnVillager.dayStart()

    def talk(self):
        s = cb.over()
        if self.to_report is not None:
            if not self.hasComeOut:
                self.hasComeOut = True
                s = cb.comingout(self.idx, self.idx, "MEDIUM")
            else:
                s = cb.identified(self.idx, self.to_report[0], self.to_report[1])
                self.to_report = None
        return s

    def vote(self):
        return 1

    def divine(self):
        pass

    def guard(self):
        return 1

    def whisper(self):
        return cb.over()

    def attack(self):
        pass

    def finish(self):
        pass
