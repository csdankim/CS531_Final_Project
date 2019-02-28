import board
import actions
import heuristic

new_board = board.gen_default_board()
board.draw_board(new_board)
print("\n")

# generate the frontier nodes
print("Frontier:")
frontier = board.gen_frontier(new_board)
board.draw_frontier(frontier)
heuristic.manhattan_distance(frontier)
