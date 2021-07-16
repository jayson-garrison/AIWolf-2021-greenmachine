import numpy as np


class ProbabilityTable:
    def __init__(self, roles, players, role_types):
        self.table = np.zeros((len(players), len(roles.keys())))
        for i in range(len(players)):
            for j in range(len(role_types)):
                self.table[i, j] = roles[role_types[j]] / len(players)
        self.rows = self.table.shape[0]
        self.columns = self.table.shape[1]

    def add(self, i, j, d):
        """

        :param i:
        :param j:
        :param d:
        :return: void
        """
        if self.table[i, j] + d > 1:
            d = 1 - self.table[i, j]
        elif self.table[i, j] + d < 0:
            d = -self.table[i, j]
        self.table[i, j] += d
        self.propagate(i, j, d)

    def propagate(self, i, j, d, depth=0, max_depth=3, tol=.000001):
        """
            We should either do max depth or tolerance
        """
        if depth < max_depth:
            for ii in range(self.table.shape[0]):
                for jj in range(self.table.shape[1]):
                    pass_d = 0
                    if ii == i:
                        if jj != j:
                            x = self.table[ii, jj] - d / (self.columns-1)
                        else:
                            x = self.table[ii, jj]
                    elif jj == j:
                        x = self.table[ii, jj] - d / (self.rows-1)
                    else:
                        x = self.table[ii, jj] + d / ((self.rows-1) * (self.columns-1))
                    if x < 0:
                        pass_d = 0 - x
                        x = 0
                    elif x > 1:
                        pass_d = 1 - x
                        x = 1
                    self.table[ii, jj] = x
                    if abs(0-pass_d) > tol:  # If pass_d is not close to 0 (if I check equal to zero, the thing never converges)
                        # print(pass_d)
                        self.propagate(ii, jj, pass_d, depth=depth+1, max_depth=max_depth, tol=tol)

    def display(self):
        print(self.table)

    def verify(self):
        print("Verify rows")
        for i in range(len(self.table[:, 0])):  # Rows
            print(sum(self.table[i, :]))
        print("Verify columns")
        for i in range(len(self.table[0, :])):  # Columns
            print(sum(self.table[:, i]))


def main():
    """
        Main
    :return: void
    """
    a = ProbabilityTable({"Werewolf": 3, "Possessed": 1, "Villager": 8, "Bodyguard": 1, "Medium": 1, "Seer": 1},
                         ["Player1", "Player2", "Player3", "Player4", "Player5", "Player6", "Player7", "Player8",
                          "Player9", "Player10", "Player11", "Player12", "Player13", "Player14", "Player15"],
                         ["Werewolf", "Possessed", "Villager", "Bodyguard", "Medium", "Seer"])
    a.verify()
    for i in range(15):
        for j in range(6):
            a.add(i, j, .9)
    # a.add(4, 4, .9)
    a.display()
    a.verify()


if __name__ == '__main__':
    main()
