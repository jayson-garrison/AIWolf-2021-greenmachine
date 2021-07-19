import numpy as np
import random


class ProbabilityTable:
    def __init__(self, roles, players):
        self.table_possessed = np.zeros(len(players))
        self.table_werewolf = np.zeros(len(players))  # WW Aligned
        self.fixed_poss = np.zeros(self.table_possessed.size)
        self.fixed_were = np.zeros(self.table_werewolf.size)
        for i in range(self.table_possessed.size):
            self.table_possessed[i] = roles["Possessed"] / self.table_possessed.size
            self.table_werewolf[i] = (roles["Werewolf"] + roles["Possessed"]) / self.table_werewolf.size
        self.expected_poss = sum(self.table_possessed)
        self.expected_were = sum(self.table_werewolf)

    def pos_prob(self, index, increment):
        index -= 1
        if not sum(self.fixed_poss * self.table_possessed):
            if increment == 0 or increment == 1:
                self.fixed_poss[index] = 1
                self.table_possessed[index] = increment
            else:
                self.table_possessed[index] += (1-self.table_possessed[index]) * increment
            self.propagate(self.table_possessed, self.fixed_poss, index, self.expected_poss)

    def wwa_prob(self, index, increment):
        index -= 1
        if not sum(self.fixed_were * self.table_werewolf) > 3:
            if increment == 0 or increment == 1:
                self.fixed_were[index] = 1
                self.table_werewolf[index] = increment
            else:
                self.table_werewolf[index] += (1 - self.table_werewolf[index]) * increment
            self.propagate(self.table_werewolf, self.fixed_were, index, self.expected_were)

    def propagate(self, to_normalize, fixed_positions, index, expected):
        non_zero_one = fixed_positions.size - sum(fixed_positions)
        alpha = (expected - sum(fixed_positions * to_normalize) - to_normalize[index] * (1-fixed_positions[index])) \
                / (sum((1-fixed_positions) * to_normalize) - to_normalize[index] * (1-fixed_positions[index]))
        if non_zero_one - 1:
            for i in range(to_normalize.size):
                if not fixed_positions[i] and index != i:
                    to_normalize[i] *= alpha

    def get_prob(self, agent_id):
        return self.table_werewolf[agent_id-1], self.table_possessed[agent_id-1]

    def display(self):
        print("Werewolf")
        print(self.table_werewolf)
        print("Possessed")
        print(self.table_possessed)

    def verify(self):
        print("Werewolf verify")
        print(sum(self.table_werewolf))
        print("Possessed verify")
        print(sum(self.table_possessed))


def main():
    """
        Main
    :return: void
    """
    a = ProbabilityTable({"Werewolf": 3, "Possessed": 1, "Villager": 8, "Bodyguard": 1, "Medium": 1, "Seer": 1},
                         ["Player1", "Player2", "Player3", "Player4", "Player5", "Player6", "Player7", "Player8",
                          "Player9", "Player10", "Player11", "Player12", "Player13", "Player14", "Player15"],
                        )
    a.display()
    a.verify()
    a.wwa_prob(1, 0)
    a.wwa_prob(2, 0)
    a.wwa_prob(3, 0)
    a.wwa_prob(4, 0)
    for i in range(5, 16):
        a.wwa_prob(i, random.random())
        a.pos_prob(i, random.random())
        a.display()
    a.display()
    a.verify()
    print(a.get_prob(15))


if __name__ == '__main__':
    main()
