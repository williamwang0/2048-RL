import numpy as np
from game import *
import random

actions = ['Up', 'Left', 'Down', 'Right']
num_feats = 8


class QLearningAgent:
    def __init__(self):
        self.Q = {} # not sure if built-in dict can hash (s, a) pair, may need to fix/use modified dict
        self.epsilon = 0.1
        self.alpha = 0.005
        self.game_field = GameField(win=(2 ** 15))
        self.discount = 0.85
        "maybe more instance variables? idk"

    def learn(self):

        """ COPY-PASTED FROM APPROX Q-LEARNING AGENT """

        """ trains agent on 1 game instance """
        self.game_field = GameField(win=(2 ** 15))
        game_field = self.game_field
        state_actions = {}  # Init, Game, Win, Gameover, Exit

        def init():
            game_field.reset()
            return 'Game'

        state_actions['Init'] = init

        def not_game(state):
            # game_field.draw(stdscr)
            # action = get_user_action(stdscr)
            action = 'Exit'
            responses = defaultdict(lambda: state)
            responses['Restart'], responses['Exit'] = 'Init', 'Exit'
            return responses[action]

        state_actions['Win'] = lambda: not_game('Win')
        state_actions['Gameover'] = lambda: not_game('Gameover')

        def game():

            best_action = self.getAction(game_field)

            prev_score = game_field.score
            prev_game_field = deepcopy(game_field)

            if game_field.move(best_action):
                if game_field.is_win():
                    return 'Win'
                if game_field.is_gameover():
                    return 'Gameover'
                reward = (game_field.score - prev_score)
                self.update(prev_game_field, best_action, game_field, reward)

            return 'Game'

        state_actions['Game'] = game

        state = 'Init'
        while state != 'Exit':
            state = state_actions[state]()

    def getQValue(self, state, action):
        """ Returns Q(state,action); Should return 0.0 if we have never seen a state """
        if (state, action) not in self.Q:
            return 0.0
        return self.Q[(state, action)]

    def computeValueFromQValues(self, state):
        """ this is the V(s) value, found from Q(s, a) values """
        actions = self.getLegalActions(state)
        if not actions:
            return 0
        return max([self.getQValue(state, a) for a in actions])

    def computeActionFromQValues(self, state):
        """ finding the optimal action given current Q(s, a) values """
        actions = self.getLegalActions(state)
        if not actions:
            return None
        best_q_value = self.computeValueFromQValues(state)
        best_actions = [a for a in actions if self.getQValue(state, a) == best_q_value]
        return random.choice(best_actions)

    def getLegalActions(self, state):
        """ returns a list of legal actions for the current state """
        return [a for a in actions if state.sim_move(a)[0] != state]

    def getAction(self, state):
        """
          Compute the action to take in the current state.
          Explore with prob self.epsilon.
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        p = self.epsilon
        if not legalActions:
            return None
        greedy_flag = random.random()
        if greedy_flag < self.epsilon:
            return random.choice(legalActions)
        else:
            return self.computeActionFromQValues(state)

    def update(self, state, action, nextState, reward):
        """ this is the q-value update method; double check it """
        alpha = self.alpha
        sample = reward + self.gamma * self.computeValueFromQValues(nextState)
        self.Q[(state, action)] = (1 - alpha) * self.getQValue(state, action) + alpha * sample
        # update self.alpha?? (slowly decrease it)


def __main__():
    agent = QLearningAgent()
    for i in range(100):
        mean_max_tile = 0
        for _ in range(20):
            agent.learn()
            mT = agent.game_field.maxTile()
            #print(mT, agent.weights)
            mean_max_tile += mT
        print(mean_max_tile / 20)


    # print(agent.weights)

__main__()
