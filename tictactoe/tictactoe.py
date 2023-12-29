"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """    
    count_empty = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                count_empty += 1
    
    if count_empty % 2 == 0:
        return O
    else:
        return X

    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_moves.add((i,j))

    return possible_moves
    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # create deep copy of board
    board_copy = copy.deepcopy(board)

    if board_copy[action[0]][action[1]] != EMPTY:
        raise Exception
    else:
        board_copy[action[0]][action[1]] = player(board_copy)
    
    return board_copy

    # raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        # three in a row are the same
        if board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        # three in a column are the same
        elif board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]
    
    # diagonals
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    
    return None
    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # check for winner
    if not winner(board) == None:
        return True
    
    # check if there is an EMPTY entry left
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    
    # no winner and no EMPTY entry left -> tie
    return True

    # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

    # raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):        
        return None
    
    list_moves = []
    if player(board) == X:
        #if board == [[EMPTY, EMPTY, EMPTY],
        #    [EMPTY, EMPTY, EMPTY],
        #    [EMPTY, EMPTY, EMPTY]]:
        #    return (1,1)
        
        for action in actions(board):
            list_moves.append([min_value(result(board,action)),action])
        
        v = - math.inf
        for move in list_moves:
            if move[0] > v:
                v = move[0]
                optimal_action = move[1]
        
            #return optimal_action
        
    if player(board) == O:
        for action in actions(board):
            list_moves.append([max_value(result(board,action)),action])
        
        v = math.inf
        for move in list_moves:
            if move[0] < v:
                v = move[0]
                optimal_action = move[1]
        
            #return optimal_action
    
    print(optimal_action)
    return optimal_action

    
    # raise NotImplementedError

def max_value(board):
    if terminal(board):
        return(utility(board))

    v = -math.inf

    for action in actions(board):
        v = max(v, min_value(result(board,action)))
    
    return v

def min_value(board):
    if terminal(board):
        return(utility(board))

    v = math.inf

    for action in actions(board):
        v = min(v, max_value(result(board,action)))
    
    return v