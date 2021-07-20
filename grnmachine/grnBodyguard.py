"""
    Contains Body Guard Class
    07/'21
    James Hale
"""
import aiwolfpy
from aiwolfpy import contentbuilder as cb
import random
import grnVillager


class BodyGuard(grnVillager.Villager):
    def __init__(self, my_name):
        self.dead_seers = {"execute": list(), "dead": list()}
        self.dead_mediums = {"execute": list(), "dead": list()}
        super().__init__(my_name)

    def update(self, base_info, diff_data, request):
        for i in range(len(diff_data["type"])):
            if diff_data["type"][i] in self.dead_seers.keys():
                if diff_data["agent"][i] in self.mediums.keys():
                    self.dead_mediums[diff_data["type"][i]].append(diff_data["agent"][i])
                elif diff_data["agent"][i] in self.seers.keys():
                    self.dead_seers[diff_data["type"][i]].append(diff_data["agent"][i])
        super().update(base_info, diff_data, request)

    def guard(self):
        alive_mediums = [i for i in self.mediums.keys() if i not in self.dead_mediums["execute"] and i not in self.dead_mediums["dead"]]
        if len(alive_mediums) == 1 and not len(self.dead_mediums["dead"]):
            # Only 1 alive medium left, and none have been killed by WW
            # So, if you are the last Medium left, and the other Medium was not killed by WW (either executed or not
            # existing) we will protect
            return int(random.choice(alive_mediums))
        else:
            alive_seers = [i for i in self.seers.keys() if i not in self.dead_seers["execute"] and i not in self.dead_seers["dead"]]
            if len(alive_seers) == 1 and not len(self.dead_seers["dead"]):
                return int(random.choice(alive_seers))
        return int(random.sample(self.alive, 1)[0])
