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
        elif colour == "black":
            y_start = range(2,8)
            
        
    
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
            
            
            
        # Function to check the avaliable moves surrounding a piece
        def check_moves(board, x, y):
            moves = 0
            # Check square to right
            if (x+1 in range(8)) and (board[x+1][y] is EMPTY):
                moves += 1
            # Check square to left
            if (x-1 in range(8)) and (board[x-1][y] is EMPTY):
                moves += 1
            # Check square below
            if (y+1 in range(8)) and (board[x][y+1] is EMPTY):
                moves += 1
            # Check square above
            if (y-1 in range(8)) and (board[x][y-1] is EMPTY):
                moves += 1

            # Check if piece can jump to right
            if (x+2 in range(8)) and ((board[x+1][y] is WHITE) or
               (board[x+1][y] is BLACK)) and (board[x+2][y] is EMPTY):
                moves += 1
            # Check if piece can jump to left
            if (x-2 in range(8)) and ((board[x-1][y] is WHITE) or
               (board[x-1][y] is BLACK)) and (board[x-2][y] is EMPTY):
                moves += 1
            # Check if piece can jump down
            if (y+2 in range(8)) and ((board[x][y+1] is WHITE) or
               (board[x][y+1] is BLACK)) and (board[x][y+2] is EMPTY):
                moves += 1
            # Check if piece can jump up
            if (y-2 in range(8)) and ((board[x][y-1] is WHITE) or
               (board[x][y-1] is BLACK)) and (board[x][y-2] is EMPTY):
                moves += 1

            return moves
    
        def moves(board):
        # Initialise moves variables
        moves_O = []
        moves_at = []

        # For each square on board:
        #       - check if it's a piece
        #       - if so, count avaliable moves

        for x in range(8):
            for y in range(8):
                if board[x][y] is WHITE:
                    # Check avaliable spaces
                    moves_O += Player.check_moves(board, x, y)

                # Count available moves for BLACK
                elif board[x][y] is BLACK:
                    moves_at += Player.check_moves(board, x, y)

        print(str(moves_O) + "\n" + str(moves_at))
        return [moves_O,  moves_at]
            
            # move piece, update my_pos and board
    
        return action
        
            # Check if piece already partially surrounded
    #   and mark goal positions for WHITE
    def find_goal_pos(goals, flanks, x, y):

        # If no WHITE pieces surround BLACK,
        #   all surrounding tiles are valid goals

        if (x+1 in range(8)) and (board[x+1][y] is EMPTY):
            goals.append((x+1, y))
        if (x-1 in range(8)) and (board[x-1][y] is EMPTY):
            goals.append((x-1, y))
        if (y+1 in range(8)) and (board[x][y+1] is EMPTY):
            goals.append((x, y+1))
        if (y-1 in range(8)) and (board[x][y-1] is EMPTY):
            goals.append((x, y-1))

        # If piece already surrounded by one WHITE piece,
        #   or is next to a CORNER, opposite square is goal

        if ((x+1 in range(8)) and (x-1 in range(8)) and ((board[x+1][y] is
           WHITE) or board[x+1][y] is CORNER)):
            goals.append((x-1, y))
            if board[x+1][y] is WHITE and (x+1,y) in attackers:
                flanks.append(attackers.pop(attackers.index((x+1, y))))
            if (x,y+1) in goals:
                goals.remove((x,y+1))
            if (x,y-1) in goals:
                goals.remove((x,y-1))

        if ((x-1 in range(8)) and (x+1 in range(8)) and ((board[x-1][y] is
           WHITE) or board[x-1][y] is CORNER)):
            goals.append((x+1, y))
            if board[x-1][y] is WHITE and (x-1,y) in attackers:
                flanks.append(attackers.pop(attackers.index((x-1, y))))
            if (x,y+1) in goals:
                goals.remove((x,y+1))
            if (x,y-1) in goals:
                goals.remove((x,y-1))

        if ((y+1 in range(8)) and (y-1 in range(8)) and ((board[x][y+1] is
           WHITE) or board[x][y+1] is CORNER)):
            goals.append((x, y-1))
            if board[x][y+1] is WHITE and (x,y+1) in attackers:
                flanks.append(attackers.pop(attackers.index((x, y+1))))
            if (x+1,y) in goals:
                goals.remove((x+1,y))
            if (x-1,y) in goals:
                goals.remove((x-1,y))

        if ((y-1 in range(8)) and (y+1 in range(8)) and ((board[x][y-1] is
           WHITE) or board[x][y-1] is CORNER)):
            goals.append((x, y+1))
            if board[x][y-1] is WHITE and (x,y-1) in attackers:
                flanks.append(attackers.pop(attackers.index((x, y-1))))
            if (x+1,y) in goals:
                goals.remove((x+1,y))
            if (x-1,y) in goals:
                goals.remove((x-1,y))

        # if BLACK on edge of board
        if ((x+1 not in range(8)) and ((y+1 in range(8) and board[x][y+1] is
           EMPTY) and ((y-1 in range(8)) and board[x][y-1] is EMPTY))):
            goals.append((x,y+1))
            goals.append((x,y-1))
            if (x-1,y) in goals:
                goals.remove((x-1,y))

        if ((x-1 not in range(8)) and ((y+1 in range(8) and board[x][y+1] is
           EMPTY) and ((y-1 in range(8)) and board[x][y-1] is EMPTY))):
            goals.append((x,y+1))
            goals.append((x,y-1))
            if (x+1,y) in goals:
                goals.remove((x+1,y))

        if ((y+1 not in range(8)) and ((x+1 in range(8) and board[x+1][y] is
           EMPTY) and ((x-1 in range(8)) and board[x-1][y] is EMPTY))):
            goals.append((x+1,y))
            goals.append((x-1,y))
            if (x,y-1) in goals:
                goals.remove((x,y-1))

        if ((y-1 not in range(8)) and ((x+1 in range(8) and board[x+1][y] is
           EMPTY) and ((x-1 in range(8)) and board[x-1][y] is EMPTY))):
            goals.append((x+1,y))
            goals.append((x-1,y))
            if (x,y+1) in goals:
                goals.remove((x,y+1))


        for goal in goals:
            WatchYourBack.remove_kamikaze(goal)

        return [goals, flanks]
    
    # remove any goals that will result in white's death
    def remove_kamikaze(goal):
        x = goal[0]
        y = goal[1]

        if (x in range(1,7) and (board[x+1][y] is BLACK
            and board[x-1][y] is BLACK) and
           ((x+2 in range(8) and board[x+2][y] is not WHITE) or (x+2 not in
           range(8))) and
           ((x-2 in range(8) and board[x-2][y] is not WHITE) or (x+2 not in
           range(8)))):

            remove_goal_pos(goals, x, y)

        if (y in range(1,7) and (board[y+1][y] is BLACK
           and board[y-1][y] is BLACK) and
           ((y+2 in range(8) and board[y+2][y] is not WHITE) or (y+2 not in
           range(8))) and
           ((y-2 in range(8) and board[y-2][y] is not WHITE) or (y+2 not in
           range(8)))):

            remove_goal_pos(goals, x, y)
            
                # Remove co-ordinate from goal list
    def remove_goal_pos(goals, x, y):

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
        
    def update(self, action):
         #update opp_pos and board
    
    
    
    
