from qlearning import *
from game import GameField


agent = FQLearningAgent()
gamefield = GameField()

[gamefield.spawn() for x in range(10)]
print("Original Board: ")

[print(x) for x in gamefield.field]

print()
actions = ['Up', 'Left', 'Down', 'Right']

[print(str(a) + " : " + str(agent.getFeature(gamefield, a))) for a in actions]