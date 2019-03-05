import board
import heuristic
import math
import sys
import random

loss_threshold = 1000

class MCTS_node:
    def __init__(self,f_value,node,cost):
        self.n = node
        self.w = wins
        self.l = losses

    def __lt__(self, other):
        return self.f < other.f

    def __str__(self):
        self.ratio_string = str(self.w) + "/" + str(self.l)
        return str(self.ratio_string)


def simulate_tree():
    pass
