from math import *

import board
import heuristic
import actions
import copy
import random
import sys

loss_threshold = 1000

class MCTS_node:
    def __init__(self, parent=None, move=None, this_board=None):
        self.move = move
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.current_board = this_board
        self.untried_moves = self.getMoves(this_board)

    def __str__(self):
        self.ratio_string = str(self.wins) + "/" + str(self.visits)
        return str(self.ratio_string)

    def select_child(self):
        s = sorted(self.children, key=lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s

    def add_child(self, move, state):
        child = MCTS_node(parent=self, move=move, this_board=state)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    def update(self,result):
        self.visits += 1
        self.wins += result

    def getMoves(self,board_selection):
        the_moves = []
        frontier = board.gen_frontier(board_selection)
        for i in range(0, len(frontier), 2):
            the_moves.append(frontier[i])
        return the_moves


def UCT(rootstate, itermax):
    root_node = MCTS_node(this_board=rootstate)

    for i in range(0, itermax):
        node = root_node
        curr_state = copy.deepcopy(root_node)

        # select
        # terminal state: loss (corner box) or win (all goals satisfied)
        while node.untried_moves == [] and not (board.check_goal(node.current_board) or board.check_loss(node.current_board)):
            node = node.select_child()
            curr_state.current_board = actions.move_agent(node.current_board, node.move)

        # expand
        if node.untried_moves != []:
            move = random.choice(node.untried_moves)
            curr_state.current_board = actions.move_agent(curr_state.current_board, move)
            node = node.add_child(move, curr_state.current_board)

        # autobots, roll out
        while not (board.check_loss(curr_state.current_board) or board.check_goal(curr_state.current_board)):
            curr_state.current_board = actions.move_agent(curr_state.current_board, random.choice(curr_state.getMoves(curr_state.current_board)))

        # backpropagate
        while node != None:
            if board.check_goal(curr_state.current_board):
                node.update(1.0)
            elif board.check_loss(curr_state.current_board):
                node.update(0.0)
            else:
                raise ValueError("Backpropagate: Not Terminal")
            node = node.parent

    return sorted(root_node.children, key=lambda c: c.visits)[-1]
