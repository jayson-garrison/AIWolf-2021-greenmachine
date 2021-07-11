import aiwolfpy
from aiwolfpy import contentbuilder as cb
import grnVillager
import random
import logging, json

class CheatCodes(object):
    #CONSTRUCTOR
    #rows = number of rows (players)
    #columnNameList = list of all column names to pass later, and the number of them there are
    # - keys: column names (roles)
    # - values: number of players in that role, or role set
    # - example: ["WEREWOLF":3, "S/M":2, "B/V":9, "POSSESSED":1]
    def __init__(self, columnNameDict) :
        self.columnNameDict = columnNameDict
        self.numPlayers = sum(columnNameDict.values())
        self.labels = list(columnNameDict.keys())
        self.table = [ [ columnNameDict[j] / self.numPlayers for j in self.labels ] for i in range(0,self.numPlayers)]

    #gets an item from the probability table
    #player = player numner
    #columnName = column name (from columnList), not number
    def get(self, player, columnName):
        row = player - 1
        try:
            col = self.labels.index(columnName)
        except:
            print("[-] Error in cheatcodes get(): make sure column name in column list")
            return

        return self.table[row][col]
    
    #gets an item from the probability table
    #player = player numner
    #columnName = column name (from columnList), not number
    #value = value you would like to set at the specified place
    def setl(self, player, columnName, value):
        row = player - 1
        try:
            col = self.labels.index(columnName)
        except:
            print("[-] Error in cheatcodes set(): make sure column name in column list")
            return

        self.table[row][col] = value
        return


    def update(self, player, columnName, value):
        row = player - 1
        try:
            col = self.labels.index(columnName)
        except:
            print("[-] Error in cheatcodes set(): make sure column name in column list")
            return
        #[1] update the target
        self.table[row][col] += value

        #[2] update the target's row (iterate over roles)
        nocol = list(range(0, len(self.table[row])))
        nocol.remove(col)
        for colIter in nocol:
            self.table[row][colIter] -= value / (len(self.table[row]) - 1)   #self.columnNameDict[columnName] - 1
            
        #[3] update the target's column
        norow = list(range(0, len(self.table)))
        norow.remove(row)
        for rowIter in norow:
            self.table[rowIter][col] -= value / (len(self.table) - 1)

        #[4] update the rest
        norow = list(range(0, len(self.table)))
        norow.remove(row)
        for rowIter in norow:
            nocol = list(range(0, len(self.table[row])))
            nocol.remove(col)
            for colIter in nocol:
                self.table[rowIter][colIter] += value / ((len(self.table) - 1) * (len(self.table[row]) - 1))

    def setu(self, player, columnName, value):
        incrimentVal = value - self.get(player, columnName)
        return self.update(player, columnName, incrimentVal)

    def print(self):
        print('------- Cheat Codes Table -------')
        print(self.labels)
        for i in self.table:
            print(i) 
        print('---------------------------------')
    
'''
inst = CheatCodes({"POSSESSED":1, "WEREWOLF":3, "S/M":2})
for i in inst.table:
    print(i) 
print('--------------')
inst.setu(2, "POSSESSED", 1)
for i in inst.table:
    print(i) 
print("howdy")
inst.print()
'''
