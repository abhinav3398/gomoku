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

#----------------------------------------------------------------------
# main game
#----------------------------------------------------------------------
def gamemain():
    board_size = 15
    board = initial_state(board_size)

#----------------------------------------------------------------------
if __name__ == '__main__':
    gamemain()

