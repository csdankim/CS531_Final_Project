import board
import actions
import heuristic
import ida
import rbfs

new_board = board.gen_default_board()
board.draw_board(new_board)
print("\n")

# After some manual testing I found that it takes
# 7 moves at best to reach it
print("Running IDA* with Manhattan Distance heuristic")
ida.ida_run(new_board, 7,"MD")
print("Running IDA* with Hungarian heuristic")
new_board = board.gen_default_board()
ida.ida_run(new_board, 7,"HU")
print("Running RBFS with Manhattan Distance heurisitc")
new_board = board.gen_default_board()
rbfs.rbfs_run(new_board,"MD")
print("Running RBFS with Hungarian heurisitc")
new_board = board.gen_default_board()
rbfs.rbfs_run(new_board,"HU")
