def move_agent(board, direction):
    result_square = ""
    for row in range(0, len(board)):
        for column in range(0, len(board[row])):
            if board[row][column] == "4" or board[row][column] == "1":
                if board[row][column] == "4":
                    is_goal = False
                else:
                    is_goal = True
                agent_row = row
                agent_column = column
                if direction == "L":
                    result_square = board[row][column-1]
                    target_row = row
                    target_column = column - 1
                elif direction == "R":
                    result_square = board[row][column+1]
                    target_row = row
                    target_column = column + 1
                elif direction == "U":
                    result_square = board[row-1][column]
                    target_row = row - 1
                    target_column = column
                elif direction == "D":
                    result_square = board[row+1][column]
                    target_row = row + 1
                    target_column = column
                else:
                    raise ValueError("Bad directionection!")
    # result_square has what is there now!
    if result_square == "-1":
        # there is a wall, we cannot move!
        return False
    elif result_square == "0":
        board[target_row][target_column] = "1"
        if is_goal:
            board[agent_row][agent_column] = "0"
        else:
            board[agent_row][agent_column] = "5"
        return board
    elif result_square == "5":
        board[target_row][target_column] = "4"
        if is_goal:
            board[agent_row][agent_column] == "0"
        else:
            board[agent_row][agent_column] = "5"
        return board
    elif result_square == "3" or result_square == "2":
        if result_square == "3":
            is_box_goal = False
        else:
            is_box_goal = True
        # we also have to check if we can move the box or not ... ugh
        if direction == "L":
            box_result_square = board[agent_row][agent_column-2]
            box_target_row = agent_row
            box_target_column = agent_column - 2
        elif direction == "R":
            box_result_square = board[agent_row][agent_column+2]
            box_target_row = agent_row
            box_target_column = agent_column + 2
        elif direction == "U":
            box_result_square = board[agent_row-2][agent_column]
            box_target_row = agent_row - 2
            box_target_column = agent_column
        elif direction == "D":
            box_result_square = board[agent_row+2][agent_column]
            box_target_row = agent_row + 2
            box_target_column = agent_column
        # now we have the box result, let us see if we can move it to that square!
        if box_result_square == "5":
            board[box_target_row][box_target_column] = "3"
            if is_box_goal:
                board[target_row][target_column] = "1"
            else:
                board[target_row][target_column] = "4"
            if is_goal:
                board[agent_row][agent_column] = "0"
            else:
                board[agent_row][agent_column] = "5"
            return board
        elif box_result_square == "0":
            board[box_target_row][box_target_column] = "2"
            if is_box_goal:
                board[target_row][target_column] = "1"
            else:
                board[target_row][target_column] = "4"
            if is_goal:
                board[agent_row][agent_column] = "0"
            else:
                board[agent_row][agent_column] = "5"
            return board
        elif box_result_square == "-1" or box_result_square == "2" or box_result_square == "3":
            # we hit a wall, a box, or a goal that has a box on it, so we cannot move this specific box!
            return False
