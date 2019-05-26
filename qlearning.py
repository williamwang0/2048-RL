import numpy as np
from collections import defaultdict
from game import *
import random

actions = ['Up', 'Left', 'Down', 'Right']
num_feats = 8


class QLearningAgent:
    def __init__(self):
        self.Q = {} # not sure if built-in dict can hash (s, a) pair, may need to fix/use modified dict
        self.epsilon = 1
        self.alpha = 1
        "maybe more instance variables? idk"

    def learn(self):
        #TODO
        return

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

    def getAction(self, state):
        """
          Compute the action to take in the current state.
          Explore with prob self.epsilon.
        """
        # Pick Action
        legalActions = [a for a in actions if state.sim_move(a)[0] != state]
        p = self.epsilon
        if not legalActions:
            return None
        greedy_flag = 0 # ASSIGN BERNOULLI COIN FLIP HERE #
        # my name is albert and im really smart cause i know what a bernoulli coin flip is
        if greedy_flag:
            return random.choice(legalActions)
        else:
            return self.computeActionFromQValues(state)

    def update(self, state, action, nextState, reward):
        """ this is the q-value update method; double check it """
        alpha = self.alpha
        sample = reward + self.discount * self.computeValueFromQValues(nextState)
        self.Q[(state, action)] = (1 - alpha) * self.getQValue(state, action) + alpha * sample



class FQLearningAgent:

    def __init__(self):
        self.weights = np.array([0 for x in range(num_feats)])

        self.gamma = 0.9
        self.alpha = 0.005
        self.explore = 0
        self.game_field = GameField(win=(2 ** 15))
        self.counts = [{} for _ in range(num_feats)]

    def learn(self):
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
            def exFunc(action):
                fv = self.getFeature(game_field, action)
                count = 1
                for i in range(num_feats):
                    if fv[i] in self.counts[i]:
                        count += 1
                return self.getQValue(game_field, action) + self.explore / count

            def regFunc(action):
                return self.getQValue(game_field, action)

            best_action = max([action for action in actions if game_field.move_is_possible(action)]
                              , key=exFunc)
            # add epsilon exploration later here #
            # new_field, reward = game_field.sim_move(best_action, True)

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

    def numAdj(self, board, ratio):
        """ takes in a board and a ratio.
            returns number of horizontally adjacent pairs with that ratio """
        counter = 0
        for x_val in range(len(board)):
            for rat in self.rowRatios(board, x_val):
                try:
                    if rat == ratio or (1 / rat) == ratio:
                        counter += 1
                except ZeroDivisionError:
                    pass
        return counter

    def rowIncr(self, ratios):
        """ returns whether ratios is monotonically increasing """
        if not ratios:
            return False
        if ratios[0] < 1:
            for rat in ratios:
                if rat >= 1:
                    return False
            return True
        else:
            for rat in ratios:
                if rat < 1:
                    return False
            return True

    def rowRatios(self, board, rowNum):
        """ returns a list of the ratios between each number on 'board' in row 'rowNum' """
        row = board[rowNum]
        result = []
        for i in range(len(row) - 1):
            try:
                result.append(row[i] / row[i + 1])
            except ZeroDivisionError:
                pass
        return result

    def getFeature(self, s, a):
        """ returns feature value calculation of a q-state
        1. Merges
        2. Biggest Num in Corner (0 or 1)
        3. Adjacent Pairs that differ by a factor of 2
        4. Adjacent Pairs that are equal
        5. Max Tile
        6. Monotonically increasing along a field edge
        7. Log(sum) of tiles
        8. Max near corner"""
        prev_board = s.field
        new_board = s.sim_move(a)[0]
        feature_vector = []

        # Merges, Open Tiles, Biggest Num in Corner
        prev_open = 0
        max_num = 0

        big_num_in_corner = 0

        open_tiles = -1

        for y in prev_board:
            for x in y:
                if x == 0:
                    prev_open += 1

        for y in new_board:
            for x in y:
                if x == 0:
                    open_tiles += 1
                if x > max_num:
                    max_num = x

        merges = open_tiles - prev_open + 1

        if new_board[0][0] == max_num:
            big_num_in_corner = 1

        if new_board[len(new_board) - 1][0] == max_num:
            big_num_in_corner = 1

        if new_board[0][len(new_board) - 1] == max_num:
            big_num_in_corner = 1

        if new_board[len(new_board) - 1][len(new_board) - 1] == max_num:
            big_num_in_corner = 1

        feature_vector.extend([merges, big_num_in_corner])

        #Adjacent Pairs differ by a Factor of 2
        double_count = 0
        double_count += self.numAdj(new_board, 2)
        double_count += self.numAdj(transpose(new_board), 2)
        feature_vector.append(double_count)

        #Adjacent Pairs that are equal
        equal_count = 0
        equal_count += self.numAdj(new_board, 1)
        equal_count += self.numAdj(transpose(new_board), 1)
        feature_vector.append(equal_count)

        #Max Tile
        feature_vector.append(np.log2(max_num))

        #Monotonically Increasing along an edge
        row0Incr = self.rowIncr(self.rowRatios(new_board, 0))
        row3Incr = self.rowIncr(self.rowRatios(new_board, 3))
        col0Incr = self.rowIncr(self.rowRatios(transpose(new_board), 0))
        col3Incr = self.rowIncr(self.rowRatios(transpose(new_board), 3))
        feature_vector.append(any([row0Incr, row3Incr, col0Incr, col3Incr]))

        #Sum Tiles
        feature_vector.append(np.log(sum([sum(x) for x in new_board])))


        #Biggest Number in one of 8 corners?
        def max_near_corner(board, max_num):
            if board[0][1] == max_num:
                return 1
            if board[1][0] == max_num:
                return 1
            if board[0][len(board) - 2] == max_num:
                return 1
            if board[len(board)-1][1] == max_num:
                return 1
            if board[len(board) - 2][0] == max_num:
                return 1
            if board[len(board) - 1][1] == max_num:
                return 1
            if board[len(board) - 1][len(board) - 2] == max_num:
                return 1
            if board[len(board) - 2][len(board) - 1] == max_num:
                return 1
            return 0

        feature_vector.append(max_near_corner(new_board, max_num))

        # EXPLORATION FUNCTION SUPPORT
        fv = feature_vector
        for i in range(num_feats):
            if fv[i] not in self.counts[i]:
                self.counts[i][fv[i]] = 1
            else:
                self.counts[i][fv[i]] += 1

        return np.array(feature_vector)

    def getQValue(self, s, a):
        """ returns dot-product of feature vector with weight vector """
        return sum(self.weights * self.getFeature(s, a))

    def update(self, s1, a, s2, r):
        """ updates weights based on transition """
        diff = r + (self.gamma * max([self.getQValue(s2, act) for act in actions])) \
               - self.getQValue(s1, a)
        self.weights = self.weights + (self.alpha * diff * self.getFeature(s1, a))


def __main__():
    agent = FQLearningAgent()
    for i in range(100):
        mean_max_tile = 0
        for _ in range(20):
            agent.learn()
            mT = agent.game_field.maxTile()
            print(mT, agent.weights)
            mean_max_tile += mT
        print(mean_max_tile / 20)


    # print(agent.weights)

__main__()
