import board
import actions
import heuristic
import ida
import rbfs

import argparse


parser = argparse.ArgumentParser(description='Solve Sobokan puzzles')
parser.add_argument("-m", "--map",
                    dest="map_choice",
                    default="trivial_board.txt",
                    help="Choose a map file (default: trivial_board.txt)")

args = parser.parse_args()
new_board = board.gen_default_board(args.map_choice)
board.draw_board(new_board)
print("\n")

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
