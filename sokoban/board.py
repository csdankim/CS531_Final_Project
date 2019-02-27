import copy

import actions


MOVES = ["U", "D", "L", "R"]


def gen_default_board():
    with open('boards.txt') as board_file:
        board = []
        for line in board_file:
            board.append(line.strip().split(","))
    return board


def draw_board(sokoban_board):
    for i in range(0,len(sokoban_board)):
        print(sokoban_board[i])


def draw_frontier(sokoban_frontier):
    for i in range(0, len(sokoban_frontier), 2):
        print("Direction: " + str(sokoban_frontier[i]))
        draw_board(sokoban_frontier[i+1])


def gen_frontier(frontier_board):
    current_frontier = []
    for i in range(0, len(MOVES)):
        board_frontier = copy.deepcopy(frontier_board)
        result = actions.move_agent(board_frontier, MOVES[i])
        if result:
            current_frontier.append(MOVES[i])
            current_frontier.append(result)
    return current_frontier

