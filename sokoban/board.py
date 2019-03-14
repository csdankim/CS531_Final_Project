import copy

import actions

MOVES = ["U", "D", "L", "R"]


def gen_default_board(board_file_selection):
    with open(board_file_selection) as board_file:
        board = []
        for line in board_file:
            board.append(line.strip().split(","))
    return board

def check_goal(sokoban_board):
    for row in range(0,len(sokoban_board)):
        for column in range(0,len(sokoban_board[row])):
            # in these cases, we have an agent on a goal or a goal without
            # anything on it, indicating a failure
            # the goal state is when there are no goal squares without a box
            if sokoban_board[row][column] == "1":
                return False
            if sokoban_board[row][column] == "0":
                return False
    return True

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
        result = []
        if board_frontier != True and board_frontier != False:
            result = actions.move_agent(board_frontier, MOVES[i])
        if result:
            current_frontier.append(MOVES[i])
            current_frontier.append(result)
    return current_frontier


# for MCTS, find out if our board is in a loss state:
# a loss is when we have a box in a corner, which means it cannot be moved
# so we cannot recover the box, and our current state is unsolvable
def check_loss(board):
    for row in range(0, len(board)):
        for column in range(0, len(board[row])):
            if board[row][column] == "3":
                # we have a box, let's see if it is permanently stuck
                # we check simple deadlock
                if board[row+1][column] == "-1" and board[row][column-1] == "-1":
                    return True
                if board[row+1][column] == "-1" and board[row][column+1] == "-1":
                    return True
                if board[row-1][column] == "-1" and board[row][column-1] == "-1":
                    return True
                if board[row-1][column] == "-1" and board[row][column+1] == "-1":
                    return True
                '''if board[row][column-1] == "-1" and board[row+1][column] == "-1":
                    # corner blocking from left and bottom
                    return True
                if board[row][column-1] == "-1" and board[row-1][column] == "-1":
                    # corner blocking from left and above
                    return True
                if board[row-1][column] == "-1" and board[row][column+1] == "-1":
                    # corner blocking from right and above
                    return True
                if board[row+1][column] == "-1" and board[row][column+1] == "-1":
                    # corner blocking from right and below
                    return True'''
    return False

# we check freeze deadlock
def freeze_deadlock(board):
    for row in range(0, len(board)):
        for column in range(0, len(board[row])):
            if board[row][column] == "3":
                if board[row][column+1] == "3" and ((board[row-1][column] == "-1" or "2") or (board[row+1][column] == "-1" or "2")):
                    if board[row-1][column+1] == "-1" or board[row+1][column+1] == "-1":
                        return True
                if board[row+1][column] == "3" and ((board[row][column-1] == "-1" or "2") or (board[row][column+1] == "-1" or "2")):
                    if board[row+1][column-1] == "-1" or board[row+1][column+1] == "-1":
                        return True
    return False