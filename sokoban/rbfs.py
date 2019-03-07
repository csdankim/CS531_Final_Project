import board
import heuristic
import math

infinity = math.inf


class F_node:
    def __init__(self,f_value,node,cost):
        self.f = f_value
        self.n = node
        self.c = cost

    def __lt__(self, other):
        return self.f < other.f

    def __str__(self):
        return str(self.f)


def rbfs_run(evaluation_board,method):
    # reflects the layout of the RBFS evaluations
    initial_board = F_node(0, evaluation_board, 0)
    rbfs_search_function(initial_board, infinity, 0, method)


def rbfs_search_function(f_node, f_limit, depth, method):
    if board.check_goal(f_node.n):
        print("Goal Achieved:")
        board.draw_board(f_node.n)
        return "SUCCESS", f_node.f
    frontier = board.gen_frontier(f_node.n)
    if len(frontier) == 0:
        return "FAILURE", infinity
    successors = []
    for i in range(1, len(frontier), 2):
        if method == "MD":
            successors.append(F_node(max((depth + heuristic.manhattan_distance_node(frontier[i])), f_node.f), frontier[i], depth))
        else:
            successors.append(F_node(max((depth + heuristic.hungarian_method(frontier[i])), f_node.f), frontier[i], depth))
    while True:
        successors.sort()
        best_node = successors[0]
        if best_node.f > f_limit:
            return "FAILURE", best_node.f
        if len(successors) == 1:
            alternative = successors[0]
        else:
            alternative = successors[1]
        result, best_node.f = rbfs_search_function(best_node, min(f_limit, alternative.f),depth+1,method)
        if result != "FAILURE":
            return result, best_node.f
