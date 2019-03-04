import board
import heuristic
import math
import sys

infinity = math.inf


class F_node:
    def __init__(self,f_value,node):
        self.f = f_value
        self.n = node

    def __lt__(self, other):
        return self.f < other.f

    def __str__(self):
        return str(self.f)


def rbfs_run(evaluation_board):
    # reflects the layout of the RBFS evaluations
    initial_board = F_node(0, evaluation_board)
    return rbfs_search_function(initial_board, infinity)


def rbfs_search_function(f_node, f_limit):
    if board.check_goal(f_node.n):
        print("Goal Achieved:")
        return f_node.n
    frontier = board.gen_frontier(f_node.n)
    if len(frontier) == 0:
        return "FAILURE", infinity
    successors = []
    for i in range(1, len(frontier), 2):
        print(frontier[i])
        successors.append(F_node(max((1 + heuristic.manhattan_distance_node(frontier[i])), f_node.f), frontier[i]))
    while True:
        successors.sort()
        best_node = successors[0]
        if best_node.f > f_limit:
            return "FAILURE", best_node.f
        alternative = successors[1]
        result, best_node.f = rbfs_search_function(best_node, min(f_limit, alternative.f))
        if result != "FAILURE":
            return result
