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
dl = 6

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
            elif (board[i][j] == EMPTY) and board[i-1][j] is not EMPTY:
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
    #dummyboard=[[O, X, X, X, O, X, None], [None, X, O, X, X, O, None], [None, O, X, X, X, O, None], [None, O, O, O, X, X, None], [None, None, None, None, O, None, None], [None, None, None, None, None, None, None]]
    #assert alln(dummyboard,nr) == X
    #return alln(dummyboard,nr)
    return alln(board,nr)


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
    This can be done otherwise
    4 in a row means 4 for winner X of -4 for winner O
    3 if 3 out of 4 in a row for X etcetera
    """
    '''
    aantal op rij is maximaal aantal (=nr = 4)
    dit telt aantal op rij van dezelfde soort
    tussendoor mogen wel lege plekken zijn
    maar geen velden van de andere soort
    elke X > 1 op rij levert 1 punt op --> 2, 3 of 4
    elke O > 1 op rij levert -1 punt op --> -2, -3 of -4
    als deze functie 4 = aantal oplevert is X de winnaar
    en als deze functie -4 = -aantal oplevert is O de winnaar

    '''

    countX = 0
    countO = 0
    
    #countX of countO counts number in a row of one sort
    #[rows,columns,diagonals upright, diagonals upleft]
    
    #rows
    for i in range(nrows):
        for j in range(ncolumns - nr):
            k = 0
            #hier ging iets mis: countX[n] blijft doortellen
            tempcount = 0
            while board[i][j+k] in [X,EMPTY] and k < nr:
                if board[i][j+k] ==X:
                    tempcount += 1
                k += 1
            countX = max(countX,tempcount)
            k = 0
            tempcount = 0
            while board[i][j+k] in [O,EMPTY] and k < nr:
                if board[i][j+k] ==O:
                    tempcount += 1
                k += 1
            countO = max(countO,tempcount)
    #columns
    for j in range(ncolumns):
        for i in range(nrows - nr):
            k = 0
            tempcount = 0
            while board[i+k][j] in [X,EMPTY] and k < nr:
                if board[i+k][j] ==X:
                    tempcount += 1
                k += 1
            countX = max(countX,tempcount)
            k = 0
            tempcount = 0
            while board[i+k][j] in [O,EMPTY] and k < nr:
                if board[i+k][j] ==O:
                    tempcount += 1
                k += 1
            countO = max(countO, tempcount)
    #diagonals upright:
    for i in range(nrows - nr):
        for j in range(ncolumns - nr):   
            k = 0
            tempcount = 0
            while board[i+k][j+k] in [X,EMPTY] and k < nr:
                if board[i+k][j+k] ==X:
                    tempcount += 1
                k += 1
            countX = max(countX,tempcount)
            k = 0
            tempcount = 0
            while board[i+k][j+k] in [O,EMPTY] and k < nr:
                if board[i+k][j+k] ==O:
                    tempcount += 1
                k += 1
            countO = max(countO,tempcount)
    #diagonals upleft
    for i in range(nrows - nr):
        for j in range(ncolumns - 1, ncolumns - nr, -1):
            k = 0
            tempcount = 0
            while board[i+k][j-k] in [X,EMPTY] and k < nr:
                if board[i+k][j-k] ==X:
                    tempcount += 1
                k += 1
            countX = max(countX,tempcount)
            k = 0
            tempcount = 0
            while board[i+k][j-k] in [O,EMPTY] and k < nr:
                if board[i+k][j-k] ==O:
                    tempcount += 1
                k += 1
            countO = max(countO,tempcount)
    
    if countX == countO:
        return 0
    if countX > countO:
        return countX
    else:
        return -countO   

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    if terminal(board):
        return
    if player(board)==X:
        w=max_value(board,-math.inf,math.inf,dl)
    else:
        w=min_value(board,-math.inf,math.inf,dl)
    return w[0]
        
def max_value(board,alpha,beta,limit):
    #returns [move,value] that maximizes score
    #v=-math.inf
    w=[None,alpha]
    # w[0] is move w[1] is value of utility

    # utilvalue via countn opvragen
    # if abs(value) == nr dan terminal, or limit <0

    utilvalue = utility(board)    
    # als er al een winnaar is dan terug, w[0] blijft None
    if abs(utilvalue) == nr or limit < 0:
        #now X or O has won, or limit reached
        return [w,utilvalue]
        
    #dummyboard=[[O, X, X, X, O, X, None], [None, X, O, X, X, O, None], [None, O, X, X, X, O, None], [None, O, O, O, X, X, None], [None, None, None, None, O, None, None], [None, None, None, None, None, None, None]]
    #thisutility = utility(dummyboard)
    #print("utility with dummyboard = " , thisutility)
    #assert thisutility == 3
    
    for action in actions(board):
        #see if this is a winning move for X
        tempresult = result(board,action)
        temputility = utility(tempresult)
        if temputility == nr:
            return [action, temputility]

        # if not a winning move, try further using minimax
        # here, figure out what min_value would do
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

    utilvalue = utility(board)
    if abs(utilvalue) == nr or limit < 0:
        # now X or O has won, or limit reached, return, w[0] is nog steeds None
        return [w,utility(board)]
       

    for action in actions(board):
        #see if this is a winning move for O
        tempresult = result(board,action)
        temputility = utility(tempresult)
        if temputility == -nr:
            return [action, temputility]
        
        # if not a winning move, try further using minimax
        # here, figure out what max_value would do        
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

def alln(board,aantal):

    # rows:
    for i in range(nrows):
        for j in range(ncolumns - nr + 1):
            gevonden = board[i][j] in [X,O]
            if gevonden:
                for k in range(aantal-1):
                    gevonden = gevonden and board[i][j+k] == board[i][j+k+1]
                if gevonden:
                    return board[i][j]

    #columns
    for j in range(ncolumns):
        for i in range(nrows - nr + 1):
            gevonden = board[i][j] in [X,O]
            if gevonden:
                for k in range(aantal-1):
                    gevonden = gevonden and board[i+k][j] == board[i+k+1][j]
                if gevonden:
                    return board[i][j]
    
    #diagonals upright:
    for i in range(nrows - nr + 1):
        for j in range(ncolumns - nr + 1): 
            gevonden = board[i][j] in [X,O]   
            if gevonden:
                for k in range(aantal-1):
                    gevonden = gevonden and board[i+k][j+k] == board[i+k+1][j+k+1]
                if gevonden:
                    return board[i][j]
    
    #diagonals upleft
    for i in range(nrows - nr + 1):
        for j in range(ncolumns - 1, ncolumns - nr - 1, -1):
            gevonden = board[i][j] in [X,O] 
            if gevonden:
                for k in range(aantal-1):
                    gevonden = gevonden and board[i+k][j-k] == board[i+k+1][j-k-1]
                if gevonden:
                    return board[i][j]

    # if nothing found yet, no aantal in a row
    return False
            

def bordvol(board):
    for i in range(nrows):
        for j in range(ncolumns):
            if board[i][j]is EMPTY:
                return False
    return True
