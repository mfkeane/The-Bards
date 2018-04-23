fill lists with player and opponent positions
implement update 
board shrinking
fix search

class Player:
    
    from collections import defaultdict
    
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
            moves = []
            # Check square to right
            if (x+1 in range(8)) and (board[y][x+1] is EMPTY):
                moves.append((x,y),(x+1,y));
            # Check square to left
            if (x-1 in range(8)) and (board[y][x-1] is EMPTY):
                moves.append((x,y),(x-1,y));
            # Check square below
            if (y+1 in range(8)) and (board[y+1][x] is EMPTY):
                moves.append((x,y),(x,y+1));
            # Check square above
            if (y-1 in range(8)) and (board[y-1][x] is EMPTY):
                moves.append((x,y),(x,y-1));

            # Check if piece can jump to right
            if (x+2 in range(8)) and ((board[y][x+1] is my_colour) or
               (board[y][x+1] is opp_colour)) and (board[y][x+2] is EMPTY):
                moves.append((x,y),(x+2,y));
            # Check if piece can jump to left
            if (x-2 in range(8)) and ((board[y][x-1] is my_colour) or
               (board[y][x-1] is opp_colour)) and (board[y][x-2] is EMPTY):
                moves.append((x,y),(x-2,y));
            # Check if piece can jump down
            if (y+2 in range(8)) and ((board[y+1][x] is my_colour) or
               (board[y+1][x] is opp_colour)) and (board[y+2][x] is EMPTY):
                moves.append((x,y),(x,y+2));
            # Check if piece can jump up
            if (y-2 in range(8)) and ((board[y-1][x] is my_colour) or
               (board[y-1][x] is opp_colour)) and (board[y-2][x] is EMPTY):
                moves.append((x,y),(x,y-2));

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
                    my_moves = my_moves + Player.check_moves(self, x, y)

        print(str(my_moves) + "\n"))
        return my_moves
    
    # -------------------SEARCH FUNCTIONS------------------

#***
#    The following is based upon and modified from code posted online at:
#    Title: Implementing Depth Limited Path Finding with Stack
#    Author: Screennames "Brian" and "RootTwo"
#    Date: 12 Feb 2016, 21:03
#   Availability: https://stackoverflow.com/questions/35261256/implementing
#                 -depth-limited-path-finding-with-stack
#***

    # Iterative Deepening Search to find paths
    def it_deepening(self, path, attacker, goals, max_depth=16):
        for depth in range(1, max_depth):

            result = Player.depth_limited_search(board, attacker, goals
                                                        ,depth)

            if result is not None:
                return result
            else:
                continue

    # Searching algorithm function: Depth Limited Search
    def depth_limited_search(self, start, goals, depth):
        SENTINEL = object()
        path = []
        visited = [start]

        while visited:

            current = visited.pop()
            # once goal state reached, return the path to it
            if current in goals and current!=start:
                path.append(current)
                return path

            # if the depth is reached without reaching goal, increase depth
            #   & start again
            elif current == SENTINEL:
                depth += 1
                if len(path) > 0:
                    path.pop()

            # if goal isn't reached but depth hasn't been reached, keep
            #   searching through available moves
            elif depth != 0:
                depth -= 1
                path.append(current)
                visited.append(SENTINEL)
                visited.extend(Player.append_moves(board, current[0],
                                                          current[1], path))


#***
#    END OF MODIFIED CODE
#***

    def calc_shortest_dist(self, attacker, goals):
        return len(it_deepening(self, [], attacker, goals))

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
            my_pos = (x,y)
            
        else:
            # Moving Phase
            # Will return a nested tuple
            
            # Run moves, returns array of nested tuples (current pos, end pos)
            moves_list = moves(self)
            
            if len(moves_list) < 1:
                # No avaliable moves
                return None
            
            # Use search function as evaluation on every move and every goal, len of return is distance to goal pos
            eval_dict = defaultdict()
            # For every move, run search len function on every goal, keep track of shortest distance
            for i in len(moves_list):
                val = calc_shortest_dist(self, moves_list[i][1], goals)
                # Then add index of move as key and shortest dist as value in dictionary
                eval_dict[i] = val
            
            for key, value in sorted(eval_dict.iteritems(), key=lambda (k,v): (v,k)): # not really sure how sorted works, loop not necessary but I'm unsure how to do it otherwise
                action = moves_list[key]
                break
            
            #      sort dictionary, use key (index of moves) to find and return that move
            
        return action
            
       
        
    def update(self, action):
         #update opp_pos and board
            
            #have list of white & black pos, update opponent pos, update board and find new goal pos
    
        
    
    
