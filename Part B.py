class Player:
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
            
        else:
            # Moving Phase
            # Will return a nested tuple
            
            # move piece, update my_pos and board
    
        return action
        
        
    def update(self, action):
         #update opp_pos and board
    
    
    
    
