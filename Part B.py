 fill lists with player and opponent positions
implement update 
board shrinking - move corners
fix search

class Player:
    
    from collections import defaultdict
    import random
    
  def update_corners(self, min_index, max_index)
    return [(min_index, min_index),(min_index, max_index),(max_index, min_index),(max_index, max_index)]
    
    def _init_(self, colour):
        
        turn = 0

        min_index = 0
        max_index = 7
        corners = update_corners(min_index, max_index)
        empty_list_spaces = []
        for i in range(max_index+1):
            for j in range(max_index+1):
                if (i,j) not in corners:
                    empty_list_spaces.add((i,j))
    
        my_pos  = []
        opp_pos = []
        
        my_dead  = 0
        opp_dead = 0
        
        if colour == "white":
            y_start = range(0,6)
        elif colour == "black":
            y_start = range(2,8)
              
	save_pos = [] # positions to place pieces to save another immediately
	kill_pos = [] # positions to place pieces to kill an opponent immediately
	
        attackers = []
        flanks = []

            # Check if piece already partially surrounded
    #   and mark goal positions for Player
    def find_goal_pos(self, goals, flanks, x, y):

        # If no Player pieces surround Opponent,
        #   all surrounding tiles are valid goals

        if (x+1 in range(max_index + 1)) and ((x+1,y) in empty_list_spaces):
            goals.append((x+1, y))
        if (x-1 in range(max_index + 1)) and ((x-1,y) in empty_list_spaces):
            goals.append((x-1, y))
        if (y+1 in range(max_index + 1)) and ((x,y+1) in empty_list_spaces):
            goals.append((x, y+1))
        if (y-1 in range(max_index + 1)) and ((x,y-1) in empty_list_spaces):
            goals.append((x, y-1))

        # If piece already surrounded by one Player piece,
        #   or is next to a corner, opposite square is goal

        if ((x+1 in range(max_index + 1)) and (x-1 in range(max_index + 1)) and (((x+1,y) in
           my_pos) or (x+1,y) in corners)):
            goals.append((x-1, y))
            if (x+1,y) in my_pos and (x+1,y) in attackers:
                flanks.append(attackers.pop(attackers.index((x+1, y))))
            if (x,y+1) in goals:
                goals.remove((x,y+1))
            if (x,y-1) in goals:
                goals.remove((x,y-1))

        if ((x-1 in range(max_index + 1)) and (x+1 in range(max_index + 1)) and (((x-1,y) in
           my_pos) or (x-1,y) in corners)):
            goals.append((x+1, y))
            if (x-1,y) in my_pos and (x-1,y) in attackers:
                flanks.append(attackers.pop(attackers.index((x-1, y))))
            if (x,y+1) in goals:
                goals.remove((x,y+1))
            if (x,y-1) in goals:
                goals.remove((x,y-1))

        if ((y+1 in range(max_index + 1)) and (y-1 in range(max_index + 1)) and ((board[x][y+1] is
           my_pos) or (x,y+1) in corners)):
            goals.append((x, y-1))
            if (x,y+1) in my_pos and (x,y+1) in attackers:
                flanks.append(attackers.pop(attackers.index((x, y+1))))
            if (x+1,y) in goals:
                goals.remove((x+1,y))
            if (x-1,y) in goals:
                goals.remove((x-1,y))

        if ((y-1 in range(max_index + 1)) and (y+1 in range(max_index + 1)) and ((board[x][y-1] is
           my_pos) or (x,y-1) in corners)):
            goals.append((x, y+1))
            if (x,y-1) in my_pos and (x,y-1) in attackers:
                flanks.append(attackers.pop(attackers.index((x, y-1))))
            if (x+1,y) in goals:
                goals.remove((x+1,y))
            if (x-1,y) in goals:
                goals.remove((x-1,y))

        # if Opponent on edge of board
        if ((x+1 not in range(max_index + 1)) and ((y+1 in range(max_index + 1) and (x,y+1) in
           empty_list) and ((y-1 in range(max_index + 1)) and (x,y-1) in empty_list_spaces))):
            goals.append((x,y+1))
            goals.append((x,y-1))
            if (x-1,y) in goals:
                goals.remove((x-1,y))

        if ((x-1 not in range(max_index + 1)) and ((y+1 in range(max_index + 1) and (x,y+1) in
           empty_list) and ((y-1 in range(max_index + 1)) and (x,y-1) in empty_list_spaces))):
            goals.append((x,y+1))
            goals.append((x,y-1))
            if (x+1,y) in goals:
                goals.remove((x+1,y))

        if ((y+1 not in range(max_index + 1)) and ((x+1 in range(max_index + 1) and (x+1,y) in
           empty_list) and ((x-1 in range(max_index + 1)) and (x-1,y) in empty_list_spaces))):
            goals.append((x+1,y))
            goals.append((x-1,y))
            if (x,y-1) in goals:
                goals.remove((x,y-1))

        if ((y-1 not in range(max_index + 1)) and ((x+1 in range(max_index + 1) and (x+1,y) in
           empty_list) and ((x-1 in range(max_index + 1)) and (x-1,y) in empty_list_spaces))):
            goals.append((x+1,y))
            goals.append((x-1,y))
            if (x,y+1) in goals:
                goals.remove((x,y+1))


        for goal in goals:
            WatchYourBack.remove_kamikaze(goal)

        return [goals, flanks]
    
    # remove any goals that will result in my_pos's death
    def remove_kamikaze(self, goal):
        x = goal[0]
        y = goal[1]

        if (x in range(1,7) and ((x+1,y) in opp_colour
            and (x-1,y) in opp_colour) and
           ((x+2 in range(max_index + 1) and (x+2,y) in not my_pos) or (x+2 not in
           range(max_index + 1))) and
           ((x-2 in range(max_index + 1) and (x-2,y) in not my_pos) or (x+2 not in
           range(max_index + 1)))):

            remove_goal_pos(goals, x, y)

        if (y in range(1,7) and ((x,y+1) in opp_colour
           and board[y-1][y] is opp_colour) and
           ((y+2 in range(max_index + 1) and (x,y+2) in not my_pos) or (y+2 not in
           range(max_index + 1))) and
           ((y-2 in range(max_index + 1) and (x,y-2) in not my_pos) or (y+2 not in
           range(max_index + 1)))):

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
    
      # Function to check the available moves surrounding a piece
        def check_moves(self, x, y):
            moves = []
            # Check square to right
            if (x+1 in range(max_index + 1)) and ((x+1,y) in empty_list_spaces):
                moves.append((x,y),(x+1,y));
            # Check square to left
            if (x-1 in range(max_index + 1)) and ((x-1,y) in empty_list_spaces):
                moves.append((x,y),(x-1,y));
            # Check square below
            if (y+1 in range(max_index + 1)) and ((x,y+1) in empty_list_spaces):
                moves.append((x,y),(x,y+1));
            # Check square above
            if (y-1 in range(max_index + 1)) and ((x,y-1) in empty_list_spaces):
                moves.append((x,y),(x,y-1));

            # Check if piece can jump to right
            if (x+2 in range(max_index + 1)) and (((x+1,y) in my_pos) or
               ((x+1,y) in opp_colour)) and ((x+2,y) in empty_list):
                moves.append((x,y),(x+2,y));
            # Check if piece can jump to left
            if (x-2 in range(max_index + 1)) and (((x-1,y) in my_pos) or
               ((x-1,y) in opp_colour)) and ((x-2,y) in empty_list):
                moves.append((x,y),(x-2,y));
            # Check if piece can jump down
            if (y+2 in range(max_index + 1)) and (((x,y+1) in my_pos) or
               ((x,y+1) in opp_colour)) and ((x,y+2) in empty_list):
                moves.append((x,y),(x,y+2));
            # Check if piece can jump up
            if (y-2 in range(max_index + 1)) and (((x,y-1) in my_pos) or
               ((x,y-1) in opp_colour)) and ((x,y-2) in empty_list):
                moves.append((x,y),(x,y-2));

            return moves
    
        def moves(self):
        # Initialise moves variables
        my_moves = []


        # For each square on board:
        #       - check if it's a piece
        #       - if so, count available moves

        for x in range(max_index + 1):
            for y in range(max_index + 1):
                if board[y][x] is my_pos:
                    # Check available spaces
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

    def cases(self, case_1, case_2, case_3, case_4):
         for pos in op_pos:
        
