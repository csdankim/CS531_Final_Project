def gen_default_board():
    with open('boards.txt') as board_file:
        board = []
        for line in board_file:
            board.append(line.strip().split(","))
    return board


def draw_board(sokoban_board):
    for i in range(0,len(sokoban_board)):
        print(sokoban_board[i])


