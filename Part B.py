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
        moves_O = 0
        moves_at = 0

        # For each square on board:
        #       - check if it's a piece
        #       - if so, count avaliable moves

        for x in range(8):
            for y in range(8):
                if board[x][y] is WHITE:
                    # Check avaliable spaces
                    moves_O += WatchYourBack.check_moves(board, x, y)

                # Count available moves for BLACK
                elif board[x][y] is BLACK:
                    moves_at += WatchYourBack.check_moves(board, x, y)

        print(str(moves_O) + "\n" + str(moves_at))
        return [moves_O,  moves_at]
            
            # move piece, update my_pos and board
    
        return action
        
        
    def update(self, action):
         #update opp_pos and board
    
    
    
    
