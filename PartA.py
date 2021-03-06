#Define symbols

empty = "-"
white = "O"
black = "@"
player = (black, white)

# initialise board matrix

board = []
attackers = []
targets = []
goals = []

#############################################
class player:
    def __init__(self, colour, in_goal)
        self.colour = colour
        self.in_goal = in_goal

white = player()
black = player()

#############################################


# Load board and game_type
for i in range(8):
    board[i] = input().replace(" ", "")
    #board[i] = input().split()
game_type = input()

# Check game_type
#------------------------MOVES------------------------
if game_type is Moves:

    # Initialise moves variables
    moves_O = 0
    moves_at = 0

    # For each square on board:
    #       - check if it's a piece
    #       - if so, count avaliable moves

    for x in range(8):
        for y range(8):
            if board[x][y] is white:
                #Check avaliable spaces
                moves_O += CheckMoves(board,x,y)

            elif board[x][y] is black:
                #Check avaliable spaces
                moves_at += CheckMoves(board,x,y)


#---------------------MASSACRE----------------------
elif game_type is Massacre:

    # Store locations of Black and White pieces

    num_white = 0
    num_black = 0

    for x in range(8):
        for y range(8):
            if board[x][y] is white:
                attackers.append((x,y))
                num_white += 1

            elif board[x][y] is black:
                targets.append((x,y))
                find_goal_pos(targets(x,y))
                num_black += 1

    for i in range(num_white):
        if attackers[i] is in_goal_pos(attackers[i]):
            i += 1
        else
            it_depth_search(attackers[i])

#------------------HELPER FUNCTIONS-----------------

# Function to check the avaliable moves surrounding a piece

def CheckMoves(board, x, y):
    moves = 0
    if board[x+1][y] is empty:
        moves+=1
    if board[x-1][y] is empty:
        moves+=1
    if board[x][y+1] is empty:
        moves+=1
    if board[x][y-1] is empty:
        moves+=1

    if (x+2 is in range(8)) and (board[x+1][y] in player)
    and (board[x+2][y] is empty):
        moves+=1
    if (x-2 is in range(8)) and (board[x-1][y] in player)
    and (board[x-2][y] is empty):
        moves+=1
    if (y+2 is in range(8)) and (board[x][y+1] in player)
    and (board[x][y+2] is empty):
        moves+=1
    if (y-2 is in range(8)) and (board[x][y-1] in player)
    and (board[x][y-2] is empty):
        moves+=1

    return moves

# Check if piece already partially surrounded and mark goal positions for white

def find_goal_pos(x,y):

    # If no white pieces surround black, all surrounding tiles are valid goals

    if (board[x+1][y] is empty and board[x-1][y] is empty
    and board[x][y+1] is empty and board[x][y-1] is empty):

        goals.append((x+1,y))
        goals.append((x-1,y))
        goals.append((x,y+1))
        goals.append((x,y-1))

    # If piece already surrounded by one white piece, adjacent square is goal

    if (board[x+1][y] is white):
        goals.append((x-1,y))
    if (board[x-1][y] is white):
        goals.append((x+1,y))
    if (board[x][y+1] is white):
        goals.append((x,y-1))
    if (board[x][y-1] is white):
        goals.append((x,y+1))

def in_goal_pos(x,y):

    # Check that the white piece is in a goal pos

    if (board[x+1][y] is black or board[x-1][y] is black
    or board[x][y+1] is black or board[x][y-1] is black):
        return 1
    else
        return 0

def check_taken(x,y):


def check_win(board):
