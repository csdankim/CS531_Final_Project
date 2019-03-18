import board
import ida
import rbfs
import mcts

import argparse
import sys

parser = argparse.ArgumentParser(description='Solve Sobokan puzzles')
parser.add_argument("-m", "--map",
                    dest="map_choice",
                    default="boards/test_board1.txt",
                    help="Choose a map file (default: trivial_board.txt)")


args = parser.parse_args()
new_board = board.gen_default_board(args.map_choice)


print("Running IDA* with Manhattan Distance heuristic")
ida.ida_run(new_board,"MD")
print("Running IDA* with Hungarian heuristic")
new_board = board.gen_default_board(args.map_choice)
ida.ida_run(new_board,"HU")
print("Running RBFS with Manhattan Distance heurisitc")
new_board = board.gen_default_board(args.map_choice)
rbfs.rbfs_run(new_board,"MD")
print("Running RBFS with Hungarian heurisitc")
new_board = board.gen_default_board(args.map_choice)
rbfs.rbfs_run(new_board,"HU")
print("Running MCTS")
new_board = board.gen_default_board(args.map_choice)
mcts.run_mcts(new_board)
