"""
Gomoku Player
"""
# import numpy as np
import math
from random import shuffle

X = 1 # White Player
O = -1 # Black Player
EMPTY = 0

def initial_state(size=15):
    """
    Returns starting state of the board.
    """
    # return np.array([[EMPTY]*size]*size)
    return [[EMPTY for _ in range(size)] for _ in range(size)]


def player_turn(board, last_player=None):
    """
    Returns player who has the next turn on a board.
    """
    if last_player == X or last_player == O:
        return X if last_player == O else O
    
    # return (O if np.sign(np.sum(board)) == X else X) if (board==EMPTY).any() else EMPTY

    _sum = 0 # sum of all elements in the board
    for row in board:
        _sum += sum(row)
    _sum_sign = int(math.copysign(1, _sum))

    any_empty = False
    for row in board:
        if EMPTY in row:
            any_empty = True
            break
    
    return (O if _sum_sign == X else X) if any_empty else EMPTY

def actions(board):
    """
    Returns set of all possible actions (i, j) on the board.
    """
    # return list(zip(*np.where(board == EMPTY)))
    board_len = len(board[0])
    return [(i, j) for i in range(board_len) for j in range(board_len) if board[i][j] == EMPTY]

def make_move(board, action, player=None):
    """
    Returns board after the move.
    """
    if player is None:
        player = player_turn(board)
    i, j = action
    # board[i, j] = player
    board[i][j] = player
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
    # board_len = board.shape[0]
    board_len = len(board[0])
    row, col = action
    
    if row < 0 or row >= board_len or col < 0 or col >= board_len: return 0
    # return board[row, col]
    return board[row][col]

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    dirs = ((1, -1), (1, 0), (1, 1), (0, 1))
    # board_len = board.shape[0]
    board_len = len(board[0])
    
    for i in range(board_len):
        for j in range(board_len):
            if board[i][j] == EMPTY: continue
            id = board[i][j]
            for d in dirs:
                x, y = i, j
                count = 0
                for _ in range(5):
                    if get(board, (x, y)) != id: break
                    y += d[0]
                    x += d[1]
                    count += 1
                # Exactly 5 in a row and no more than 5
                if count == 5 and get(board, (x+d[0], y+d[1])) != id:
                    return id
    return EMPTY

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # return winner(board) != EMPTY or not (board == EMPTY).any()
    any_empty = False
    for row in board:
        if EMPTY in row:
            any_empty = True
            break

    return winner(board) != EMPTY or not any_empty

def display_state(board):
    board_len = len(board[0])
    
    print(' '+' -'*board_len)
    
    print('  ' + ' '.join([chr(ord('A') + i) for i in range(board_len)]))

    for row in range(board_len):
        print(chr(ord('A') + row), end=' ')
        for col in range(board_len):
            ch = board[row][col]
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

# todo: make minimax converg faster
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    # find which pllayer's turn it is in the board
    turn = player_turn(board) == X
    # find the playable moves init dict to map value to optimised moves
    moves, v2action = actions(board), {}
    # shuffle for randomness
    shuffle(moves)

    minimum_score, maximum_score = -(board.shape[0]**2), board.shape[0]**2
    
    def alphabeta(b, alpha, beta, maximizingPlayer):
        """ min_/max_value function with alpha-beta pruning"""

        if terminal(b):
            return winner()(b)

        else:
            score, optimizer = (minimum_score, max) if maximizingPlayer else (maximum_score, min)

            possible_moves = actions(b)

            for move in possible_moves:
                child = result(board=b, action=move)

                score = optimizer(score, alphabeta(b=child, alpha=alpha, beta=beta, maximizingPlayer=not maximizingPlayer))

                if maximizingPlayer:
                    alpha = optimizer(alpha, score)
                else:
                    beta = optimizer(beta, score)

                if alpha >= beta:
                    break

            return score
    
    # picks action a in ACTIONS(s) that produces optimal value of MIN/MAX-VALUE(RESULT(s, a))
    for move in moves:
        possible_board = result(board=board, action=move)
        v2action[alphabeta(b=possible_board, maximizingPlayer=not turn, alpha=minimum_score, beta=maximum_score)] = move
    # choose our optimizer function (min or max) based on which player is playing
    optimizer = max if turn else min
    # return the optimised action from dict.
    return v2action[optimizer(v2action)]


#----------------------------------------------------------------------
# main game
#----------------------------------------------------------------------
def gamemain():
    board_size = 15
    board = initial_state(board_size)

    while 1:
        row = col = -1
        display_state(board)
        turn = player_turn(board)
        turn_chr = 'X' if turn == X else 'O'
        action = input('Enter your move (q/f:Quit/Forfeit): ').strip('\r\n\t ').lower()
        
        if action == 'f':
            print('player {} forfeits.'.format(turn_chr))
            print('player {} wins.'.format('O' if turn == X else 'X'))
            
            print("new game")
            board = initial_state(board_size)
            continue
        
        elif action == 'q':
            print('player {} quits.'.format(turn_chr))
            break

        elif len(action) == 2:
            tr = ord(action[0].upper()) - ord('A')
            tc = ord(action[1].upper()) - ord('A')
            if tr >= 0 and tc >= 0 and tr < board_size and tc < board_size:
                if board[tr][tc] == 0:
                    row, col = tr, tc
                else:
                    print( 'can not move there')
            else:
                print( 'bad position')
        
        elif action == 'h' or action == 'help':
            action = minimax(board)
            if action is not None:
                print('play: {}'.format(action))
            else:
                print('no moves left to play.')

        if row >= 0 and col >= 0:
            action = (row, col)
            board = make_move(board, action, turn)
        
        if terminal(board):
            victor = winner(board)
            if victor != EMPTY:
                print('player {} wins.'.format('O' if victor == X else 'X'))
            else:
                print('draw')
            
            print("new game")
            board = initial_state(board_size)
            continue

#----------------------------------------------------------------------
if __name__ == '__main__':
    gamemain()

