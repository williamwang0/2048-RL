import numpy as np

class FQLearningAgent:

    def __init__(self):
        self.weights = np.array([0, 0, 0, 0])

    def getFeature(self, s, a):
        """ returns feature value calculation of a q-state """
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