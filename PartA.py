# initialise board matrix
#board = [[0 for col in range(8)] for row in range(8)]

empty = "-"
white = "O"
black = "@"
player = (black, white)

board = []
attackers = []
targets = []
goals = []

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

    for x in range(8):
        for y range(8):
            if board[x][y] is white:
                attackers.append((x,y))

            elif board[x][y] is black:
                targets.append((x,y))
                goal_pos(targets(x,y))



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

    if (x+2 is in range(8)) and (board[x+1][y] in player) and (board[x+2][y] is empty):
        moves+=1
    if (x-2 is in range(8)) and (board[x-1][y] in player) and (board[x-2][y] is empty):
        moves+=1
    if (y+2 is in range(8)) and (board[x][y+1] in player) and (board[x][y+2] is empty):
        moves+=1
    if (y-2 is in range(8)) and (board[x][y-1] in player) and (board[x][y-2] is empty):
        moves+=1

    return moves

def goal_pos(x,y):
    if (board[x+1][y] is empty and board[x-1][y] is empty
        and board[x][y+1] is empty and board[x][y-1] is empty):

        goals.append((x+1,y))
        goals.append((x-1,y))
        goals.append((x,y+1))
        goals.append((x,y-1))

    if (board[x+1][y] is white):
        goals.append((x-1,y))
    if (board[x-1][y] is white):
        goals.append((x+1,y))
    if (board[x][y+1] is white):
        goals.append((x,y-1))
    if (board[x][y-1] is white):
        goals.append((x,y+1))

def check_taken(x,y):


def check_win(board):
