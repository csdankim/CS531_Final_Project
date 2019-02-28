from IDA import *
import heapq   # for priority que (BFS)
import time
# from timeit import default_timer as timer


"""
    reference: https://courses.cs.washington.edu/courses/cse326/03su/homework/hw3/bestfirstsearch.html
    
    BFS Pseudocode
    
    Best-First-Search( Maze m )
        Insert( m.StartNode )
        Until PriorityQueue is empty    ## data structure: priority queue
            c <- PriorityQueue.DeleteMin
            If c is the goal
                Exit
            Else
                Foreach neighbor n of c
                    If n "Unvisited"
                        Mark n "Visited"
                        Insert( n )
                Mark c "Examined"
    End procedure
"""

"""
    reference: Textbook. Figure 3.26 The algorithm for recursive best-first search.
    
    function RECURSIVE-BEST-FIRST-SEARCH(problem) returns a solution, or failure
        return RBFS(problem,MAKE-NODE(problem.INITIAL-STATE),∞)
    
    function RBFS(problem, node, f limit ) returns a solution, or failure and a new f-cost limit
        if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
        successors ←[ ]
        for each action in problem.ACTIONS(node.STATE) do
            add CHILD-NODE(problem, node, action) into successors
        if successors is empty then return failure,∞   # the node is at the dead-end, thus unwind and set the the best alternative cost
        for each s in successors do /* update f with value from previous search, if any */
            s.f ←max(s.g + s.h, node.f ))
        loop do    # while True:
            best ←the lowest f-value node in successors    # best_f_val = node_f_cost[best_nodes[0]]
            if best .f > f limit then return failure, best .f     
                                                                    
                # if best_f_val > best_alt[curr_node]
                #     forward
                #     update_alt_cost = best_f_val
                # else 
                #     unwind  # need to implement
                #     update_alternative_cost = best_f_val
                # 
                # 
                # if len(best_nodes) == 2
                #     snd_best_f_val = node_f_cost[best_nodes[1]]
                #     if snd_best_f_val < best_alt[curr_node]
    
                                                                        
            alternative ←the second-lowest f-value among successors    # heapq.nsmallest(n, iterable, key=None) 
            result , best .f ←RBFS(problem, best , min( f limit, alternative))    # unwind
        if result = failure then return result
"""

"""
    reference: aima_code_python_search.py
    
    def recursive_best_first_search(problem, h=None):
        #[Figure 3.26]
        h = memoize(h or problem.h, 'h')
    
        def RBFS(problem, node, flimit):
            if problem.goal_test(node.state):
                return node, 0   # (The second value is immaterial)
            successors = node.expand(problem)
            if len(successors) == 0:    # the node is at the dead-end, thus unwind and set the best alternative cost 
                return None, infinity
            # if len(best_f) == 0:
            #   best_alt_cost = float('Infinity')
            for s in successors:
                s.f = max(s.path_cost + h(s), node.f)
            while True:
                # Order by lowest f value
                successors.sort(key=lambda x: x.f)
                best = successors[0]
                if best.f > flimit:
                    return None, best.f
                if len(successors) > 1:
                    alternative = successors[1].f
                else:
                    alternative = infinity
                print(node)
                result, best.f = RBFS(problem, best, min(flimit, alternative))
                if result is not None:
                    return result, best.f
    
        node = Node(problem.initial)
        node.f = h(node)
        result, best.f = RBFS(problem, node, infinity)
        return result
"""

## implement class recursive_best_first_search overriding IDAStar
## recursive
## BFS data structure : priority queue  https://docs.python.org/3/library/heapq.html

## problem 1: new node found, initialize its cost

## Problem 2: calculate, update, and assign best node cost value for local f_limit

## Problem 3: Problem 3: node expansion and unwind


