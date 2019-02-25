import board
import actions

new_board = board.gen_default_board()
board.draw_board(new_board)
print("\n")
# L for left, R for right, U for up, D for down!
result = actions.move_agent(new_board, "R")
if result:
    board.draw_board(result)
else:
    print("The requested move failed!")
    board.draw_board(new_board)

