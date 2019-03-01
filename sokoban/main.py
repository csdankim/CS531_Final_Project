import board
import actions
import heuristic
import ida

new_board = board.gen_default_board()
board.draw_board(new_board)
print("\n")

# After some manual testing I found that it takes
# 7 moves at best to reach it
result = ida.ida_run(new_board, 7)
