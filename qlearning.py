import numpy as np

class FQLearningAgent:

    def __init__(self):
        self.weights = np.array([0, 0, 0, 0])

    def getFeature(self, s, a):
        """ returns feature value calculation of a q-state
        1. Merges
        2. Open Tiles
        3. Biggest Num in Corner (0 or 1)
        4. Adjacent Pairs that differ by a factor of 2 """
        prev_board = s.field
        new_board = s.sim_move(a)[0]
        feature_vector = []

        #Merges, Open Tiles, Biggest Num in Corner
        prev_open = 0
        max_num = 0

        big_num_in_corner = 0
        merges = 0
        open_tiles = 0

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

        merges = open_tiles - prev_open

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
        count = 0

        for x in new_board:
            for y_index in range(len(x) - 1):
                y_ratio =  x[y_index] / x[y_index + 1]
                if y_ratio == 0.5 or y_ratio == 2:
                    count = count + 1

        for y in new_board:
            for x_index in range(len(y) - 1):
                x_ratio =  y[x_index] / y[x_index + 1]
                if x_ratio == 0.5 or x_ratio == 2:
                    count = count + 1

        feature_vector.append(count)


        return

    def getQValue(self, s, a):
        """ returns dot-product of feature vector with weight vector """
        return sum(self.weights * self.getFeature(s, a))

    def update(self, s1, a, s2, r):
        """ updates weights based on transition """
        
        return


class State:

    def __init__(self, f=None, s=0):
        self.field = f
        self.score = s

    def setField(self, f):
        self.field = f

    def setScore(self, s):
        self.score = s

def main(stdscr):
    curses.use_default_colors()
    game_field = GameField(win=2048)
    state_actions = {}  # Init, Game, Win, Gameover, Exit

    def init():
        game_field.reset()
        return 'Game'

    state_actions['Init'] = init

    def not_game(state):
        game_field.draw(stdscr)
        action = get_user_action(stdscr)
        responses = defaultdict(lambda: state)
        responses['Restart'], responses['Exit'] = 'Init', 'Exit'
        return responses[action]

    state_actions['Win'] = lambda: not_game('Win')
    state_actions['Gameover'] = lambda: not_game('Gameover')

    def game():
        game_field.draw(stdscr)
        action = get_user_action(stdscr)
        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action):  # move successful
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        return 'Game'

    state_actions['Game'] = game

    state = 'Init'
    while state != 'Exit':
        state = state_actions[state]()