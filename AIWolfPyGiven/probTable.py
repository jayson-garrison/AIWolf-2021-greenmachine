# make a class that is a probability table that performs conditional probability updates based on 
# information to determine each player's probability to be a certain role.

# idea: create a base class that takes the role as a variable, thus it can be a Werewolf, Seer, etc.
# (only consider important roles that actually effect decision making, so no need to determine probabilities
# for villagers), and calculate the distribution based on actions that are associated with a likely role.