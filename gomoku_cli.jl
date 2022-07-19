using LinearAlgebra, Random, StaticArrays

is_empty = iszero
const X = 1 # White Player
const O = -1 # Black Player
const EMPTY = 0


"""
Returns starting state of the board.
"""
initial_state(size=15) = repeat([EMPTY], size, size)

"""
Returns player who has the next turn on a board.
"""
player_turn(board) = any(is_empty, board) ? ((sign∘sum)(board) == X ? O : X) : EMPTY

"""
Returns set of all possible actions (i, j) on the board.
"""
actions(board) = findall(is_empty, board)

"""
Returns board after the move.
"""
make_move!(board, action::CartesianIndex{2}, player=player_turn(board)) = (all(i->0<i<=size(board, 1), action.I)) && (board[action] = player)
make_move!(board, action, player=player_turn(board)) = make_move!(board, CartesianIndex(action...), player)

"""
Returns the board that results from making move (i, j) on the board.
"""
result(board, action::CartesianIndex{2}) = (new_board = copy(board); make_move!(new_board, action); return new_board)
result(board, action) = result(board, CartesianIndex(clamp.(action, 1, size(board, 1))...))
result(board, i::T, j::T) where T <: Integer = result(board, CartesianIndex(clamp(i, 1, size(board, 1))), CartesianIndex(clamp(j, 1, size(board, 1))))

"""
Returns the value of board at action.
"""
get(board, action::CartesianIndex{2}) = board[action]
get(board, action) = all(i->0<i<=size(board, 1), action) ? get(board, CartesianIndex(action)) : EMPTY
get(board, i::T, j::T) where T <: Integer = get(board, (i, j))

"""
Returns the winner of the game, if there is one.
"""
function winner(board)
    dirs = ((1, -1), (1, 0), (1, 1), (0, 1))
    # board_len = board.shape[0]
    board_len = size(board, 1)
    
    for i in 1:board_len, j in 1:board_len
        is_empty(board[i, j]) && continue
        id = board[i, j]
        winning_moves = min(5, size(board, 1))
        for d in dirs
            x, y = i, j
            count = 0
            while get(board, (x, y)) == id
                (count > winning_moves || get(board, (x, y)) != id) && break
                x += d[1]
                y += d[2]
                count += 1
            end
            
            # Exactly 5 in a row and no more than 5
            (count == winning_moves && get(board, i+winning_moves*d[1], j+winning_moves*d[2]) != id && get(board, i-d[1], j-d[2]) != id) &&
                (return id)
        end
    end
    
    EMPTY
end

"""
Returns True if game is over, False otherwise.
"""
terminal(board) = winner(board) != EMPTY || EMPTY ∉ board

function display_state(board)
    board_len = size(board, 1)
    
    println(" "*" -"^board_len)
    println("  "*join('A' .+ (0:board_len-1), ' '))

    for row in 1:board_len
        print(('A' + row-1) * ' ')
        println(join(ch == EMPTY ? "∘ " : ch == X ? "X " : "O " for ch ∈ board[row, :]))
    end

    if terminal(board)
        victor = winner(board)
        if victor != EMPTY
            println("""player $(victor == X ? 'X' : 'O') wins.""")
        else
            println("draw")
        end
    else
        turn = player_turn(board) == X ? 'X' : 'O'
        println("Player $turn's turn")
    end
end


"""
# TODO
makes minimax converge faster by:
1: make a 6 x 6 filter kernel and apply that filter to game board and perform these filter operations,
2: rotate the filter(by 90°) 4 times and store those 4 filter configurations.
3: convolve through the board parallelly(not sequentially) using all 4 filters.
4: if any of the 4 filter matches the board subset during convolution, then
5: apply minimax to find winning move(location) on the filtered subset of the board
6: rotate the move/location according to filter configuration."
7: calculate and assign (TODO: some kind of score) to the move to find the optimal(max/min) scoring move from the (board_size x board_size)moves obtained after entire convolvolution.
8: return the optimal(minimum/maximum) move
"""
function ai_move(board)
    nothing
