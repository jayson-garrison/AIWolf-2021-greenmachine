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
    def guard(self):
        if self.mediums.keys():
            return int(random.choice(list(self.mediums.keys())))
        return int(random.sample(self.alive, 1)[0])
