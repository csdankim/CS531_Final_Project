import random
import time

import heuristic
import board

md_step = 0
hu_step = 0

def ida_run(evaluation_board,method):
    if method == "MD":
        ida_threshold = heuristic.manhattan_distance_node(evaluation_board)
    else:
        ida_threshold = heuristic.hungarian_method(evaluation_board)
    while True:
        search_result = ida_search_function(evaluation_board,0,ida_threshold,method)
        if (search_result == -1):
            return "GOAL"
        ida_threshold = search_result

def ida_search_function(node,g,threshold,method):
    global md_step
    global hu_step
    if method == "MD":
        f_value = g + heuristic.manhattan_distance_node(node)
        md_step += 1
    else:
        f_value = g + heuristic.hungarian_method(node)
        hu_step += 1
    if (f_value >threshold):
        return f_value
    if (board.check_goal(node)):
        print("IDA* Goal achieved:")
        if method == "MD":
            print("Steps: {}" .format(md_step))
        else:
            print("Steps: {}" .format(hu_step))
        board.draw_board(node)
        return -1

    min = float("inf")
    frontier = board.gen_frontier(node)
    for i in range(1, len(frontier), 2):
        tempvalue = ida_search_function(frontier[i], g+1, threshold, method)
        if (tempvalue == -1):
            return -1
        if (tempvalue < min):
            min = tempvalue
    return min
