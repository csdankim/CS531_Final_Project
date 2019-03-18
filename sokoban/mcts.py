from math import *
from collections import deque

import time
import board
import actions
import copy
import random
import numpy as np

class MCTS_node:
    def __init__(self, parent=None, move=None, this_board=None, simple_dead_pos=None):
        self.move = move
        self.parent = parent
        self.children = []
        self.wins = 0
        self.loss = 0
        self.visits = 0
        self.current_board = this_board
        self.untried_moves = self.getMoves(this_board, simple_dead_pos)
        self.ressq = 0
        self.simple_dead_pos = simple_dead_pos

    def __str__(self):
        self.ratio_string = str(self.wins) + "/" + str(self.visits)
        return str(self.ratio_string)

    def select_child(self):
        if self.parent == None:
            s = sorted(self.children, key=lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits) + sqrt((c.ressq - c.visits*(c.wins/c.visits)**2 + 10000.)/c.visits))[-1]
        else:
            s = sorted(self.children, key=lambda c: c.wins/c.visits + sqrt(2*log(self.parent.visits)/c.visits) + sqrt((c.ressq - c.visits*(c.wins/c.visits)**2 + 10000.)/c.visits))[-1]
        return s

    def add_child(self, move, state, simple_dead_state):
        child = MCTS_node(parent=self, move=move, this_board=state, simple_dead_pos=self.simple_dead_pos)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    def update(self,result):
        self.visits += 1
        self.wins += result
        self.ressq += result**2

    def getMoves(self,board_selection, simple_dead_pos):
        the_moves = []
        frontier = board.gen_frontier(board_selection)
        #print("frontier")
        for i in range(0, len(frontier), 2):
            if not simple_deadlock(frontier[i], simple_dead_pos) and not board.freeze_deadlock(frontier[i]):
                the_moves.append(frontier[i])
        return the_moves


def UCT(rootstate, itermax, simple_dead_pos):

    root_node = MCTS_node(this_board=rootstate)

    step_count = 0

    for i in range(itermax):
        node = root_node
        #print(i)
        # BUG: it always resets the whole state, which means a child action way down the line
        # is being applied to the VERY FIRST state, which can be an invalid move
        # I think we need a complete reset! We must make sure the curr_state has the original
        # possible moves!
        # curr_state = copy.deepcopy(root_node)
        original_state = copy.deepcopy(rootstate)
        curr_state = MCTS_node(this_board=original_state)

        # select
        # terminal state: loss (corner box) or win (all goals satisfied)
        while node.untried_moves == []:
            # if we got here, the last choice led to a terminal state
            # so we need to try another child of node
            node = node.select_child()
            curr_state.current_board = node.current_board

        if board.check_goal(curr_state.current_board):
            print("MCTS Goal Achieved")
            print("Steps:{}, Iterations:{}".format(step_count, i))
            break

        # expand
        expansion_state =copy.deepcopy(curr_state)
        if node.untried_moves != []:
            move = random.choice(node.untried_moves)
            node = node.add_child(move, curr_state.current_board, simple_dead_pos)
            expansion_state.current_board = actions.move_agent(expansion_state.current_board, move)
            node = node.add_child(move, expansion_state.current_board, simple_dead_pos)

        state_calculation = copy.deepcopy(curr_state)
        # autobots, roll out (while state is non terminal)
        random_child = []
        random_child = random.choice(state_calculation.getMoves(state_calculation.current_board, simple_dead_pos))
        depth = 0
        state_result = False
        while random_child != [] and depth < 100:
            step_count += 1
            state_calculation.current_board = actions.move_agent(
                state_calculation.current_board,
                random_child)
            if board.check_goal(state_calculation.current_board):
                print("MCTS Goal Achieved")
                print("Steps:{}, Iterations:{}".format(step_count, i))
                state_result = True
                break
            if simple_deadlock(state_calculation.current_board, simple_dead_pos) or board.freeze_deadlock(state_calculation.current_board):
                break
            del random_child
            random_child = random.choice(state_calculation.getMoves(state_calculation.current_board, simple_dead_pos))
            depth += 1
        if state_result:
            break

        # backpropagate
        goal_check = False
        while node != None :
            if board.check_goal(state_calculation.current_board):
                node.update(3.0)
                node.t = node.visits
                goal_check = True
                break
            elif simple_deadlock(node.current_board, simple_dead_pos):
                node.update(-3.0)
                node.t = node.visits
            elif board.freeze_deadlock(node.current_board):
                node.update(-1.0)
                node.t = node.visits
            else:
                node.update(0.5)
                node.t = node.visits
            #else:
            #    raise ValueError("Backpropagate: Not Terminal")
            node = node.parent

        if goal_check:
            print("MCTS Goal Achieved")
            print("Steps:{}, Iterations:{}".format(step_count, i))
            break

    return sorted(root_node.children, key=lambda c: c.visits)[-1]


def run_mcts(sokoban_board):

    simple_dead_position = corner_deadlock(sokoban_board)
    simple_dead_position += edge_deadlock(sokoban_board)

    the_moves = []
    frontier = board.gen_frontier(sokoban_board)
    for i in range(0, len(frontier), 2):
        the_moves.append(frontier[i])
    UCT(rootstate=sokoban_board, itermax=100000, simple_dead_pos=simple_dead_position)
    print("Game over!")


def edge_deadlock(board):

    dead_position = []

    flag1 = True
    for column in range(1, len(board[1])):
        if board[1][column] == "0" or board[1][column] == "1" or board[1][column] == "2":
            flag1 = False
    if flag1:
        for column in range(1, len(board[1])):
            dead_position.append(1)
            dead_position.append(column)

    flag2 = True
    for column in range(1, len(board[len(board)-2])):
        if board[len(board)-2][column] == "0" or board[len(board)-2][column] == "1" or board[len(board)-2][column] == "2":
            flag2 = False
    if flag2:
        for column in range(1, len(board[len(board)-2])):
            dead_position.append(len(board)-2)
            dead_position.append(column)

    flag3 = True
    for row in range(1, len(board)):
        if board[row][1] == "0" or board[row][1] == "1" or board[row][1] == "2":
            flag3 = False
    if flag3:
        for row in range(1, len(board)):
            dead_position.append(row)
            dead_position.append(1)

    flag4 = True
    #print(len(board[1])-2)
    #print(len(board)-2)
    for row in range(1, len(board)-2):
        if board[row][len(board[row])-2] == "0" or board[row][len(board[row])-2] == "1" or board[row][len(board[row])-2] == "2":
            flag4 = False
    if flag4:
        for row in range(1, len(board)):
            dead_position.append(row)
            dead_position.append(len(board[row])-2)

    #print(dead_position)
    return dead_position

def corner_deadlock(board):

    dead_position = []

    for row in range(1, len(board)):
        for column in range(1, len(board[row])):
            flag = False
            if board[row][column] == "3":
                if board[row+1][column] == "-1" and board[row][column-1] == "-1":
                    flag = True
                if board[row+1][column] == "-1" and board[row][column+1] == "-1":
                    flag = True
                if board[row-1][column] == "-1" and board[row][column-1] == "-1":
                    flag = True
                if board[row-1][column] == "-1" and board[row][column+1] == "-1":
                    flag = True
            if flag:
                dead_position.append(row)
                dead_position.append(column)
    return dead_position

def simple_deadlock(board, deadlock_map):

    for row in range(0, len(board)):
        for column in range(0, len(board[row])):
            if board[row][column] == "3":
                for idx in range(0, len(deadlock_map), 2):
                    if row == deadlock_map[idx] and column == deadlock_map[idx+1]:
                        return True
    return False

