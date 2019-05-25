import numpy as np
from collections import defaultdict
from game import *

actions = ['Up', 'Left', 'Down', 'Right']


class FQLearningAgent:

    def __init__(self):
        self.weights = np.array([0, 0, 0, 0, 0])
        self.gamma = 0.6
        self.alpha = 0.005
        self.explore = 20
        self.game_field = GameField(win=(2 ** 15))
        self.counts = [{} for _ in range(5)]

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
                for i in range(5):
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
        for x_val in board:
            try:
                for rat in self.rowRatios(board, x_val):
                    if rat == ratio or (1 / rat) == ratio:
                        counter += 1
            except ZeroDivisionError:
                pass
        return counter

    def rowIncr(self, ratios):
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
        row = board[rowNum]
        return [row[i] / row[i + 1] for i in range(len(row) - 1)]


    def getFeature(self, s, a):
        """ returns feature value calculation of a q-state
        1. Merges
        2. Open Tiles
        3. Biggest Num in Corner (0 or 1)
        4. Adjacent Pairs that differ by a factor of 2
        5. Adjacent Pairs that are equal
        6. Max Tile
        7. Monotonically increasing along a field edge """
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

        feature_vector.extend([merges, open_tiles, big_num_in_corner])

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

        #Monotonically Increasing along an edge
        row0Incr = self.rowIncr(self.rowRatios(new_board, 0))
        row3Incr = self.rowIncr(self.rowRatios(new_board, 3))
        col0Incr = self.rowIncr(self.rowRatios(transpose(new_board), 0))
        col3Incr = self.rowIncr(self.rowRatios(transpose(new_board), 3))
        feature_vector.append(any([row0Incr, row3Incr, col0Incr, col3Incr]))

        # EXPLORATION FUNCTION SUPPORT
        fv = feature_vector
        for i in range(5):
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
    mean_max_tile = 0
    for _ in range(100):
        agent.learn()
        mT = agent.game_field.maxTile()
        print(mT, agent.weights)
        mean_max_tile += mT
    print(mean_max_tile / 100)


    # print(agent.weights)

__main__()
