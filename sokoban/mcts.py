import board
import heuristic
import math
import copy
import random

loss_threshold = 1000

class MCTS_node:
    def __init__(self, parent=None, move=None, this_board=None):
        self.move = move
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.current_board = this_board
        self.untried_moves = self.getMoves()

    def __str__(self):
        self.ratio_string = str(self.wins) + "/" + str(self.visits)
        return str(self.ratio_string)

    def select_child(self):
        board.draw_frontier(self.frontier)
        unsorted = []
        for i in range(1, len(self.frontier), 2):
            unsorted.append(self.frontier[i])
        s = sorted(unsorted, key = lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]

    def add_child(self,move):
        child = MCTS_node(parent=self, move=move)
        return child

    def update(self,result):
        self.visits += 1
        self.wins += result

    def getMoves(self):
        the_moves = []
        frontier = board.gen_frontier(self.current_board)
        for i in range(0, len(frontier), 2):
            the_moves.append(frontier[i])
        return the_moves

def UCT(rootstate, itermax):
    root_node = MCTS_node(this_board=rootstate)
    for i in range(0, itermax):
        node = root_node
        curr_state = copy.deepcopy(rootstate)

