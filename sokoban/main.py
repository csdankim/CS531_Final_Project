import board
import actions
import heuristic
import ida

new_board = board.gen_default_board()
board.draw_board(new_board)
print("\n")

# generate the frontier nodes
frontier = board.gen_frontier(new_board)
frontier = board.gen_frontier(frontier[3])
frontier = board.gen_frontier(frontier[3])
frontier = board.gen_frontier(frontier[1])
frontier = board.gen_frontier(frontier[1])
frontier = board.gen_frontier(frontier[5])
frontier = board.gen_frontier(frontier[1])
#board.draw_frontier(frontier)
#print(board.check_goal(frontier[3]))

result = ida.ida_run(new_board, 7)
