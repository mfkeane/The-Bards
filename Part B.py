"""
 __________________________________________________________________________
|__________________________________________________________________________|
|                            Watch Your Back                               |
|                       ~ Player Implementation ~                          |
|__________________________________________________________________________|
|__________________________________________________________________________|
|                                                                          |
|           Title : the-bards.py                                           |
|         Authors : Michelle Keane & Courtney Downes                       |
|              ID :      832948           ######                           |
|            Team : The Bards                                              |
|                                                                          |
|        Made for : COMP30024 Artificial Intelligence                      |
|                   Project Part B                                         |
|                   University of Melbourne                                |
|                   2018                                                   |
|                                                                          |
|         Version : 1.0                                                    |
|            Date : 08/05/2018                                             |
|__________________________________________________________________________|
|__________________________________________________________________________|
"""

from collections import defaultdict
import random

"""
___________________________________________________________________________
                             ~ Player Class ~
___________________________________________________________________________
"""


class Player:

    # __________________________________________________________________________
    #                                 _init_
    # __________________________________________________________________________

    def __init__(self, colour):
        self.turn = -1

        # Set up board parameters and empty_list
        self.min_index = 0
        self.max_index = 7
        self.empty_list = []
        for i in range(self.max_index+1):
            for j in range(self.max_index+1):
                self.empty_list.append((i, j))

        # Initialise tracking for players:
        #   -> positions and number of dead
        self.my_pos = []
        self.opp_pos = []

        self.my_dead = 0
        self.opp_dead = 0

        self.my_colour = colour

        # Set up starting ranges for Placing Phase
        if colour == "white":
            self.y_start = range(0, 6)
        elif colour == "black":
            self.y_start = range(2, 8)
        self.y_start_list = list(self.y_start)

        # positions to place pieces to save another immediately
        self.save_pos = []
        # positions to place pieces to kill an opponent immediately
        self.kill_pos = []

        # Strategic tracking for Moving Phase
        self.flanks = []
        self.goals = []
        self.next_boarders = []

        # Set corner positions
        self.corners = Player.update_corners(self)

    # __________________________________________________________________________
    # __________________________________________________________________________
    #                           HELPER FUNCTIONS
    # __________________________________________________________________________

    # Update Corners, kills off any pieces outside the new boundaries
    def update_corners(self):
        # Update empty and piece positions (including number of dead)

        # Remove things that are in the corner positions
        if (self.min_index, self.min_index) in self.empty_list:
            self.empty_list.remove((self.min_index, self.min_index))
        if (self.min_index, self.max_index) in self.empty_list:
            self.empty_list.remove((self.min_index, self.max_index))
        if (self.max_index, self.min_index) in self.empty_list:
            self.empty_list.remove((self.max_index, self.min_index))
        if (self.max_index, self.max_index) in self.empty_list:
            self.empty_list.remove((self.max_index, self.max_index))

        if (self.min_index, self.min_index) in self.my_pos:
            self.my_pos.remove((self.min_index, self.min_index))
        if (self.min_index, self.max_index) in self.my_pos:
            self.my_pos.remove((self.min_index, self.max_index))
        if (self.max_index, self.min_index) in self.my_pos:
            self.my_pos.remove((self.max_index, self.min_index))
        if (self.max_index, self.max_index) in self.my_pos:
            self.my_pos.remove((self.max_index, self.max_index))

        if (self.min_index, self.min_index) in self.opp_pos:
            self.opp_pos.remove((self.min_index, self.min_index))
        if (self.min_index, self.max_index) in self.opp_pos:
            self.opp_pos.remove((self.min_index, self.max_index))
        if (self.max_index, self.min_index) in self.opp_pos:
            self.opp_pos.remove((self.max_index, self.min_index))
        if (self.max_index, self.max_index) in self.opp_pos:
            self.opp_pos.remove((self.max_index, self.max_index))

        # Update empty_list
        i = 0
        while i < len(self.empty_list):
            if ((self.empty_list[i][0] < self.min_index) or
                    (self.empty_list[i][0] > self.max_index) or
                    (self.empty_list[i][1] < self.min_index) or
                    (self.empty_list[i][1] > self.max_index)):
                self.empty_list.pop(i)
            else:
                i += 1

        # Update my_pos
        i = 0
        while i < len(self.my_pos):
            if ((self.my_pos[i][0] < self.min_index) or
                    (self.my_pos[i][0] > self.max_index) or
                    (self.my_pos[i][1] < self.min_index) or
                    (self.my_pos[i][1] > self.max_index)):
                self.my_pos.pop(i)
                self.my_dead += 1
            else:
                i += 1

        # Update opp_pos
        i = 0
        while i < len(self.opp_pos):
            if ((self.opp_pos[i][0] < self.min_index) or
                    (self.opp_pos[i][0] > self.max_index) or
                    (self.opp_pos[i][1] < self.min_index) or
                    (self.opp_pos[i][1] > self.max_index)):
                self.opp_pos.pop(i)
                self.opp_dead += 1
            else:
                i += 1

        self.next_boarders = []
        for i in range(self.min_index+2, self.max_index-1):
            self.next_boarders.append((i, self.min_index+1))
            self.next_boarders.append((i, self.max_index-1))
            self.next_boarders.append((self.min_index+1, i))
            self.next_boarders.append((self.max_index-1, i))
            self.next_boarders.append((i, self.min_index+2))
            self.next_boarders.append((i, self.max_index-2))
            self.next_boarders.append((self.min_index+2, i))
            self.next_boarders.append((self.max_index-2, i))

        self.corners = [(self.min_index, self.min_index),
                        (self.min_index, self.max_index),
                        (self.max_index, self.max_index),
                        (self.max_index, self.min_index)]

        # Check if the corners killed anyone by changing position
        for pos in self.corners:
            Player.check_confirmed_kill(self, pos, (-1, -1), 
                                        [self.empty_list, self.my_pos,
                                         self.opp_pos],
                                        [self.my_dead, self.opp_dead],
                                        0)
            Player.check_confirmed_kill(self, pos, (-1, -1), 
                                        [self.empty_list, self.my_pos,
                                         self.opp_pos],
                                        [self.my_dead, self.opp_dead],
                                        1)

        return [(self.min_index, self.min_index),
                (self.min_index, self.max_index),
                (self.max_index, self.max_index),
                (self.max_index, self.min_index)]

    # Function updates my_pos, opp_pos, and empty_list based on the move
    #   just taken
    def update_pos(self, pos, board, player, type=0):
        empty_list = board[0]
        if player == 0:
            # My Turn
            my_pos = board[1]
            opp_pos = board[2]
        elif player == 1:
            # Opponents Turn
            my_pos = board[2]
            opp_pos = board[1]

        if self.turn < 24:
            # Placing Phase
            my_pos.append(pos)
            empty_list.remove(pos)
            if pos in self.kill_pos:
                self.kill_pos.remove(pos)
            if pos in self.save_pos:
                self.save_pos.remove(pos)
        else:
            # Moving Phase (need to sort out old position as well)
            my_pos.append(pos[1])
            my_pos.remove(pos[0])
            empty_list.remove(pos[1])
            empty_list.append(pos[0])
            if type == 0:
                if pos[1] in self.kill_pos:
                    self.kill_pos.remove(pos[1])
                if pos[1] in self.save_pos:
                    self.save_pos.remove(pos[1])

    # Appends avaliable moves to a list
    def append_moves(self, x, y, path):
        moves = []
        if (x+1 in range(8)) and (x+1, y) in self.empty_list:
            # Only append if not already a square that has been moved to
            if (x+1, y) not in path:
                moves.append((x+1, y))
        if (x-1 in range(8)) and (x-1, y) in self.empty_list:
            if (x-1, y) not in path:
                moves.append((x-1, y))
        if (y+1 in range(8)) and (x, y+1) in self.empty_list:
            if (x, y+1) not in path:
                moves.append((x, y+1))
        if (y-1 in range(8)) and (x, y-1) in self.empty_list:
            if (x, y-1) not in path:
                moves.append((x, y-1))

        # Append jumps
        if ((x+2 in range(8)) and (((x+1, y) in self.my_pos) or
           ((x+1, y) in self.opp_pos)) and (x+2, y) in self.empty_list):
            if (x+2, y) not in path:
                moves.append((x+2, y))
        if ((x-2 in range(8)) and (((x-1, y) in self.my_pos) or
           ((x-1, y) in self.opp_pos)) and (x-2, y) in self.empty_list):
            if (x-2, y) not in path:
                moves.append((x-2, y))
        if ((y+2 in range(8)) and (((x, y+1) in self.my_pos) or
           ((x, y+1) in self.opp_pos)) and (x, y+2) in self.empty_list):
            if (x, y+2) not in path:
                moves.append((x, y+2))
        if ((y-2 in range(8)) and (((x, y-1) in self.my_pos) or
           ((x, y-1) in self.opp_pos)) and (x, y-2) in self.empty_list):
            if (x, y-2) not in path:
                moves.append((x, y-2))

        return moves

    # Function checks if a piece has been killed and updates records
    def check_confirmed_kill(self, pos, curr_pos, board, dead, type):
        empty_list = board[0]
        if type == 0:
            # My turn, check if opp is dead
            my_pos = board[1]
            opp_pos = board[2]
            my_dead = dead[0]
            opp_dead = dead[1]
        elif type == 1:
            # Opp turn, check if my piece is dead
            my_pos = board[2]
            opp_pos = board[1]
            my_dead = dead[1]
            opp_dead = dead[0]

        x = pos[0]
        y = pos[1]

        if (((x+1, y) in opp_pos) and (((x+2, y) in my_pos) or
           ((x+2, y) in self.corners)) and ((x+2, y) != curr_pos)):
            opp_pos.remove((x+1, y))
            opp_dead += 1
            empty_list.append((x+1, y))
        if (((x-1, y) in opp_pos) and (((x-2, y) in my_pos) or
           ((x-2, y) in self.corners)) and ((x-2, y) != curr_pos)):
            opp_pos.remove((x-1, y))
            opp_dead += 1
            empty_list.append((x-1, y))
        if (((x, y+1) in opp_pos) and (((x, y+2) in my_pos) or
           ((x, y+2) in self.corners)) and ((x, y+2) != curr_pos)):
            opp_pos.remove((x, y+1))
            opp_dead += 1
            empty_list.append((x, y+1))
        if (((x, y-1) in opp_pos) and (((x, y-2) in my_pos) or
           ((x, y-2) in self.corners)) and ((x, y-2) != curr_pos)):
            opp_pos.remove((x, y-1))
            opp_dead += 1
            empty_list.append((x, y-1))

        # Check if My piece will die while trying to attack
        if ((((x+1, y) in opp_pos or (x+1, y) in self.corners) and
            ((x-1, y) in opp_pos or (x-1, y) in self.corners) and
            (((x+2, y) in my_pos or (x+2, y) in self.corners) or
            ((x-2, y) in my_pos or (x-2, y) in self.corners))) or
            (((x, y+1) in opp_pos or (x, y+1) in self.corners) and
            ((x, y-1) in opp_pos or (x, y-1) in self.corners) and
            (((x, y+2) in my_pos or (x, y+2) in self.corners) or
             ((x, y-2) in my_pos or (x, y-2) in self.corners)))):
            # In a deadly spot, but we won't die as we're attacking
            safe = True
        elif (((x+1, y) in opp_pos or (x+1, y) in self.corners) and
              ((x-1, y) in opp_pos or (x-1, y) in self.corners) or
              (((x, y+1) in opp_pos or (x, y+1) in self.corners) and
              ((x, y-1) in opp_pos or (x, y-1) in self.corners))):
            # In a deadly spot and will die, even if we kill a piece
            my_pos.remove((x, y))
            my_dead += 1
            empty_list.append((x, y))

    # Check and add positions to kill_pos and save_pos
    #   kill_pos: positions that will kill an opponent immediately
    #   save_pos: positions that will save a friendly from imminent death
    def check_kill_save_pos(self, pos, type=0):
        x = pos[0]
        y = pos[1]

        if type == 0:
            if ((x+1, y) in self.my_pos) or ((x+1, y) in self.corners):
                if ((x-1, y) in self.empty_list):
                    if ((x-1, y) not in self.kill_pos):
                        self.kill_pos.append((x-1, y))
                elif ((x+2, y) in self.empty_list):
                    if ((x+2, y) not in self.save_pos):
                        self.save_pos.append((x+2, y))

            if ((x-1, y) in self.my_pos) or ((x-1, y) in self.corners):
                if ((x+1, y) in self.empty_list):
                    if ((x+1, y) not in self.kill_pos):
                        self.kill_pos.append((x+1, y))
                elif ((x-2, y) in self.empty_list):
                    if ((x-2, y) not in self.save_pos):
                        self.save_pos.append((x-2, y))

            if ((x, y+1) in self.my_pos) or ((x, y+1) in self.corners):
                if ((x, y-1) in self.empty_list):
                    if ((x, y-1) not in self.kill_pos):
                        self.kill_pos.append((x, y-1))
                elif ((x, y+2) in self.empty_list):
                    if ((x, y+2) not in self.save_pos):
                        self.save_pos.append((x, y+2))

            if ((x, y-1) in self.my_pos) or ((x, y-1) in self.corners):
                if ((x, y+1) in self.empty_list):
                    if ((x, y+1) not in self.kill_pos):
                        self.kill_pos.append((x, y+1))
                elif ((x, y-2) in self.empty_list):
                    if ((x, y-2) not in self.save_pos):
                        self.save_pos.append((x, y-2))

        if type == 1:
            if ((x+1, y) in self.opp_pos) or ((x+1, y) in self.corners):
                if ((x-1, y) in self.empty_list):
                    if ((((x-2, y) in self.opp_pos) or
                         ((x-1, y+1) in self.opp_pos) or
                         ((x-1, y-1) in self.opp_pos))):
                        return (x-1, y)

            if ((x-1, y) in self.opp_pos) or ((x-1, y) in self.corners):
                if ((x+1, y) in self.empty_list):
                    if ((((x+2, y) in self.opp_pos) or
                         ((x+1, y+1) in self.opp_pos) or
                         ((x+1, y-1) in self.opp_pos))):
                        return (x+1, y)

            if ((x, y+1) in self.opp_pos) or ((x, y+1) in self.corners):
                if ((x, y-1) in self.empty_list):
                    if ((((x, y-2) in self.opp_pos) or
                         ((x+1, y-1) in self.opp_pos) or
                         ((x-1, y-1) in self.opp_pos))):
                        return (x, y-1)

            if ((x, y-1) in self.opp_pos) or ((x, y-1) in self.corners):
                if ((x, y+1) in self.empty_list):
                    if ((((x, y+2) in self.opp_pos) or
                         ((x+1, y+1) in self.opp_pos) or
                         ((x-1, y+1) in self.opp_pos))):
                        return (x, y+1)

            return None

    # Function evaluates moves based on the risk of taking them
    #   against the reward caused by it
    def eval_move(self, pos, curr_pos, board, dead):
        x = pos[0]
        y = pos[1]

        empty_list = board[0]
        my_pos = board[1]
        opp_pos = board[2]

        my_dead = dead[0]
        opp_dead = dead[1]

        # If in Moving Phase, remove curr_pos as we will have no piece there
        #       after it moves from it if testing actual move, not the path.
        #       Add it back in after evaluation testing complete
        curr_pos_removed = False
        if self.turn >= 24 and curr_pos in my_pos:
            my_pos.remove(curr_pos)
            curr_pos_removed = True

        # Check if we'll die since there’s an opp next to us
        if (((x+1, y) in opp_pos) or ((x-1, y) in opp_pos) or
                ((x, y+1) in opp_pos) or ((x, y-1) in opp_pos)):

            # In a deadly spot, but we won't die as we're attacking
            if ((((x+1, y) in opp_pos or (x+1, y) in self.corners) and
                ((x-1, y) in opp_pos or (x-1, y) in self.corners) and
                (((x+2, y) in my_pos or (x+2, y) in self.corners) or
                ((x-2, y) in my_pos or (x-2, y) in self.corners))) or
                (((x, y+1) in opp_pos or (x, y+1) in self.corners) and
                ((x, y-1) in opp_pos or (x, y-1) in self.corners) and
                (((x, y+2) in my_pos or (x, y+2) in self.corners) or
                    ((x, y-2) in my_pos or (x, y-2) in self.corners)))):
                # Can cause a loop to form that is not productive in
                #   placing phase
                if (self.turn < 24):
                    return 5
                if curr_pos_removed:
                    my_pos.append(curr_pos)
                return 0

            # In a deadly spot and will die, even if we kill a piece
            elif (((x+1, y) in opp_pos or (x+1, y) in self.corners) and
                  ((x-1, y) in opp_pos or (x-1, y) in self.corners) or
                  (((x, y+1) in opp_pos or (x, y+1) in self.corners) and
                  ((x, y-1) in opp_pos or (x, y-1) in self.corners))):
                if curr_pos_removed:
                    my_pos.append(curr_pos)
                return 20

            if (self.turn >= 24):
                if Player.check_kill_save_pos(self, pos, 1) is not None:
                    # Will die after this turn
                    if curr_pos_removed:
                        my_pos.append(curr_pos)
                    return 20

            if (self.turn < 24):

                # placing phase, don’t go next to an opp unless setting up
                #   to kill it
                if (((x+1, y) in opp_pos and (x-1, y) in my_pos) or
                   ((x-1, y) in opp_pos and (x+1, y) in my_pos) or
                   ((x, y+1) in opp_pos and (x, y-1) in my_pos) or
                   ((x, y-1) in opp_pos and (x, y+1) in my_pos)):
                    # safe, since pos opp needs to kill piece is blocked
                    #    by my piece
                    return 0

                # In own safe starting zone
                elif ((self.y_start == range(0, 6) and (y == 0 or y == 1)) or
                        (self.y_start == range(2, 8) and (y == 7 or y == 6))):
                    return 0

                # Will kill opp and not in a deadly position
                elif (((x+1, y) in opp_pos and (x+2, y) in my_pos) or
                      ((x-1, y) in opp_pos and (x-2, y) in my_pos) or
                      ((x, y+1) in opp_pos and (x, y+2) in my_pos) or
                      ((x, y-1) in opp_pos and
                       (x, y-2) in my_pos)):
                    return 0

                # May die next as next to an opponent
                else:
                    return 10

            # Next to a corner, easier to be killed, especially in the
            # Moving Phase. However, usually a strategic position when the
            # board is at its smallest size
            if ((x+1, y) in self.corners or (x-1, y) in self.corners or
                    (x, y+1) in self.corners or (x, y-1) in self.corners):
                if curr_pos_removed:
                    my_pos.append(curr_pos)
                if (self.turn > 216):
                    return 0
                return 15

        # Not next to opponent, safe
        if curr_pos_removed:
            my_pos.append(curr_pos)
        return 0

    # Function removes goal positions that result in death
    def remove_kamikaze(self, goal, goals):
        x = goal[0]
        y = goal[1]

        if ((x in range(self.min_index+1, self.max_index-1) and
             ((x+1, y) in self.opp_pos and (x-1, y) in self.opp_pos) and
             ((x+2 in range(self.max_index + 1) and
              (x+2, y) not in self.my_pos) or
              (x+2 not in range(self.max_index + 1))) and
             ((x-2 in range(self.max_index + 1) and
              (x-2, y) not in self.my_pos) or
              (x+2 not in range(self.max_index + 1))))):

            Player.remove_goal_pos(self, goals, x, y)

        if (y in range(self.min_index+1, self.max_index-1) and
            ((x, y+1) in self.opp_pos and (x, y-1) is self.opp_pos) and
            ((y+2 in range(self.max_index + 1) and
             (x, y+2) not in self.my_pos) or
             (y+2 not in range(self.max_index + 1))) and
            ((y-2 in range(self.max_index + 1) and
             (x, y-2) not in self.my_pos) or
             (y+2 not in range(self.max_index + 1)))):

            Player.remove_goal_pos(self, goals, x, y)

    # Check if piece already partially surrounded
    #   and mark goal positions for Player
    def find_goal_pos(self, x, y):

        goals = []
        flanks = []

        # If no Player pieces surround Opponent,
        #   all surrounding tiles are valid goals
        #   and will kill the opponent equally well
        if ((x+1 in range(self.max_index + 1)) and
           ((x+1, y) in self.empty_list)):
            goals.append((x+1, y))
        if ((x-1 in range(self.max_index + 1)) and
           ((x-1, y) in self.empty_list)):
            goals.append((x-1, y))
        if ((y+1 in range(self.max_index + 1)) and
           ((x, y+1) in self.empty_list)):
            goals.append((x, y+1))
        if ((y-1 in range(self.max_index + 1)) and
           ((x, y-1) in self.empty_list)):
            goals.append((x, y-1))

        # If piece already surrounded by one Player piece,
        #   or is next to a corner, opposite square is goal
        if ((x+1 in range(self.max_index + 1)) and
           (x-1 in range(self.max_index + 1)) and
           (((x+1, y) in self.my_pos) or (x+1, y) in self.corners)):
            goals.append((x-1, y))
            flanks.append((x+1, y))

            if (x, y+1) in goals:
                goals.remove((x, y+1))
            if (x, y-1) in goals:
                goals.remove((x, y-1))

        if ((x-1 in range(self.max_index + 1)) and
           (x+1 in range(self.max_index + 1)) and (((x-1, y) in self.my_pos) or
           (x-1, y) in self.corners)):
            goals.append((x+1, y))
            flanks.append((x-1, y))

            if (x, y+1) in goals:
                goals.remove((x, y+1))
            if (x, y-1) in goals:
                goals.remove((x, y-1))

        if ((y+1 in range(self.max_index + 1)) and
           (y-1 in range(self.max_index + 1)) and (((x, y+1) is self.my_pos) or
           (x, y+1) in self.corners)):
            goals.append((x, y-1))
            flanks.append((x, y+1))

            if (x+1, y) in goals:
                goals.remove((x+1, y))
            if (x-1, y) in goals:
                goals.remove((x-1, y))

        if ((y-1 in range(self.max_index + 1)) and
           (y+1 in range(self.max_index + 1)) and (((x, y-1) is self.my_pos) or
           (x, y-1) in self.corners)):
            goals.append((x, y+1))
            flanks.append((x, y-1))

            if (x+1, y) in goals:
                goals.remove((x+1, y))
            if (x-1, y) in goals:
                goals.remove((x-1, y))

        # if Opponent is on the edge of the board, the position parallel
        #   to the boarder, on either side of the opponent, are goals
        if ((x+1 not in range(self.max_index + 1)) and
            ((y+1 in range(self.max_index + 1) and
              (x, y+1) in self.empty_list) and
            ((y-1 in range(self.max_index + 1)) and
             (x, y-1) in self.empty_list))):
            goals.append((x, y+1))
            goals.append((x, y-1))
            if (x-1, y) in goals:
                goals.remove((x-1, y))

        if ((x-1 not in range(self.max_index + 1)) and
            ((y+1 in range(self.max_index + 1) and
             (x, y+1) in self.empty_list) and
            ((y-1 in range(self.max_index + 1)) and
             (x, y-1) in self.empty_list))):
            goals.append((x, y+1))
            goals.append((x, y-1))
            if (x+1, y) in goals:
                goals.remove((x+1, y))

        if ((y+1 not in range(self.max_index + 1)) and
            ((x+1 in range(self.max_index + 1) and
             (x+1, y) in self.empty_list) and
            ((x-1 in range(self.max_index + 1)) and
             (x-1, y) in self.empty_list))):
            goals.append((x+1, y))
            goals.append((x-1, y))
            if (x, y-1) in goals:
                goals.remove((x, y-1))

        if ((y-1 not in range(self.max_index + 1)) and
            ((x+1 in range(self.max_index + 1) and
             (x+1, y) in self.empty_list) and
            ((x-1 in range(self.max_index + 1)) and
             (x-1, y) in self.empty_list))):
            goals.append((x+1, y))
            goals.append((x-1, y))
            if (x, y+1) in goals:
                goals.remove((x, y+1))

        # Remove any goals that will result in self.my_pos's death
        for goal in goals:
            Player.remove_kamikaze(self, goal, goals)
        return [goals, flanks]

    # Remove co-ordinate from goal list
    def remove_goal_pos(self, goals, x, y):

        if ((x+1, y) in goals and (x+2, y) not in targets and
           (x+1, y+1) not in targets and (x+1, y-1) not in targets):
            goals.remove((x+1, y))
        if ((x-1, y) in goals and (x-2, y) not in targets and
           (x-1, y+1) not in targets and (x-1, y-1) not in targets):
            goals.remove((x-1, y))
        if ((x, y+1) in goals and (x, y+2) not in targets and
           (x-1, y+1) not in targets and (x+1, y+1) not in targets):
            goals.remove((x, y+1))
        if ((x, y-1) in goals and (x, y-2) not in targets and
           (x-1, y-1) not in targets and (x+1, y-1) not in targets):
            goals.remove((x, y-1))

    # Function to check the available moves surrounding a piece
    def check_moves(self, x, y):
        moves = []
        # Check square to right
        if ((x+1 in range(self.max_index + 1)) and
           ((x+1, y) in self.empty_list)):
            moves.append(((x, y), (x+1, y)))
        # Check square to left
        if ((x-1 in range(self.max_index + 1)) and
           ((x-1, y) in self.empty_list)):
            moves.append(((x, y), (x-1, y)))
        # Check square below
        if ((y+1 in range(self.max_index + 1)) and
           ((x, y+1) in self.empty_list)):
            moves.append(((x, y), (x, y+1)))
        # Check square above
        if ((y-1 in range(self.max_index + 1)) and
           ((x, y-1) in self.empty_list)):
            moves.append(((x, y), (x, y-1)))

        # Check if piece can jump to right
        if ((x+2 in range(self.max_index + 1)) and
           (((x+1, y) in self.my_pos) or
           ((x+1, y) in self.opp_pos)) and ((x+2, y) in self.empty_list)):
            moves.append(((x, y), (x+2, y)))
        # Check if piece can jump to left
        if ((x-2 in range(self.max_index + 1)) and
           (((x-1, y) in self.my_pos) or
           ((x-1, y) in self.opp_pos)) and ((x-2, y) in self.empty_list)):
            moves.append(((x, y), (x-2, y)))
        # Check if piece can jump down
        if ((y+2 in range(self.max_index + 1)) and
           (((x, y+1) in self.my_pos) or
           ((x, y+1) in self.opp_pos)) and ((x, y+2) in self.empty_list)):
            moves.append(((x, y), (x, y+2)))
        # Check if piece can jump up
        if ((y-2 in range(self.max_index + 1)) and
           (((x, y-1) in self.my_pos) or
           ((x, y-1) in self.opp_pos)) and ((x, y-2) in self.empty_list)):
            moves.append(((x, y), (x, y-2)))

        return moves

    def moves(self, type=0):
        # Initialise moves variables
        my_moves = []

        # For each square on board:
        #       - check if it's a piece
        #       - if so, count available moves
        if type == 0:
            for x in range(self.max_index + 1):
                for y in range(self.max_index + 1):
                    if (x, y) in self.my_pos:
                        # Check available spaces
                        my_moves = my_moves + Player.check_moves(self, x, y)

            return my_moves
        if type == 1:
            for x in range(self.max_index + 1):
                for y in range(self.max_index + 1):
                    if (x, y) in self.opp_pos:
                        # Check available spaces
                        my_moves = my_moves + Player.check_moves(self, x, y, 1)

            return my_moves

    # Function checks if there is a safe position two away from an opponent
    def check_two_away(self, pos):
        x = pos[0]
        y = pos[1]

        if ((x+2 in range(self.max_index + 1)) and
           ((x+2, y) in self.empty_list) and
           Player.eval_move(self, (x+2, y), pos,
                            [self.empty_list, self.my_pos, self.opp_pos], 
                            [self.my_dead, self.opp_dead]) == 0):
            return(x+2, y)
        if ((x-2 in range(self.max_index + 1)) and
           ((x-2, y) in self.empty_list) and
           Player.eval_move(self, (x-2, y), pos, 
                            [self.empty_list, self.my_pos, self.opp_pos], 
                            [self.my_dead, self.opp_dead]) == 0):
            return(x-2, y)
        if ((y+2 in range(self.max_index + 1)) and
           ((x, y+2) in self.empty_list)and
           Player.eval_move(self, (x, y+2), pos,
                            [self.empty_list, self.my_pos, self.opp_pos], 
                            [self.my_dead, self.opp_dead]) == 0):
            return(x, y+2)
        if ((y-2 in range(self.max_index + 1)) and
           ((x, y-2) in self.empty_list) and
           Player.eval_move(self, (x, y-2), pos,
                            [self.empty_list, self.my_pos, self.opp_pos], 
                            [self.my_dead, self.opp_dead]) == 0):
            return(x, y-2)
        return None

    # Checks if position is on the edge of the board
    def on_boarder(self, pos):
        if ((pos[0] == self.min_index) or
           (pos[1] == self.min_index) or
           (pos[0] == self.max_index) or
           (pos[1] == self.max_index) or
           (pos == (self.min_index+1, self.min_index+1)) or
           (pos == (self.min_index+1, self.max_index-1)) or
           (pos == (self.max_index-1, self.min_index+1)) or
           (pos == (self.max_index-1, self.max_index-1))):
            return True
        else:
            return False

    # Function to make sure our pieces live to fight another day
    def about_to_die(self, pos):
        x = pos[0]
        y = pos[1]

        # Check if there is an opponent one move away from killing our piece
        killing_move_pos = Player.check_kill_save_pos(self, pos, 1)
        if killing_move_pos is None:
            return None
        else:
            # See if there's any safe places for our piece to run to
            if Player.eval_move(self, killing_move_pos, pos,
                                [self.empty_list, self.my_pos, self.opp_pos],
                                [self.my_dead, self.opp_dead]) < 20:
                return killing_move_pos
            else:
                if (x+1, y) in self.empty_list:
                    if Player.eval_move(self, (x+1, y), pos,
                                        [self.empty_list, self.my_pos,
                                         self.opp_pos],
                                        [self.my_dead,
                                         self.opp_dead]) < 20:
                        return (x+1, y)
                if (x-1, y) in self.empty_list:
                    if Player.eval_move(self, (x-1, y), pos,
                                        [self.empty_list, self.my_pos,
                                         self.opp_pos],
                                        [self.my_dead,
                                         self.opp_dead]) < 20:
                        return (x-1, y)
                if (x, y+1) in self.empty_list:
                    if Player.eval_move(self, (x, y+1), pos,
                                        [self.empty_list, self.my_pos,
                                         self.opp_pos],
                                        [self.my_dead,
                                         self.opp_dead]) < 20:
                        return (x, y+1)
                if (x, y-1) in self.empty_list:
                    if Player.eval_move(self, (x, y-1), pos,
                                        [self.empty_list, self.my_pos,
                                         self.opp_pos],
                                        [self.my_dead,
                                         self.opp_dead]) < 20:
                        return (x, y-1)

    # ----------------------------SEARCH FUNCTIONS-----------------------------

    # ***
    #    The following is based upon and modified from code posted online at:
    #    Title: Implementing Depth Limited Path Finding with Stack
    #    Author: Screennames "Brian" and "RootTwo"
    #    Date: 12 Feb 2016, 21:03
    #   Availability: https://stackoverflow.com/questions/35261256/implementing
    #                 -depth-limited-path-finding-with-stack
    # ***

    # Searching algorithm function: Depth Limited Search
    def depth_limited_search(self, start, goals, depth):
        SENTINEL = object()
        path = []
        visited = [start]

        while visited:

            current = visited.pop()
            # once goal state reached, return the path to it
            if current in goals and current != start:
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

    # ***
    #    END OF MODIFIED CODE
    # ***

    def minimax(self, board, depth, type, node, move):
        if (((depth == 0) or (Player.moves(self, type) is None) or 
             (board[4] > 11) or (board[5] > 11))):
            value = Player.eval_move(self, node[1], node[0], board, dead)
            if type == 0:
                return -value
            elif type == 1:
                return value

        if type == 0:
            best_value = -1000000
            moves_list = Player.moves(self, 0)
            for child in moves_list:
                if node == (-1, -1):
                    move = child
                Player.update_pos(self, child, board, 0, 1)
                Player.check_confirmed_kill(self, child[1], child[0],
                                            board, [board[3], board[4]],
                                            0)
                v = [Player.minimax(self, board, depth-1, 1, child, move), move]
                if v[0] > best_value:
                    return v[0]
                else:
                    return best_value

        if type == 1:
            best_value = 1000000
            moves_list = Player.moves(self, 1)
            for child in moves_list:
                if node == (-1, -1):
                    move = child
                Player.update_pos(self, child, board, 1, 1)
                Player.check_confirmed_kill(self, child[1], child[0],
                                            board, [board[4], board[3]],
                                            1)
                v = [Player.minimax(self, board, depth-1, 0, child, move), move]
                if v[0] < best_value:
                    return v[0]
                else:
                    return best_value

    # -------------------------END OF SEARCH FUNCTIONS-------------------------
    # __________________________________________________________________________

    # __________________________________________________________________________
    #                                 action
    # __________________________________________________________________________

    def action(self, turns):
        self.turn += 1

        # Handling board shrinking at Moving Turn 127
        if self.turn == 152:
            self.min_index = 1
            self.max_index = 6
            self.corners = Player.update_corners(self)

            self.kill_pos = []
            self.save_pos = []
            for pos in self.opp_pos:
                Player.check_kill_save_pos(self, pos)

        # And at Moving Turn 191
        elif self.turn == 216:
            self.min_index = 2
            self.max_index = 5
            self.corners = Player.update_corners(self)

            self.kill_pos = []
            self.save_pos = []
            for pos in self.opp_pos:
                Player.check_kill_save_pos(self, pos)

        if self.turn < 24:
            # Placing Phase:
            # Will return a tuple

            # If we have the first move, choose a random position
            if self.turn == 0:
                while(True):
                    x = random.randint(self.min_index, self.max_index)
                    y = random.randint(self.y_start_list[0],
                                       self.y_start_list[-1])
                    if (x, y) not in self.corners:
                        self.my_pos.append((x, y))
                        self.empty_list.remove((x, y))
                        return (x, y)

            # First priority is to save our pieces if needed
            # but only if it is a safe move to take
            if len(self.save_pos) != 0:
                for i in range(len(self.save_pos)):
                    if self.save_pos[i][1] in self.y_start_list:
                        if self.save_pos[i] in self.empty_list:
                            if Player.eval_move(self, self.save_pos[i],
                                                [self.empty_list, self.my_pos,
                                                 self.opp_pos],
                                                [self.my_dead,
                                                 self.opp_dead],
                                                (-1, -1)) == 0:
                                pos = self.save_pos[i]
                                Player.update_pos(self, pos, [self.empty_list,
                                                              self.my_pos, 
                                                              self.opp_pos], 0)
                                return pos

            # Second priority is to place pieces in positions that
            #    will kill an opponent, as long as it won't kill our piece
            if len(self.kill_pos) != 0:
                for i in range(len(self.kill_pos)):
                    if self.kill_pos[i][1] in self.y_start_list:
                        if self.kill_pos[i] in self.empty_list:
                            if Player.eval_move(self, self.kill_pos[i],
                                                [self.empty_list, self.my_pos,
                                                 self.opp_pos], 
                                                [self.my_dead,
                                                 self.opp_dead],
                                                 (-1, -1)) == 0:
                                pos = self.kill_pos[i]
                                Player.check_confirmed_kill(self, pos,
                                                            (-1, -1), 
                                                            [self.empty_list, 
                                                             self.my_pos, 
                                                             self.opp_pos], 
                                                            [self.my_dead, 
                                                             self.opp_dead], 0)

                                Player.update_pos(self, pos, [self.empty_list, 
                                                              self.my_pos, 
                                                              self.opp_pos], 0)
                                return pos

        # If no priorising places, place a piece somewhere so that it
        #    is not next to an opponent (therefore preventing it from being
        #    taken in the next turn)
            for pos in self.opp_pos:
                # check surrounds of position 2 away so not going into a
                #   spot where will die
                result = Player.check_two_away(self, pos)
                if result is not None:
                    if result[1] in self.y_start_list:
                        if result in self.empty_list:
                            Player.update_pos(self, result, [self.empty_list, 
                                                             self.my_pos, 
                                                             self.opp_pos], 0)
                            return result
            while(True):
                pos = self.empty_list[random.randint(0,
                                                     len(self.empty_list)-1)]
                if pos[1] in self.y_start_list:
                        if Player.eval_move(self, pos, (-1, -1),
                                            [self.empty_list, self.my_pos,
                                             self.opp_pos],
                                            [self.my_dead,
                                             self.opp_dead]) == 0:
                            Player.update_pos(self, pos, [self.empty_list, 
                                                          self.my_pos, 
                                                          self.opp_pos],0)
                            return pos

        else:
            # Moving Phase
            # Will return a nested tuple

            # Reset kill_pos and save_pos*
            # and update it to ensure all new kill_pos are found
            #   *Save_pos will never be used in the Moving Phase
            if self.turn == 24:
                self.kill_pos = []
                self.save_pos = []
                for pos in self.opp_pos:
                    Player.check_kill_save_pos(self, pos)

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

            # Find all possible moves,
            # returns array of nested tuples (current pos, next pos)
            moves_list = Player.moves(self)

            if len(moves_list) < 1:
                # No avaliable moves, have to forfeit the move
                return None

            # Set a dictionary to be used for index keys and distance values
            eval_dict = defaultdict()

            if self.my_dead > 8:
                board = []
                empty = []
                my = []
                opp = []
                for pos in self.empty_list:
                    empty.append(pos)
                board[0] = empty
                for pos in self.my_pos:
                    my.append(pos)
                board[1] = my
                for pos in self.opp_pos:
                    opp.append(pos)
                board[2] = opp

                board.append(self.my_dead) 
                board.append(self.opp_dead)

                returns = Player.minimax(self, board, 4, 0, (-1,-1), ((-1, -1), (-1, -1)))
                if returns is not None:
                    return returns[1]

            # For every valid possible move, find the distance to the nearest
            # goal to evaluate the move
            for i in range(len(moves_list)):

                if (moves_list[i][1] not in self.empty_list):
                    continue

                priority_move = Player.about_to_die(self, moves_list[i][0])
                if priority_move is not None:
                    # One of our pieces is about to die, so let it flee!
                    action = (moves_list[i][0], priority_move)
                    if i != moves_list.index(action):
                        result = (Player.depth_limited_search(self,
                                                              moves_list[i][1],
                                                              self.goals, 10))
                        priority = 50
                    else:
                        result = [priority_move]
                        if (self.turn > 216):
                            priority = -10
                        else:
                            priority = -30

                elif ((Player.on_boarder(self, moves_list[i][0]) and
                      ((self.turn > (152-(12-self.my_dead)) and
                        self.turn < 152) or
                       (self.turn > (216-(12-self.my_dead)) and
                        self.turn < 216)))):
                    # Coming up to the shrinking of the board, make sure pieces
                    #   aren't on the boarders
                    result = (Player.depth_limited_search(self,
                                                          moves_list[i][1],
                                                          self.next_boarders,
                                                          10))
                    # Give higher priority to moving pieces
                    priority = -20

                else:
                    result = (Player.depth_limited_search(self,
                                                          moves_list[i][1],
                                                          self.goals, 10))
                    priority = 0

                # If the piece can't reach a goal position, set the starting
                # value at 100. If it can, set it to the number of moves
                # away it is
                if result is None:
                    val = 100
                else:
                    val = len(result)

                val += priority

                # Higher Priority give to the moves that kill another
                if moves_list[i][1] not in self.kill_pos:
                    if self.turn > 216:
                        val += 100
                    else:
                        val += 30

                # Lower Priority given to those that are already sitting in a
                #   flanking position
                if moves_list[i][0] in self.flanks:
                    if self.turn > 216:
                        val += 1
                    else:
                        val += 30

                if (Player.on_boarder(self, moves_list[i][1]) and
                    (self.turn > (152-((12-self.my_dead)/2) and
                     self.turn < 152) or
                    (self.turn > (216-((12-self.my_dead)/2)) and
                        self.turn < 216))) and priority == 0:
                    val += 50

                # if move is a dumb move, add more to val
                first_eval = Player.eval_move(self, moves_list[i][1],
                                              moves_list[i][0],
                                              [self.empty_list, self.my_pos,
                                               self.opp_pos],
                                              [self.my_dead,
                                               self.opp_dead])
                val += first_eval
                # Piece dies immediately
                if first_eval == 20:
                    val += 100

                if result is not None:
                    for j in range(len(result)-1):
                        val += Player.eval_move(self, result[j], result[j+1],
                                                [self.empty_list, self.my_pos,
                                                 self.opp_pos], 
                                                [self.my_dead,
                                                 self.opp_dead])

                # Then add index of move as key and shortest dist as value
                #   in dictionary
                eval_dict[i] = val

            l = list(eval_dict.items())
            action = (-1, -1)

            for key, value in sorted(l,
                                     key=lambda item: (item[1], item[0])):
                action = moves_list[key]
                break

            if action != (-1, -1):
                # sort dictionary, use key (index of moves) to find and return
                #   that move
                Player.update_pos(self, action, [self.empty_list, 
                                                 self.my_pos, 
                                                 self.opp_pos],0)
                Player.check_confirmed_kill(self, action[1], action[0],
                                            [self.empty_list, self.my_pos,
                                             self.opp_pos],
                                            [self.my_dead, self.opp_dead],
                                            0)
                return action
            else:
                return None

    # __________________________________________________________________________
    # __________________________________________________________________________
    #                                 update
    # __________________________________________________________________________

    def update(self, action):
        self.turn += 1

        # Handling board shrinking
        if self.turn == 152:
            self.min_index = 1
            self.max_index = 6
            self.corners = Player.update_corners(self)

            self.kill_pos = []
            self.save_pos = []
            for pos in self.opp_pos:
                Player.check_kill_save_pos(self, pos)

        elif self.turn == 216:
            self.min_index = 2
            self.max_index = 5
            self.corners = Player.update_corners(self)

            self.kill_pos = []
            self.save_pos = []
            for pos in self.opp_pos:
                Player.check_kill_save_pos(self, pos)

        # Updating opp_pos and checking for goal positions and deaths
        if self.turn < 24:
            # Placing Phase
            Player.update_pos(self, action, [self.empty_list, 
                                             self.my_pos, 
                                             self.opp_pos], 1)
            Player.check_confirmed_kill(self, action, (-1, -1),
                                        [self.empty_list, self.my_pos, 
                                         self.opp_pos], 
                                        [self.my_dead, self.opp_dead],  1)
            Player.check_kill_save_pos(self, action)

        else:
            # Moving Phase
            if self.turn == 24:
                self.kill_pos = []
                self.save_pos = []

            Player.update_pos(self, action, [self.empty_list, 
                                             self.my_pos, 
                                             self.opp_pos], 1)
            Player.check_confirmed_kill(self, action[1], action[0],
                                        [self.empty_list, self.my_pos, 
                                         self.opp_pos], 
                                        [self.my_dead, self.opp_dead], 1)
            Player.check_kill_save_pos(self, action[1])

"""
__________________________________________________________________________
                                END OF CODE
__________________________________________________________________________
"""