end


struct AI_Knowledge 
    board::Matrix{Int8}
    action::CartesianIndex{2}
    player::Int8
    actions::Vector{CartesianIndex{2}}
    symmetricity::SMatrix
    board_size::UInt8
end

"""
Returns the optimal action for the current player on the board.
"""
function minimax(board; default_return_move=CartesianIndex(-1, -1))
  terminal(board) && (return default_return_move)
  # find which pllayer's turn it is in the board
  turn = player_turn(board)
  # find the playable moves
  possible_moves = actions(board)
  # shuffle for randomness
  shuffle!(possible_moves)
  # an object to map value to optimised moves
  value_to_move = Vector{Tuple{Int8, CartesianIndex{2}}}(undef, length(possible_moves))
  # picks action a in ACTIONS(s) that produces optimal value of MIN/MAX-VALUE(RESULT(s, a))
  for (i, move) in enumerate(possible_moves)
    possible_board = result(board, move)
    score = alphabeta(possible_board, MINIMUM_SCORE, MAXIMUM_SCORE, turn != X)
    value_to_move[i] = (score, move)
  end
  # choose our optimizer function (min or max) based on which player is playing
  optimizer = turn == X ? argmax : argmin
  # return the optimised action from dict.values
  optimal_value, optimal_move = optimizer(x->x[1], value_to_move)
  optimal_move
end

const MINIMUM_SCORE = Int8(-100)
const MAXIMUM_SCORE = Int8(100)
""" min_/max_value function with alpha-beta pruning"""
function alphabeta(board, α, β, maximizingPlayer)
  terminal(board) && (return winner(board))

  score, optimizer = maximizingPlayer ? (MINIMUM_SCORE, max) : (MAXIMUM_SCORE, min)
  
  possible_moves = actions(board)

  for move in possible_moves
    child = result(board, move)
    
    score = optimizer(score, alphabeta(child, α, β, !maximizingPlayer))

    if maximizingPlayer
      α = optimizer(α, score)
    else
      β = optimizer(β, score)
    end
    
    α >= β && break
  end
  
  score
end

#----------------------------------------------------------------------
# main game
#----------------------------------------------------------------------
function gamemain(board_size=15)
    board = initial_state(board_size)

    while true
        row = col = -1
        display_state(board)
        turn = player_turn(board)
        turn_chr = turn == X ? 'X' : 'O'
        print("Enter your move (q/f:Quit/Forfeit): ")
        action = (lowercase∘strip∘readline)()
        
        if length(action) != 2 && action[1] == 'f'
            println("player $turn_chr forfeits.")
            println("player $(turn == X ? 'O' : 'X') wins.")
            
            println("new game")
            board = initial_state(board_size)
            continue
        
        elseif length(action) != 2 && action[1] == 'q'
            println("player $turn_chr quits.")
            break

        elseif length(action) == 2
            tr = action[1] - 'a' + 1
            tc = action[2] - 'a' + 1
            if tr > 0 && tc > 0 && tr <= board_size && tc <= board_size
                if board[tr, tc] == EMPTY
                    row, col = tr, tc
                else
                    println("can not move there")
                end
            else
                println("bad position")
            end
        
        elseif length(action) != 2 && action[1] == 'h'
            ai_action = minimax(board).I
            if !ismissing(ai_action)
                x, y = (ai_action[1] + 'a' - 1), (ai_action[2] + 'a' - 1)
                println("play: $((x, y))")
            else
                println("no moves left to play.")
            end
        end

        (row > 0 && col > 0 && row <= board_size && col <= board_size) && make_move!(board, (row, col), turn)
        
        if terminal(board)
            victor = winner(board)
            victor != EMPTY ? println("player $(victor == X ? 'X' : 'O') wins.") : println("draw")
            
            println("new game")
            board = initial_state(board_size)
            continue
        end
    end
end