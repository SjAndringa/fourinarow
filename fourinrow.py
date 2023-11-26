"""
Game Player
"""

import math

X = "X"
O = "O"
EMPTY = None
nrows = 6
ncolumns = 7
nr = 4
dl = 4

def initial_state():
    """
    Returns starting state of the board.
    """
    columns = [EMPTY for x in range(ncolumns)]
    state = [list(columns) for x in range(nrows)]
    return state

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    nX=0
    nO=0
    for i in range(nrows):
        for j in range(ncolumns):
            cell=board[i][j]
            if cell==X:
                nX += 1
            elif cell==O:
                nO += 1
    return X if nX <= nO else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible=set()
    for i in range(nrows):
        for j in range(ncolumns):
            if i == 0:
                if board[i][j] == EMPTY:
                    possible.add((i,j))
            else:
                if (board[i][j] == EMPTY) and board[i-1][j] is not EMPTY:
                    possible.add((i,j))
    return possible


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newboard=deepcopy(board)
    newboard[action[0]][action[1]]=player(board)
    #print(newboard)
    return newboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    """
    if player(board)==X:
        w=O
    else:
        w=X
    print("kijken of deze speler winnaar is ",w)
    """
    
    #rows
    for i in range(nrows):
        for j in range(ncolumns - nr):
            if alln(board,i,j,True):
                return board[i][j]
    #columns
    for j in range(ncolumns):
        for i in range(nrows - nr):
            if alln(board,i,j,False):
                return board[i][j]
    #diagonals to the right
    for i in range(nrows-nr):
        for j in range(ncolumns - nr):
            if alld(board,i,j,True):
                return board[i][j]
    #diagonals to the left
    for i in range(nrows-nr):
        for j in range(ncolumns - nr):
            if alld(board,i,j,False):
                return board[i][j]
    #when no return occurred, no nr in a row
    return False


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    if winner(board) in [X,O]:
        #print("goed gespeeld door: ",dezewinnaar)
        return True
    elif bordvol(board):
        return True
    else:
        return False
    

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    Maybe use preliminaryutility more 4 in a row means 4 for winner X of -4 for winner O
    """
    dezewinnaar=winner(board)
    if dezewinnaar==X:
        return 1
    elif dezewinnaar==O:
        return -1
    else:
        return 0

def preliminaryutility(board,maxaantal):
    '''
    returns a preliminary utility if no winner yet
    3 or 2 for X, -3 or -3 for O
    called from minimax when depth is reached
    '''
    for aantal in range(1,maxaantal):
        #rows
        for i in range(nrows):
            for j in range(ncolumns - nr):
                if board[i][j] in [X,O] and alln(board,i,j,True,aantal):
                    return (board[i][j],aantal) if board[i][j]==X else (board[i][j],-aantal)
        # rows
        for j in range(ncolumns):
            for i in range(nrows - nr):
                if board[i][j] in [X, O] and alln(board, i, j, False, aantal):
                    return (board[i][j], aantal) if board[i][j] == X else (board[i][j], -aantal)
        # diagonals to the right
        for i in range(nrows - nr):
            for j in range(ncolumns - nr):
                if board[i][j] in [X,O] and alld(board, i, j, True, aantal):
                    return (board[i][j], aantal) if board[i][j] == X else (board[i][j], -aantal)
        # diagonals to the left
        for i in range(nrows - nr):
            for j in range(ncolumns - nr):
                if if board[i][j] in [X,O] and alld(board, i, j, False, aantal):
                    return (board[i][j], aantal) if board[i][j] == X else (board[i][j], -aantal)
        # when no return occurred, no nr in a row
        return 0

def minimax(board,limit):
    """
    Returns the optimal action for the current player on the board.
    """
    
    if terminal(board):
        return
    if player(board)==X:
        w=max_value(board,-math.inf,math.inf,limit)
    else:
        w=min_value(board,-math.inf,math.inf,limit)
    return w[0]
        
def max_value(board,alpha,beta,limit):
    #returns [move,value] that maximizes score
    #v=-math.inf
    w=[None,alpha]
    # w[0] is move w[1] is value of utility
    if limit < 0:
        return w
    if terminal(board):
        #print("max_value returns ",utility(board))
        # de regel hieronder kan niet goed zijn
        return [w,utility(board)]
    for action in actions(board):
        temp=min_value(result(board,action),alpha,beta,limit-1)
        
        if temp[1]>alpha:
            alpha=temp[1]
            w=[action,temp[1]]
        if alpha >= beta:
            #print("pruned from max-value")
            break
        # je moet ook nog de action erbij geven
    return w

def min_value(board,alpha,beta,limit):
    #v=100
    w=[None,beta]
    # w[0] is move w[1] is value of utility
    if limit < 0:
        return [w,preliminaryutility(board,nr-1)]
    if terminal(board):
        #print("min_value returns ",utility(board))
        return [w,utility(board)]

    for action in actions(board):
        temp=max_value(result(board,action),alpha,beta,limit-1)
        if temp[1]<beta:
            beta=temp[1]
            w=[action,temp[1]]
        if alpha >= beta:
            #print("pruned from min-value")
            break
        # je moet ook nog de action erbij geven
    return w

def deepcopy(board):
    import copy
    return copy.deepcopy(board)

def allthree(a,b,c):
    return (a==b and b==c and a in [X,O])

def alln(board,i,j,rows, aantal):
    if rows:
        for k in range(aantal):
            if not board[i][j+k] == board[i][j+k+1]:
                return False
        return True
    else:
        for k in range(aantal):
            if not board[i+k][j] == board[i+k+1][j]:
                return False
        return True

def alld(board,i,j,upright,aantal):
    if upright:
        for k in range(aantal):
            if not board[i+k][j+k] == board[i+k+1][j+k+1]:
                return False
        return True
    else:
        for k in range(aantal):
            if not board[i+k][j-k] == board[i+k+1][j-k-1]:
                return False
        return True

def bordvol(board):
    for i in range(nrows):
        for j in range(ncolumns):
            if board[i][j]is EMPTY:
                return False
    return True
