def manhattan_distance(frontier):
    total_md = []
    for item in range(0,len(frontier)):
        if isinstance(frontier[item], list):
            curr_frontier_goals = []
            curr_frontier_boxes = []
            for row in range(0,len(frontier[item])):
                for column in range(0, len(frontier[item][row])):
                    if frontier[item][row][column] == '0':
                        curr_frontier_goals.append(row)
                        curr_frontier_goals.append(column)
                    if frontier[item][row][column] == '3':
                        curr_frontier_boxes.append(row)
                        curr_frontier_boxes.append(column)
            frontier_md = 0
            for box_evals in range(0, len(curr_frontier_boxes), 2):
                best_goal_distance = -1
                for goal_evals in range(0, len(curr_frontier_goals), 2):
                    distance_x = abs(int(curr_frontier_boxes[int(box_evals)]) - int(curr_frontier_goals[int(goal_evals)]))
                    distance_y = abs(int(curr_frontier_boxes[int(box_evals)+1]) - int(curr_frontier_goals[int(goal_evals)+1]))
                    curr_goal_md = distance_x + distance_y
                    if (curr_goal_md < best_goal_distance) or (best_goal_distance is -1):
                        best_goal_distance = curr_goal_md
                # after this loop, the box has been associated with the best distance
                frontier_md = frontier_md + best_goal_distance
            # after this loop, we have the sum of the best distances
            total_md.append(frontier_md)
    print(total_md)
    return total_md

def displaced_distance(frontier):
    pass
