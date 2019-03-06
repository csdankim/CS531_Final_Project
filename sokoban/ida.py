import random
import time

import heuristic
import board

def ida_run(evaluation_board,MAX_ITERATIONS,method):
    if method == "MD":
        ida_threshold = heuristic.manhattan_distance_node(evaluation_board)
    else:
        ida_threshold = heuristic.hungarian_method(evaluation_board)
    while True:
        search_result = ida_search_function(evaluation_board,0,ida_threshold,MAX_ITERATIONS,method)
        if (search_result == -1):
            return "GOAL"
        ida_threshold = search_result

def ida_search_function(node,g,threshold,MAX_ITERATIONS,method):
    if method == "MD":
        f_value = g + heuristic.manhattan_distance_node(node)
    else:
        f_value = g + heuristic.hungarian_method(node)
    if (f_value >threshold):
        return f_value
    if (board.check_goal(node)):
        print("Goal achieved:")
        board.draw_board(node)
        return -1
    min = int(MAX_ITERATIONS) + 1
    frontier = board.gen_frontier(node)
    for i in range(1,len(frontier),2):
        tempvalue = ida_search_function(frontier[i],g+1,threshold,MAX_ITERATIONS,method)
        if (tempvalue == -1):
            return -1
        if (tempvalue < min):
            min = tempvalue
    return min