class recursive_best_first_search(IDAStar):

    def solve(self, root, is_goal, max_cost = None):

        self.is_goal = is_goal
        self.path = [root]  # stack: recursion
        self.nodes_evaluated = 0
        self.h_time = 0

        curr_node = root
        curr_f_val = {}
        best_alt = {root: float('Infinity')}


        cpu_start = time.time()

        while True:
            self.nodes_evaluated += 1

            cpu_end = time.time()

            if cpu_end - cpu_start > 20:
                raise timelimit

            if self.is_goal(curr_node):
                return {
                    'Path': len(self.path) - 1,
                    'Nodes': self.nodes_evaluated,
                    # 'Moves': self.path_descrs,
                    # 'Cost': bound,
                    'Heuristic Running Time': self.h_time,
                    'Total Running Time': cpu_end - cpu_start
                }

            # recursive search start: its role is the same as IDAStar's _search
            node_f_cost = curr_f_val.get(curr_node, {})   # https://www.programiz.com/python-programming/methods/dictionary/get

            ## Problem 1: new node found, initialize its cost

            if not node_f_cost:
                curr_f_val[curr_node] = {}
                parent_g_val = len(self.path) - 1
                for cost, n, descr in self.neighbours(curr_node):

                     # for s in successors:
                     #    s.f = max(s.path_cost + h(s), node.f)

                    if n in best_alt: continue
                    # update node cost with g(parent) + cost + h(heuristics)
                    h_start = time.time()
                    h_val = self.h(n)
                    h_end = time.time()
                    self.h_time += (h_end - h_start)

                    curr_f_val[curr_node][n] = parent_g_val + cost + h_val

                node_f_cost = curr_f_val[curr_node]


            ## Problem 2: calculate, update, and assign best node cost value for local f_limit

            # best_nodes = a list of the two smallest node_f_costs
            # if the node is a leaf, unwind and set the best_alt to infinity
            # else
            #     best_f_val = node_f_cost[best_nodes[0]]   # assign best f val
            #     if best_f_val > best_alt[curr_node]       # compare f_val at the current node
            #         unwind # need to implement
            #         update_alt_cost = best_f_val          # update the alternative cost
            #     else
            #         forward
            #         update_alt_cost = best_f_val
            #
            #     if there are two best nodes, compare 2nd best node's f-value and curr_node's value
            #         snd_best_f_val = node_f_cost[best_nodes[1]]    # line 53 implementation
            #         if snd_best_f_val < best_alt[curr_node]
            #             update_alt_cost = snd_best_f_value

            unwind = True
            best_nodes = heapq.nsmallest(2, node_f_cost, key=node_f_cost.get)
                        # heapq.nsmallest(n, iterable, key=None)

            if len(best_nodes) == 0:     # reached at a leaf.
                update_alt_cost = float('Infinity')

            else:
                best_f_val = node_f_cost[best_nodes[0]]

                if best_f_val > best_alt[curr_node]:
                    update_alt_cost = best_f_val
                else:
                    unwind = False
                    update_alt_cost = best_alt[curr_node]

                if len(best_nodes) == 2:
                    snd_best_f_val = node_f_cost[best_nodes[1]]
                    if snd_best_f_val <= best_alt[curr_node]:
                        update_alt_cost = snd_best_f_val


            ## Problem 3: node expansion and unwind


            """
                Figure 3.27 from AIMA
                Stages in an RBFS search for the shortest route to Bucharest. The f-limit
                value for each recursive call is shown on top of each current node, and every node is labeled
                with its f-cost. (a) The path via Rimnicu Vilcea is followed until the current best leaf (Pitesti)
                has a value that is worse than the best alternative path (Fagaras). (b) The recursion unwinds
                and the best leaf value of the forgotten subtree (417) is backed up to Rimnicu Vilcea; then
                Fagaras is expanded, revealing a best leaf value of 450. (c) The recursion unwinds and the
                best leaf value of the forgotten subtree (450) is backed up to Fagaras; then Rimnicu Vilcea is
                expanded. This time, because the best alternative path (through Timisoara) costs at least 447,
                the expansion continues to Bucharest.
            """

            # ###############################################
            # warning!!: python is the script language!!! ###
            # ###############################################

            # if else:
            # unwind pseudo-code for implementation
            #
            # if
            # forward(node expansion)
            # move forward to the lowest f-value and continue
            #
            # else
            # unwind
            # Update curr_f_val of the parent_node with best_val
            # delete curr_node
            # unwind 1 step back toward parent_node
            # assign curr_node to parent_node

            if not unwind:   # forward(node expansion)
                nxt_node = best_nodes[0]  # the lowest f-value
                best_alt[nxt_node] = update_alt_cost
                self.path.append(nxt_node)
                curr_node = nxt_node
                continue

            else:   # unwind
                parent_node = self.path[-2]
                curr_f_val[parent_node][curr_node] = update_alt_cost
                del curr_f_val[curr_node]
                del best_alt[curr_node]
                self.path = self.path[:-1]
                curr_node = parent_node



# For debugging
#---------------------------------------------------------------------------------------------------------------------------------------------------

# if __name__ == "__main__":
#
#
#     solved_state = slide_solved_state(4)
#     neighbours = slide_neighbours(4)
#     is_goal = lambda p: p == solved_state
#
#     tests = [
#         (5,1,7,3,9,2,11,4,13,6,15,8,0,10,14,12),
#         (2,5,13,12,1,0,3,15,9,7,14,6,10,11,8,4),
#         (5,2,4,8,10,0,3,14,13,6,11,12,1,15,9,7),
#         (11,4,12,2,5,10,3,15,14,1,6,7,0,9,8,13),
#         (5,8,7,11,1,6,12,2,9,0,13,10,14,3,4,15)
#     ]
#
#
#     slide_solver = IDAStar(slide_wd(4, solved_state, hrst=True), neighbours)
#
#     for p in tests:
#         start = time.time()  # measure CPU time start
#         try:
#             results = slide_solver.solve(p, is_goal)
#             slide_print(p)
#             # print(", ".join({-1: "Left", 1: "Right", -4: "Up", 4: "Down"}[move[1]] for move in moves))
#             # print(cost, num_eval)
#             print('path {}\nnodes {}\nHeuristic Running Time {} sec'.format(results['Path'], results['Nodes'], results['Heuristic Running Time']))
#             end = time.time()  # measure CPU time end
#             proc_time = end - start
#             print('Total CPU Running Time {0} sec'.format(proc_time)) # measure total CPU time
#         except timelimit:
#             slide_print(p)
#             print('takes too long')