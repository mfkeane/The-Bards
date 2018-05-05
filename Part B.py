#fill lists with player and opponent positions
#implement update
#board shrinking - move corners
#fix search

from collections import defaultdict
import random
class Player:

    def __init__(self, colour):
        self.turn= -1

        self.min_index = 0
        self.max_index = 7
        self.empty_list = []
        for i in range(self.max_index+1):
            for j in range(self.max_index+1):
                self.empty_list.append((i,j))

        self.my_pos  = []
        self.opp_pos = []

        self.my_dead  = 0
        self.opp_dead = 0

        if colour == "white":
            self.y_start = range(0,6)
        elif colour == "black":
            self.y_start = range(2,8)
        self.y_start_list = list(self.y_start)

        self.save_pos = [] # positions to place pieces to save another immediately
        self.kill_pos = [] # positions to place pieces to kill an opponent immediately

        self.attackers = []
        self.flanks = []
        self.goals = []
        self.corners = Player.update_corners(self)

    # Update Corners by.. well updating corners... Also kills off any pieces outside the new boundaries
    def update_corners(self):
        # Update empty and piece positions (including number of dead)
        for i in range(len(self.empty_list)):
            if (self.empty_list[i][0] < self.min_index or
                self.empty_list[i][0] > self.max_index or
                self.empty_list[i][1] < self.min_index or
                self.empty_list[i][1] > self.max_index):
                self.empty_list.pop(i)
        for i in range(len(self.my_pos)):
            if (self.my_pos[i][0] < self.min_index or
                self.my_pos[i][0] > self.max_index or
                self.my_pos[i][1] < self.min_index or
                self.my_pos[i][1] > self.max_index):
                self.my_pos.pop(i)
                self.my_dead += 1
        for i in range(len(self.opp_pos)):
            if (self.opp_pos[i][0] < self.min_index or
                self.opp_pos[i][0] > self.max_index or
                self.opp_pos[i][1] < self.min_index or
                self.opp_pos[i][1] > self.max_index):
                self.opp_pos.pop(i)
                self.opp_dead += 1

        self.empty_list.remove((self.min_index, self.min_index))
        self.empty_list.remove((self.min_index, self.max_index))
        self.empty_list.remove((self.max_index, self.min_index))
        self.empty_list.remove((self.max_index, self.max_index))
        return [(self.min_index, self.min_index),
                (self.min_index, self.max_index),
                (self.max_index, self.min_index),
                (self.max_index, self.max_index)]

    def update_pos(self, pos, player):
        if player==0:
            if self.turn<24:
                self.my_pos.append(pos)
                self.empty_list.remove(pos)
                if pos in self.kill_pos:
                    self.kill_pos.remove(pos)
                if pos in self.save_pos:
                    self.save_pos.remove(pos)
            else:
                self.my_pos.append(pos[1])
                self.my_pos.remove(pos[0])
                self.empty_list.remove(pos[1])
                self.empty_list.append(pos[0])
                if pos[1] in self.kill_pos:
                    self.kill_pos.remove(pos[1])
                if pos[1] in self.save_pos:
                    self.save_pos.remove(pos[1])

        elif player==1:
            if self.turn<24:
                self.opp_pos.append(pos)
                self.empty_list.remove(pos)
                if pos in self.kill_pos:
                    self.kill_pos.remove(pos)
                if pos in self.save_pos:
                    self.save_pos.remove(pos)
            else:
                self.opp_pos.append(pos[1])
                self.opp_pos.remove(pos[0])
                self.empty_list.remove(pos[1])
                self.empty_list.append(pos[0])
                if pos[1] in self.kill_pos:
                    self.kill_pos.remove(pos[1])
                if pos[1] in self.save_pos:
                    self.save_pos.remove(pos[1])


     # Appends avaliable moves to a list
    def append_moves(self,x,y,path):
        moves = []
        if (x+1 in range(8)) and (x+1,y) in self.empty_list:
            # Only append if not already a square that has been moved to
            if (x+1, y) not in path:
                moves.append((x+1, y))
        if (x-1 in range(8)) and (x-1,y) in self.empty_list:
            if (x-1, y) not in path:
                moves.append((x-1, y))
        if (y+1 in range(8)) and (x,y+1) in self.empty_list:
            if (x, y+1) not in path:
                moves.append((x, y+1))
        if (y-1 in range(8)) and (x,y-1) in self.empty_list:
            if (x, y-1) not in path:
                moves.append((x, y-1))

        # append jumps
        if ((x+2 in range(8)) and (((x+1,y) in self.my_pos) or
           ((x+1,y) in self.opp_pos)) and (x+2,y) in self.empty_list):
            if (x+2, y) not in path:
                moves.append((x+2, y))
        if ((x-2 in range(8)) and (((x-1,y) in self.my_pos) or
           ((x-1,y) in self.opp_pos)) and (x-2,y) in self.empty_list):
            if (x-2, y) not in path:
                moves.append((x-2, y))
        if ((y+2 in range(8)) and (((x,y+1) in self.my_pos) or
           ((x,y+1) in self.opp_pos)) and (x,y+2) in self.empty_list):
            if (x, y+2) not in path:
                moves.append((x, y+2))
        if ((y-2 in range(8)) and (((x,y-1) in self.my_pos) or
           ((x,y-1) in self.opp_pos)) and (x,y-2) in self.empty_list):
            if (x, y-2) not in path:
                moves.append((x, y-2))

        return moves

    # Function checks if a piece has been killed and updates records
    def check_confirmed_kill(self, pos, type):
        if type == 0:
        # My turn, check if opp is dead
            x = pos[0]
            y = pos[1]
            if (((x+1,y) in self.opp_pos) and ((x+2,y) in self.my_pos)):
                self.opp_pos.remove((x+1,y))
                self.opp_dead += 1
                self.empty_list.append((x+1,y))
            elif (((x-1,y) in self.opp_pos) and ((x-2,y) in self.my_pos)):
                self.opp_pos.remove((x-1,y))
                self.opp_dead += 1
                self.empty_list.append((x-1,y))
            elif (((x,y+1) in self.opp_pos) and ((x,y+2) in self.my_pos)):
                self.opp_pos.remove((x,y+1))
                self.opp_dead += 1
                self.empty_list.append((x,y+1))
            elif (((x,y-1) in self.opp_pos) and ((x,y-2) in self.my_pos)):
                self.opp_pos.remove((x,y-1))
                self.opp_dead += 1
                self.empty_list.append((x,y-1))

        elif type == 1:
        # Opp turn, check if my piece is dead
            x = pos[0]
            y = pos[1]
            if (((x+1,y) in self.my_pos) and ((x+2,y) in self.opp_pos)):
                self.my_pos.remove((x+1,y))
                self.my_dead += 1
                self.empty_list.append((x+1,y))
            elif (((x-1,y) in self.my_pos) and ((x-2,y) in self.opp_pos)):
                self.my_pos.remove((x-1,y))
                self.my_dead += 1
                self.empty_list.append((x-1,y))
            elif (((x,y+1) in self.my_pos) and ((x,y+2) in self.opp_pos)):
                self.my_pos.remove((x,y+1))
                self.my_dead += 1
                self.empty_list.append((x,y+1))
            elif (((x,y-1) in self.my_pos) and ((x,y-2) in self.opp_pos)):
                self.my_pos.remove((x,y-1))
                self.my_dead += 1
                self.empty_list.append((x,y-1))

    def check_kill_save_pos(self, pos):
        x = pos[0]
        y = pos[1]

        if ((x+1,y) in self.my_pos):
            if ((x-1,y) in self.empty_list):
                self.kill_pos.append((x-1,y))
            elif ((x+2,y) in self.empty_list):
                self.save_pos.append((x+2,y))
        elif ((x-1,y) in self.my_pos):
            if ((x+1,y) in self.empty_list):
                self.kill_pos.append((x+1,y))
            elif ((x-2,y) in self.empty_list):
                self.save_pos.append((x-2,y))
        elif ((x,y+1) in self.my_pos):
            if ((x,y-1) in self.empty_list):
                self.kill_pos.append((x,y-1))
            elif ((x,y+2) in self.empty_list):
                self.save_pos.append((x,y+2))
        elif ((x,y-1) in self.my_pos):
            if ((x,y+1) in self.empty_list):
                self.kill_pos.append((x,y+1))
            elif ((x,y-2) in self.empty_list):
                self.save_pos.append((x,y-2))

    def eval_move(self, pos, curr_pos):
        x = pos[0]
        y = pos[1]

        if self.turn >= 24:
            self.my_pos.remove(curr_pos)

        if (((x+1,y) in self.opp_pos) or ((x-1,y) in self.opp_pos) or 
            ((x,y+1) in self.opp_pos) or ((x,y-1) in self.opp_pos)):
            # Check if we'll die since there’s an opp next to us
            if ((((x+1,y) in self.opp_pos or (x+1,y) in self.corners) and
               ((x-1,y) in self.opp_pos or (x-1,y) in self.corners) and
               (((x+2,y) in self.my_pos or (x+2,y) in self.corners) or
               ((x-2,y) in self.my_pos or (x-2,y) in self.corners))) or
               (((x,y+1) in self.opp_pos or (x,y+1) in self.corners) and
               ((x,y-1) in self.opp_pos or (x,y-1) in self.corners) and
               (((x,y+2) in self.my_pos or (x,y+2) in self.corners) or
               ((x,y-2) in self.my_pos or (x,y-2) in self.corners)))):
            # In a deadly spot, but we won't die as we're attacking
                if (self.turn < 24):
                    # Can cause a loop to form that is not productive in placing phase
                    return 5
                self.my_pos.append(curr_pos)   
                return 0
            elif (((x+1,y) in self.opp_pos or (x+1,y) in self.corners) and
                 ((x-1,y) in self.opp_pos or (x-1,y) in self.corners) or
                 (((x,y+1) in self.opp_pos or (x,y+1) in self.corners) and
                 ((x,y-1) in self.opp_pos or (x,y-1) in self.corners))):
            # In a deadly spot and will die, even if we kill a piece
                if self.turn>=24:
                    self.my_pos.append(curr_pos)
                return 20
            if (self.turn<24):
                # placing phase, don’t go next to an opp unless setting up to kill it
                if (((x+1,y) in self.opp_pos and (x-1,y) in self.my_pos) or
                   ((x-1,y) in self.opp_pos and (x+1,y) in self.my_pos) or
                   ((x,y+1)  in self.opp_pos and (x,y-1) in self.my_pos) or
                   ((x,y-1) in self.opp_pos and (x,y+1) in self.my_pos)):
                   # safe, since pos opp needs to kill piece is blocked by my piece
                    return 0
               # in own safe zone
                elif ((self.y_start == range(0,6) and (y==0 or y==1)) or
                   (self.y_start == range(2,8) and (y==7 or y==6))):
                    return 0
                elif (((x+1,y) in self.opp_pos and (x+2,y) in self.my_pos) or\
                     ((x-1,y) in self.opp_pos and (x-2,y) in self.my_pos) or\
                    ((x,y+1) in self.opp_pos and (x,y+2) in self.my_pos) or
                    ((x,y-1) in self.opp_pos and (x,y-2) in self.my_pos)):
                    # Will kill opp and not in a deadly position
                    return 0
                else:
                    #may die next as next to an opponent
                    return 10
            if ((x+1,y) in self.corners or (x-1,y) in self.corners or
                (x,y+1) in self.corners or (x,y-1) in self.corners):
                if self.turn>=24:
                    self.my_pos.append(curr_pos)
                return 15
        # not next to opp
        if self.turn>=24:
            self.my_pos.append(curr_pos)
        return 0

    #change y vals of out of bounds for moving

    def remove_kamikaze(self, goal, goals):
        x = goal[0]
        y = goal[1]

        if (x in range(self.min_index+1,self.max_index-1)
           and ((x+1,y) in self.opp_pos and (x-1,y) in self.opp_pos) and
           ((x+2 in range(self.max_index + 1) and (x+2,y) not in self.my_pos)
           or (x+2 not in range(self.max_index + 1))) and
           ((x-2 in range(self.max_index + 1) and
           (x-2,y) not in self.my_pos) or
           (x+2 not in range(self.max_index + 1)))):

            Player.remove_goal_pos(self, goals, x, y)

        if (y in range(self.min_index+1,self.max_index-1)
           and ((x,y+1) in self.opp_pos and (x,y-1) is self.opp_pos) and
           ((y+2 in range(self.max_index + 1) and
           (x,y+2) not in self.my_pos) or
           (y+2 not in range(self.max_index + 1))) and
           ((y-2 in range(self.max_index + 1) and (x,y-2) not in self.my_pos)
           or (y+2 not in range(self.max_index + 1)))):

            Player.remove_goal_pos(self, goals, x, y)

    # Check if piece already partially surrounded
    #   and mark goal positions for Player
    def find_goal_pos(self, x, y):

        goals=[]
        flanks=[]

        # If no Player pieces surround Opponent,
        #   all surrounding tiles are valid self.goals

        if ((x+1 in range(self.max_index + 1)) and
           ((x+1,y) in self.empty_list)):
            goals.append((x+1, y))
        if ((x-1 in range(self.max_index + 1)) and
           ((x-1,y) in self.empty_list)):
            goals.append((x-1, y))
        if ((y+1 in range(self.max_index + 1)) and
           ((x,y+1) in self.empty_list)):
            goals.append((x, y+1))
        if ((y-1 in range(self.max_index + 1)) and
           ((x,y-1) in self.empty_list)):
            goals.append((x, y-1))

        # If piece already surrounded by one Player piece,
        #   or is next to a corner, opposite square is goal

        if ((x+1 in range(self.max_index + 1)) and
           (x-1 in range(self.max_index + 1)) and
           (((x+1,y) in self.my_pos) or (x+1,y) in self.corners)):
            goals.append((x-1, y))
            if (x+1,y) in self.my_pos and (x+1,y) in self.attackers:
                flanks.append(self.attackers.pop(self.attackers.index((x+1, y))))
            if (x,y+1) in goals:
                goals.remove((x,y+1))
            if (x,y-1) in goals:
                goals.remove((x,y-1))

        if ((x-1 in range(self.max_index + 1)) and
           (x+1 in range(self.max_index + 1)) and (((x-1,y) in self.my_pos)
           or (x-1,y) in self.corners)):
            goals.append((x+1, y))
            if (x-1,y) in self.my_pos and (x-1,y) in self.attackers:
                flanks.append(self.attackers.pop(self.attackers.index((x-1, y))))
            if (x,y+1) in goals:
                goals.remove((x,y+1))
            if (x,y-1) in goals:
                goals.remove((x,y-1))

        if ((y+1 in range(self.max_index + 1)) and
           (y-1 in range(self.max_index + 1)) and (((x,y+1) is self.my_pos)
           or (x,y+1) in self.corners)):
            goals.append((x, y-1))
            if (x,y+1) in self.my_pos and (x,y+1) in self.attackers:
                flanks.append(self.attackers.pop(self.attackers.index((x, y+1))))
            if (x+1,y) in goals:
                goals.remove((x+1,y))
            if (x-1,y) in goals:
                goals.remove((x-1,y))

        if ((y-1 in range(self.max_index + 1)) and
           (y+1 in range(self.max_index + 1)) and (((x,y-1) is self.my_pos)
           or (x,y-1) in self.corners)):
            goals.append((x, y+1))
            if (x,y-1) in self.my_pos and (x,y-1) in self.attackers:
                flanks.append(self.attackers.pop(self.attackers.index((x, y-1))))
            if (x+1,y) in goals:
                goals.remove((x+1,y))
            if (x-1,y) in goals:
                goals.remove((x-1,y))

        # if Opponent on edge of board
        if ((x+1 not in range(self.max_index + 1)) and
           ((y+1 in range(self.max_index + 1) and (x,y+1) in self.empty_list)
           and ((y-1 in range(self.max_index + 1))
           and (x,y-1) in self.empty_list))):
            goals.append((x,y+1))
            goals.append((x,y-1))
            if (x-1,y) in goals:
                goals.remove((x-1,y))

        if ((x-1 not in range(self.max_index + 1)) and
           ((y+1 in range(self.max_index + 1) and (x,y+1) in self.empty_list)
           and ((y-1 in range(self.max_index + 1))
           and (x,y-1) in self.empty_list))):
            goals.append((x,y+1))
            goals.append((x,y-1))
            if (x+1,y) in goals:
                goals.remove((x+1,y))

        if ((y+1 not in range(self.max_index + 1)) and
           ((x+1 in range(self.max_index + 1) and (x+1,y) in self.empty_list)
           and ((x-1 in range(self.max_index + 1))
           and (x-1,y) in self.empty_list))):
            goals.append((x+1,y))
            goals.append((x-1,y))
            if (x,y-1) in goals:
                goals.remove((x,y-1))

        if ((y-1 not in range(self.max_index + 1)) and
           ((x+1 in range(self.max_index + 1) and (x+1,y) in self.empty_list)
           and ((x-1 in range(self.max_index + 1))
           and (x-1,y) in self.empty_list))):
            goals.append((x+1,y))
            goals.append((x-1,y))
            if (x,y+1) in goals:
                goals.remove((x,y+1))


        for goal in goals:
            Player.remove_kamikaze(self, goal, goals)

        return [goals, flanks]

    # remove any self.goals that will result in self.my_pos's death


    # Remove co-ordinate from goal list
    def remove_goal_pos(self, goals, x, y):

        if ((x+1, y) in goals and (x+2,y) not in targets and
           (x+1,y+1) not in targets and (x+1,y-1) not in targets):
            goals.remove((x+1, y))
        if ((x-1, y) in goals and (x-2,y) not in targets and
           (x-1,y+1) not in targets and (x-1,y-1) not in targets):
            goals.remove((x-1, y))
        if ((x, y+1) in goals and (x,y+2) not in targets and
           (x-1,y+1) not in targets and (x+1,y+1) not in targets):
            goals.remove((x, y+1))
        if ((x, y-1) in goals and (x,y-2) not in targets and
           (x-1,y-1) not in targets and (x+1,y-1) not in targets):
            goals.remove((x, y-1))

      # Function to check the available moves surrounding a piece
    def check_moves(self, x, y):
        moves = []
        # Check square to right
        if ((x+1 in range(self.max_index + 1)) and
           ((x+1,y) in self.empty_list)):
            moves.append(((x,y),(x+1,y)));
        # Check square to left
        if ((x-1 in range(self.max_index + 1)) and
           ((x-1,y) in self.empty_list)):
            moves.append(((x,y),(x-1,y)));
        # Check square below
        if ((y+1 in range(self.max_index + 1)) and
           ((x,y+1) in self.empty_list)):
            moves.append(((x,y),(x,y+1)));
        # Check square above
        if ((y-1 in range(self.max_index + 1)) and
           ((x,y-1) in self.empty_list)):
            moves.append(((x,y),(x,y-1)));

        # Check if piece can jump to right
        #FIX CHECK 2 AWAY TO BE USED IN HERE?
        if ((x+2 in range(self.max_index + 1)) and (((x+1,y) in self.my_pos) or
           ((x+1,y) in self.opp_pos)) and ((x+2,y) in self.empty_list)):
            moves.append(((x,y),(x+2,y)));
        # Check if piece can jump to left
        if ((x-2 in range(self.max_index + 1)) and (((x-1,y) in self.my_pos) or
           ((x-1,y) in self.opp_pos)) and ((x-2,y) in self.empty_list)):
            moves.append(((x,y),(x-2,y)));
        # Check if piece can jump down
        if ((y+2 in range(self.max_index + 1)) and (((x,y+1) in self.my_pos) or
           ((x,y+1) in self.opp_pos)) and ((x,y+2) in self.empty_list)):
            moves.append(((x,y),(x,y+2)));
        # Check if piece can jump up
        if ((y-2 in range(self.max_index + 1)) and (((x,y-1) in self.my_pos) or
           ((x,y-1) in self.opp_pos)) and ((x,y-2) in self.empty_list)):
            moves.append(((x,y),(x,y-2)));

        return moves

    def moves(self):
        # Initialise moves variables
        my_moves = []


        # For each square on board:
        #       - check if it's a piece
        #       - if so, count available moves

        for x in range(self.max_index + 1):
            for y in range(self.max_index + 1):
                if (x,y) in self.my_pos:
                    # Check available spaces
                    my_moves = my_moves + Player.check_moves(self, x, y)

        #print(str(my_moves) + "\n"))
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

            result = Player.depth_limited_search(self, attacker, self.goals
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
            if current in self.goals and current!=start:
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
                visited.extend(Player.append_moves(self, current[0],
                                                          current[1], path))


#***
#    END OF MODIFIED CODE
#***

    def calc_shortest_dist(self, attacker, goals):
        return len(Player.it_deepening(self, [], attacker, self.goals))


    #CHANGE TO USE FOR JUMPS?
    def check_two_away(self, pos):
        x = pos[0] #CHECK THIS?
        y = pos[1]

        if ((x+2 in range(self.max_index + 1)) and
           ((x+2,y) in self.empty_list) and
           Player.eval_move(self, (x+2,y), pos)==0):
            return(x+2,y)
        if ((x-2 in range(self.max_index + 1)) and
           ((x-2,y) in self.empty_list) and
           Player.eval_move(self, (x-2,y), pos)==0):
            return(x-2,y)
        if ((y+2 in range(self.max_index + 1)) and
           ((x,y+2) in self.empty_list)and
           Player.eval_move(self, (x,y+2), pos)==0):
            return(x,y+2)
        if ((y-2 in range(self.max_index + 1)) and
           ((x,y-2) in self.empty_list) and
           Player.eval_move(self, (x,y-2), pos)==0):
            return(x,y-2)
        return None


    def action(self, turns):
        self.turn+= 1

        # Handling board shrinking
        if self.turn== 151:
            self.min_index = 1
            self.max_index = 6
            self.corners = Player.update_corners(self)

        elif self.turn== 215:
            self.min_index = 2
            self.max_index = 5
            self.corners = Player.update_corners(self)

        if self.turn<24:
            possible_moves = []
            if self.turn== 0:
                while(True):
                    x = random.randint(self.min_index, self.max_index)
                    y = random.randint(self.y_start_list[0], self.y_start_list[-1])
                    if (x, y) not in self.corners:
                        self.my_pos.append((x,y))
                        self.empty_list.remove((x,y))
                        return (x,y)


       # First priority is to save our pieces if needed
            if len(self.save_pos) != 0:
                for i in range(len(self.save_pos)):
                    if self.save_pos[i][1]  in self.y_start_list:
                        if self.save_pos[i] in self.empty_list:
                            if Player.eval_move(self, self.save_pos[i], (-1,-1))==0:
                                pos = self.save_pos[i]
                                Player.update_pos(self, pos, 0)
                                return pos



           # Second priority is to place pieces in positions that will kill an opponent
       #If player is self.my_pos, change min and max index
            if len(self.kill_pos) != 0:
                for i in range(len(self.kill_pos)):
                    if self.kill_pos[i][1] in self.y_start_list:
                        if self.kill_pos[i] in self.empty_list:
                            if Player.eval_move(self,self.kill_pos[i], (-1,-1))==0:
                                pos = self.kill_pos[i]
                                Player.check_confirmed_kill(self, pos, 0)
                                Player.update_pos(self, pos, 0)
                                return pos

       # If no priorising places, place a piece somewhere so that it is not next to an opponent
       # (therefore preventing it from being taken in the next turn)
            for pos in self.opp_pos:
                result = Player.check_two_away(self,pos) #check surrounds of position 2 away so not going into a spot where will die
                if result != None:
                    if result[1] in self.y_start_list:
                        if result in self.empty_list:
                            Player.update_pos(self, result, 0)
                            return result
            while(True):
                pos = self.empty_list[random.randint(0, len(self.empty_list)-1)]
                if pos[1] in self.y_start_list:
                        if Player.eval_move(self,pos,(-1,-1)) == 0:
                            Player.update_pos(self, pos, 0)
                            return pos

#priority: case 1 (next to black), case 2 (next to my zone), case 3 (next to wall or 2 from my zone), case 4 (2 from my piece)
#place opponent, check if matches any of cases. If it matches, check place for my piece isn’t next to a black that is not in soon (not killable). If next to black not in soon, check if can place a white piece somewhere to make case 4 happen, if not, place randomly but not next to black

        else:
            # Moving Phase
            # Will return a nested tuple

            if self.turn==24:
                # First turn of moving phase before goals updated
                self.attackers = self.my_pos
                self.goals = []
                self.flanks = []

                for pos in self.opp_pos:
                    returns = Player.find_goal_pos(self, pos[0], pos[1])

                    for goal in returns[0]:
                        if goal not in self.goals:
                            self.goals.append(goal)
                    for flank in returns[1]:
                        if flank not in self.flanks:
                            self.flanks.append(flank)
                

            # Run moves, returns array of nested tuples (current pos, end pos)
            moves_list = Player.moves(self)

            if len(moves_list) < 1:
                # No avaliable moves
                return None

            # Use search function as evaluation on every move and every goal, len of return is distance to goal pos
            eval_dict = defaultdict()
            # For every move, run search len function on every goal, keep track of shortest distance


            for i in range(len(moves_list)):
                result = (Player.depth_limited_search(self,
                                                moves_list[i][1], self.goals, 10))
                if result == None:
                    continue
                val = len(result)

                if moves_list[i] not in self.kill_pos:
                    val += 5
            # if move is a dumb move, add more to val
            val += Player.eval_move(self, moves_list[i][1], moves_list[i][0])
                # Then add index of move as key and shortest dist as value in dictionary
            eval_dict[i] = val
            l = list(eval_dict.items()) 
            for key, value in sorted(l,
                key=lambda item: (item[1], item[0])): # PRINT LIST TO SEE IF IT WORKS
                action = moves_list[key]
                break

            #      sort dictionary, use key (index of moves) to find and return that move
            Player.check_confirmed_kill(self, action[1], 0)
            #print(self.opp_pos)
            print(self.my_pos)
            Player.update_pos(self, action, 0)
            return action



    def update(self, action):
        self.turn+= 1

        #update self.opp_pos and board
        if self.turn<24:
        # Placing Phase
            Player.update_pos(self, action, 1)

            #if check_cases(self, action): #what are we doing with this?
            #    soon.add(action)

            Player.check_confirmed_kill(self, action, 1)
            Player.check_kill_save_pos(self, action)

        else:
        # Moving Phase
            if self.turn==24:
                self.attackers = self.my_pos

            Player.update_pos(self, action, 1)

            Player.check_confirmed_kill(self, action[1], 1)
            Player.check_kill_save_pos(self, action[1])

            self.goals = []
            self.flanks = []

            for pos in self.opp_pos:
                returns = Player.find_goal_pos(self, pos[0], pos[1])

                for goal in returns[0]:
                    if goal not in self.goals:
                        self.goals.append(goal)
                for flank in returns[1]:
                    if flank not in self.flanks:
                        self.flanks.append(flank)




            #have list of self.my_pos & op_pos pos, update opponent pos, update board and find new goal pos




#principle variation search
