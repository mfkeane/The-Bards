class Player:
    
    # Constants
    EMPTY = '-'
    WHITE = 'O'
    BLACK = '@'
    CORNER = 'X'
    
    def _init_(self, colour):
    
        dimension = 8
        board = ["X------X",
                 "--------",
                 "--------",
                 "--------",
                 "--------",
                 "--------",
                 "--------",
                 "X------X"]
    
        my_pos  = []
        opp_pos = []
        
        my_dead  = 0
        opp_dead = 0
        
        if colour == "white":
            y_start = range(0,6)
            my_colour = WHITE
            opp_colour = BLACK
        elif colour == "black":
            y_start = range(2,8)
            my_colour = BLACK
            opp_colour = WHITE
              
            # Check if piece already partially surrounded
    #   and mark goal positions for Player
    def find_goal_pos(self, goals, flanks, x, y):

        # If no Player pieces surround Opponent,
        #   all surrounding tiles are valid goals

        if (x+1 in range(8)) and (board[y][x+1] is EMPTY):
            goals.append((x+1, y))
        if (x-1 in range(8)) and (board[y][x-1] is EMPTY):
            goals.append((x-1, y))
        if (y+1 in range(8)) and (board[y+1][x] is EMPTY):
            goals.append((x, y+1))
        if (y-1 in range(8)) and (board[y-1][x] is EMPTY):
            goals.append((x, y-1))

        # If piece already surrounded by one Player piece,
        #   or is next to a CORNER, opposite square is goal

        if ((x+1 in range(8)) and (x-1 in range(8)) and ((board[y][x+1] is
           my_colour) or board[y][x+1] is CORNER)):
            goals.append((x-1, y))
            if board[y][x+1] is my_colour and (x+1,y) in attackers:
                flanks.append(attackers.pop(attackers.index((x+1, y))))
            if (x,y+1) in goals:
                goals.remove((x,y+1))
            if (x,y-1) in goals:
                goals.remove((x,y-1))

        if ((x-1 in range(8)) and (x+1 in range(8)) and ((board[y][x-1] is
           my_colour) or board[y][x-1] is CORNER)):
            goals.append((x+1, y))
            if board[y][x-1] is my_colour and (x-1,y) in attackers:
                flanks.append(attackers.pop(attackers.index((x-1, y))))
            if (x,y+1) in goals:
                goals.remove((x,y+1))
            if (x,y-1) in goals:
                goals.remove((x,y-1))

        if ((y+1 in range(8)) and (y-1 in range(8)) and ((board[x][y+1] is
           my_colour) or board[y+1][x] is CORNER)):
            goals.append((x, y-1))
            if board[y+1][x] is my_colour and (x,y+1) in attackers:
                flanks.append(attackers.pop(attackers.index((x, y+1))))
            if (x+1,y) in goals:
                goals.remove((x+1,y))
            if (x-1,y) in goals:
                goals.remove((x-1,y))

        if ((y-1 in range(8)) and (y+1 in range(8)) and ((board[x][y-1] is
           my_colour) or board[y-1][x] is CORNER)):
            goals.append((x, y+1))
            if board[y-1][x] is my_colour and (x,y-1) in attackers:
                flanks.append(attackers.pop(attackers.index((x, y-1))))
            if (x+1,y) in goals:
                goals.remove((x+1,y))
            if (x-1,y) in goals:
                goals.remove((x-1,y))

        # if Opponent on edge of board
        if ((x+1 not in range(8)) and ((y+1 in range(8) and board[y+1][x] is
           EMPTY) and ((y-1 in range(8)) and board[y-1][x] is EMPTY))):
            goals.append((x,y+1))
            goals.append((x,y-1))
            if (x-1,y) in goals:
                goals.remove((x-1,y))

        if ((x-1 not in range(8)) and ((y+1 in range(8) and board[y+1][x] is
           EMPTY) and ((y-1 in range(8)) and board[y-1][x] is EMPTY))):
            goals.append((x,y+1))
            goals.append((x,y-1))
            if (x+1,y) in goals:
                goals.remove((x+1,y))

        if ((y+1 not in range(8)) and ((x+1 in range(8) and board[y][x+1] is
           EMPTY) and ((x-1 in range(8)) and board[y][x-1] is EMPTY))):
            goals.append((x+1,y))
            goals.append((x-1,y))
            if (x,y-1) in goals:
                goals.remove((x,y-1))

        if ((y-1 not in range(8)) and ((x+1 in range(8) and board[y][x+1] is
           EMPTY) and ((x-1 in range(8)) and board[y][x-1] is EMPTY))):
            goals.append((x+1,y))
            goals.append((x-1,y))
            if (x,y+1) in goals:
                goals.remove((x,y+1))


        for goal in goals:
            WatchYourBack.remove_kamikaze(goal)

        return [goals, flanks]
    
    # remove any goals that will result in white's death
    def remove_kamikaze(self, goal):
        x = goal[0]
        y = goal[1]

        if (x in range(1,7) and (board[y][x+1] is opp_colour
            and board[y][x-1] is opp_colour) and
           ((x+2 in range(8) and board[y][x+2] is not my_colour) or (x+2 not in
           range(8))) and
           ((x-2 in range(8) and board[y][x-2] is not my_colour) or (x+2 not in
           range(8)))):

            remove_goal_pos(goals, x, y)

        if (y in range(1,7) and (board[y+1][x] is opp_colour
           and board[y-1][y] is opp_colour) and
           ((y+2 in range(8) and board[y+2][x] is not my_colour) or (y+2 not in
           range(8))) and
           ((y-2 in range(8) and board[y-2][x] is not my_colour) or (y+2 not in
           range(8)))):

            remove_goal_pos(goals, x, y)
            
                # Remove co-ordinate from goal list
    def remove_goal_pos(self, goals, x, y):

        if ((x+1, y) in goals and (x+2,y) not in targets and (x+1,y+1) not in
         targets and (x+1,y-1) not in targets):
            goals.remove((x+1, y))
        if ((x-1, y) in goals and (x-2,y) not in targets and (x-1,y+1) not in
         targets and (x-1,y-1) not in targets):
            goals.remove((x-1, y))
        if ((x, y+1) in goals and (x,y+2) not in targets and (x-1,y+1) not in
         targets and (x+1,y+1) not in targets):
            goals.remove((x, y+1))
        if ((x, y-1) in goals and (x,y-2) not in targets and (x-1,y-1) not in
         targets and (x+1,y-1) not in targets):
            goals.remove((x, y-1))
    
      # Function to check the avaliable moves surrounding a piece
        def check_moves(self, x, y):
            moves = 0
            # Check square to right
            if (x+1 in range(8)) and (board[y][x+1] is EMPTY):
                moves += 1
            # Check square to left
            if (x-1 in range(8)) and (board[y][x-1] is EMPTY):
                moves += 1
            # Check square below
            if (y+1 in range(8)) and (board[y+1][x] is EMPTY):
                moves += 1
            # Check square above
            if (y-1 in range(8)) and (board[y-1][x] is EMPTY):
                moves += 1

            # Check if piece can jump to right
            if (x+2 in range(8)) and ((board[y][x+1] is my_colour) or
               (board[y][x+1] is opp_colour)) and (board[y][x+2] is EMPTY):
                moves += 1
            # Check if piece can jump to left
            if (x-2 in range(8)) and ((board[y][x-1] is my_colour) or
               (board[y][x-1] is opp_colour)) and (board[y][x-2] is EMPTY):
                moves += 1
            # Check if piece can jump down
            if (y+2 in range(8)) and ((board[y+1][x] is my_colour) or
               (board[y+1][x] is opp_colour)) and (board[y+2][x] is EMPTY):
                moves += 1
            # Check if piece can jump up
            if (y-2 in range(8)) and ((board[y-1][x] is my_colour) or
               (board[y-1][x] is opp_colour)) and (board[y-2][x] is EMPTY):
                moves += 1

            return moves
    
        def moves(self):
        # Initialise moves variables
        my_moves = []


        # For each square on board:
        #       - check if it's a piece
        #       - if so, count avaliable moves

        for x in range(8):
            for y in range(8):
                if board[y][x] is my_colour:
                    # Check avaliable spaces
                    my_moves += Player.check_moves(self, x, y)

        print(str(my_moves) + "\n"))
        return [my_moves]
    

    def action(self, turns):
        
        # Handling board shrinking
        if turns == 128:
            board = ["X----X",
                     "------",
                     "------",
                     "------",
                     "------",
                     "X----X"]
            dimension = 6
            
         elif turns == 192:
            board = ["X--X",
                     "----",
                     "----",
                     "X--X"]
            dimension = 4
        
        if turns <=24:
            # Placing Phase
            # Will return a single tuple
            
            # pick somewhere to place piece in y_range and not on X
            #   and add to my_pos and board
            
            # Update the board
            s = list(board[y])
            s[x] = EMPTY
            board[y] = "".join(s)
            
        else:
            # Moving Phase
            # Will return a nested tuple
            
        return action
            
       
        
    def update(self, action):
         #update opp_pos and board
    
        
    
    
