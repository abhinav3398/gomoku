"""
Gomoku Player
"""
import numpy as np

X = 1 # White Player
O = -1 # Black Player
EMPTY = 0

def initial_state(size=15):
    """
    Returns starting state of the board.
    """
    return np.array([[EMPTY]*size]*size)


def player_turn(board, last_player=None):
    """
    Returns player who has the next turn on a board.
    """
    if last_player == X or last_player == O:
        return X if last_player == O else O
    
    return (O if np.sign(np.sum(board)) == X else X) if (board==EMPTY).any() else EMPTY

def actions(board):
    """
    Returns set of all possible actions (i, j) on the board.
    """
    return list(zip(*np.where(board == EMPTY)))

def make_move(board, action, player=None):
    """
    Returns board after the move.
    """
    if player is None:
        player = player_turn(board)
    i, j = action
    board[i, j] = player
    return board

def result(board, action, player=None):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if player is None:
        player = player_turn(board)
    return make_move(board.copy(), action, player)

#----------------------------------------------------------------------
# main game
#----------------------------------------------------------------------
def gamemain():
    board_size = 15
    board = initial_state(board_size)

#----------------------------------------------------------------------
if __name__ == '__main__':
    gamemain()

