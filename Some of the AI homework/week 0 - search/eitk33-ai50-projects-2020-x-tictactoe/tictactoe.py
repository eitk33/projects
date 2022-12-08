"""
Tic Tac Toe Player
"""
import copy
import math
import sys

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
    # EK
    countero = 0
    counterx = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == X:
                counterx += 1
            elif board[i][j] == O:
                countero += 1
            else:
                pass
    if counterx > countero:
        return O
    else:
        return X


def actions(board):
    # EK
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == None:
                actions_set.add((i, j))
    return actions_set


def result(board, action):
    # EK
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)

    if is_valid(action) != True:
        raise TypeError('Not a valid action')
    elif board_copy[action[0]][action[1]] != None:
        raise ValueError('cell taken')
    board_copy[action[0]][action[1]] = player(board)
    return board_copy

    raise NotImplementedError


def is_valid(a):
    # EK
    if not a:
        print('not a')
        return True
    if type(a) != tuple:
        print('not tuple')
        return True
    if len(a) != 2:
        print('not len')
        return True
    if type(a[0]) != int or type(a[1]) != int:
        return True
    return True


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # EK
    counter = 0
    a = list(map(list, zip(*board)))
    diag1 = [board[i][i] for i in range(len(board))]
    diag2 = [board[i][len(board[0]) - i - 1] for i in range(len(board))]
    for i in range(len(board)):
        if iswin(board[i]):
            return iswin(board[i])
        elif iswin(a[i]):
            return iswin(a[i])
    if iswin(diag1):
        return iswin(diag1[0])
    elif iswin(diag2):
        return iswin(diag2[0])
    return None


def iswin(l):
    # EK
    if l[0] and len(set(l)) == 1:
        return l[0]
    else:
        return None
    raise NotImplementedError


def terminal(board):
    # EK
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    else:
        for i in range(len(board)):
            for j in range(len(board)):
                if not board[i][j]:
                    return False
        return True
    raise NotImplementedError


def utility(board):
    # EK
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    a = winner(board)
    utility = int
    if a:
        if a == 'X':
            utility = 1
        elif a == 'O':
            utility = -1
    else:
        utility = 0
    return utility
    raise NotImplementedError


def minimax(board):
    # EK
    """
    Returns the optimal action for the current player on the board.
    """
    my_list = []
    if terminal(board):
        return None
    else:
        for action in actions(board):
            if player(board) == 'X':
                p = maxi(result(board, action))
                lim = -1
            elif player(board) == 'O':
                p = mini(result(board, action))
                lim = 1

            my_list.append((p, action))
    best_move = (None, None)
    counter = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if not board[i][j]:
                counter += 1
    for item in my_list:
        if player(board) == 'X' and item[0] >= lim:
            lim = item[0]
            best_move = item[1]
            if counter > 1:
                for action in actions(result(board, item[1])):
                    if utility(result(board, item[1])) == 1:
                        best_move = item[1]
                        break
                    elif utility(result(result(board, item[1]), action)) == -1:
                        best_move = action
                        break
        elif player(board) == 'O' and item[0] <= lim:
            lim = item[0]
            best_move = item[1]
            if counter > 1:
                for action in actions(result(board, item[1])):
                    if utility(result(board, item[1])) == -1:
                        best_move = item[1]
                        break
                    elif utility(result(result(board, item[1]), action)) == 1:
                        best_move = action
                        break

    return best_move


def maxi(b):
    # EK
    lim = -1
    # p = -1
    if terminal((b)):
        return (utility(b))
    for action in actions(b):
        p = max(lim, mini(result(b, action)))
    return p


def mini(b):
    #EK
    lim = 1
    #   p = 1
    if terminal((b)):
        return (utility(b))
    for action in actions(b):
        p = min(lim, maxi(result(b, action)))
    return p
