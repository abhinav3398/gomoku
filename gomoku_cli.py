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

def get(board, action):
    """
    Returns the value of board at action.
    """
    board_len = board.shape[0]
    row, col = action
    
    if row < 0 or row >= board_len or col < 0 or col >= board_len: return 0
    return board[row, col]

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    dirs = ((1, -1), (1, 0), (1, 1), (0, 1))
    board_len = board.shape[0]
    
    for i in range(board_len):
        for j in range(board_len):
            if board[i, j] == EMPTY: continue
            id = board[i, j]
            for d in dirs:
                x, y = i, j
                count = 0
                for _ in range(5):
                    if get(board, (i, j)) != id: break
                    y += d[0]
                    x += d[1]
                    count += 1
                # Exactly 5 in a row and no more than 5
                if count == 5 and get(board, (i, j)) != id:
                    return id
    return EMPTY

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) != EMPTY or not (board == EMPTY).any()

def display_state(board):
    print(' '+' -'*board.shape[0])
    
    board_len = board.shape[0]
    print('  ' + ' '.join([chr(ord('A') + i) for i in range(board_len)]))

    for row in range(board_len):
        print(chr(ord('A') + row), end=' ')
        for col in range(board_len):
            ch = board[row, col]
            if ch == EMPTY: 
                print('.', end=' ')
            elif ch == X:
                print( 'X', end=' ')
            elif ch == O:
                print( 'O', end=' ')
        print()

    if terminal(board):
        victor = winner(board)
        if victor != EMPTY:
            print('player {} wins.'.format('O' if victor == X else 'X'))
        else:
            print('draw')
    else:
        turn = 'X' if player_turn(board) == X else 'O'
        print('Player {}\'s turn'.format(turn))

#----------------------------------------------------------------------
# main game
#----------------------------------------------------------------------
def gamemain():
    board_size = 15
    board = initial_state(board_size)

#----------------------------------------------------------------------
if __name__ == '__main__':
    gamemain()