#next to each other, next to a wall, +1 from my space, +2 from my space, + 2 from black
    def case_2(self, ):
        #+1 from me only space
    def case_3(self, ):
        #next to a wall

    def check_cases(self, action):
          #case one
          if so:
	   return true:
         #case 2
         #case 3

    def calc_shortest_dist(self, attacker, goals):
        return len(it_deepening(self, [], attacker, goals))

    def action(self, turns):
        turn = turns

        # Handling board shrinking
        
        pieces_in_play = 0
        
        if turns == 128:
            min_index = 1
            max_index = 6
            corners = update_corners(min_index, max_index)
            
        elif turns == 192:
            min_index = 2
	    max_index = 5
     	    corners = update_corners(min_index, max_index)
        
        if turns <=24:
            if turns == 1:
		#Check not placing next to black
                x = random.randint(min_index, max_index)
                y_start_list = list(y_start)
                y = random.randint(y_start_list[0], y_start_list[-1]) 
	    	return (x,y)
	
            """if case_1 != false:
	        return(x,y)
            elif case_2 != false:
	        return(x,y) 
            elif case_3 != false:
                return(x,y)
            elif case_4 != false:
                return(x,y) """

	   # First priority is to save our pieces if needed
           if len(save_pos) != 0:
                for i in range(len(save_pos)):
	          if check_surroundings(save_pos[i]):
                           return save_pos.pop(i)


           # Second priority is to place pieces in positions that will kill an opponent
	   #If player is my_pos, change min and max index 
	   if len(kill_pos) != 0:
                for i in range(len(kill_pos)):
	          if check_surroundings(kill_pos[i]):
                           return kill_pos.pop(i)

	   # If no priorising places, place a piece somewhere so that it is not next to an opponent 
	   # (therefore preventing it from being taken in the next turn)
           for pos in opp_pos:
               result = check_two_away(pos) #check surrounds of position 2 away so not going into a spot where will die
	       if result != None:
	           return result
	
	   for pos in empty_pos:
	        if pos[1] in y_start:
	            if check_surroundings(pos[0], pos[1]) is true:
                        return (x,y) #check surrounds, say if in own area, then safe)
