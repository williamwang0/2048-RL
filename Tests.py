from qlearning import *
from game import GameField


agent = FQLearningAgent()
gamefield = GameField()

[gamefield.spawn() for x in range(10)]

[print(a) for a in gamefield.field]
print()
actions = ['Up', 'Left', 'Down', 'Right']
for act in actions:
    print()
    [print(a) for a in gamefield.sim_move('Up')[0]]
    print(str(act) + " : " + str(agent.getFeature(gamefield, act)))