import board
import actions
import heuristic
import ida
import rbfs

# specify board file here
board_selection = "easy_board.txt"
ida_limit = 40

new_board = board.gen_default_board(board_selection)
board.draw_board(new_board)
print("\n")

print("Running IDA* with Manhattan Distance heuristic")
ida.ida_run(new_board, ida_limit,"MD")
print("Running IDA* with Hungarian heuristic")
new_board = board.gen_default_board(board_selection)
ida.ida_run(new_board, ida_limit,"HU")
print("Running RBFS with Manhattan Distance heurisitc")
new_board = board.gen_default_board(board_selection)
rbfs.rbfs_run(new_board,"MD")
print("Running RBFS with Hungarian heurisitc")
new_board = board.gen_default_board(board_selection)
rbfs.rbfs_run(new_board,"HU")