#CHECK EMPTY GUYS PLEASE or choose rand value from empty

#priority: case 1 (next to black), case 2 (next to my zone), case 3 (next to wall or 2 from my zone), case 4 (2 from my piece)
#place opponent, check if matches any of cases. If it matches, check place for my piece isn’t next to a black that is not in soon (not killable). If next to black not in soon, check if can place a white piece somewhere to make case 4 happen, if not, place randomly but not next to black

            
            # MY SECTION, FIX
            for i in range(0, pieces_in_play):
                #if (check if next to opp piece) check surrounds fn (killable fn)?
                    #set goal as square opposite 
            pieces_in_play = pieces_in_play + 1
            # Placing Phase
            # Will return a single tuple
            
            # pick somewhere to place piece in y_range and not on X
            #   and add to my_pos and board
            
            # Update the board
            my_pos.add((x,y))
	    empty_spaces.remove((x,y)) 
	    if (x,y) in kill_pos:
    	        kill_pos.remove((x,y))
            
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
		
		# if move is a dumb move, add 20 to val
		if eval_move(self, i) != true: #need to make this function
			val += 20
                # Then add index of move as key and shortest dist as value in dictionary
                eval_dict[i] = val
            
            for key, value in sorted(eval_dict.iteritems(), key=lambda (k,v): (v,k)): # not really sure how sorted works, loop not necessary but I'm unsure how to do it otherwise
                action = moves_list[key]
                break
            
            #      sort dictionary, use key (index of moves) to find and return that move
            
            return action
            
       
        
    def update(self, action):
        turn += 1

        #update opp_pos and board
        if turn <=24:
 	# Placing Phase
	    op_pos.add(action)
            empty_spaces.remove(action) 
            if action in kill_pos:
                kill_pos.remove(action)

            if check_cases(self, action):
                soon.add(action)

        else:
        # Moving Phase
            op_pos.add(action[1])
            empty_spaces.remove(action[1]) 
            empty_spaces.add(action[0])
            if action[1] in kill_pos:
                kill_pos.remove(action[1])
    


            #have list of my_pos & op_pos pos, update opponent pos, update board and find new goal pos
    
        
    
    
#principle variation search


