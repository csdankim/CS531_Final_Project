from RBFS import *

"""
from the instruction of the assignment

For m= 10, 20, 30, 40, 50 do  
    For n=10 random problems p generated by Scramble(m) 
      For the two algorithms A
        For each heuristic function h, 
            Solve p using A and h 
            Record the length of the solution found, the number of nodes 
               searched, and the total CPU time spent on evaluating
               the heuristic and on solving the whole problem. 
"""

def main():
    solved_state = slide_solved_state(4)  # n X n grid, n=4
    neighbours = slide_neighbours(4)
    is_goal = lambda p: p == solved_state

    for m in [10, 20, 30, 40, 50]:
        for n in range(10):
            scramble_puzzle = slide_randomize(solved_state, m, neighbours)  # by Scramble(m)
            for algorithm in [IDAStar, recursive_best_first_search]:
                for heuristic_function in [True, False]:
                    slide_solver = algorithm(slide_wd(4, solved_state, hrst=heuristic_function), neighbours)
                    results = slide_solver.solve(scramble_puzzle, is_goal)
                    print('{},{},{},{},{},{},{},{}'.format(n + 1, m, algorithm, heuristic_function, results['Path'],
                                                           results['Nodes'], results['Heuristic Running Time'],
                                                           results['Total Running Time']))

if __name__ == "__main__":
    main()
