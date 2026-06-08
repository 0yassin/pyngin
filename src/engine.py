from moves import get_legal_moves, get_move_score
from evaluate import get_relative_eval

def get_engine_move(board, d):
    best_move = None
    best_score = -float('inf')
    alpha, beta = -float('inf'), float('inf')
    legal_moves = get_legal_moves(board)
    if not legal_moves:
        return None

    legal_moves.sort(key=lambda m:get_move_score(m, board), reverse=True)
    
    for move in legal_moves:
        temp_board = board.clone()
        temp_board.make_move(move)

        score = -negamax(temp_board, d - 1, -beta, -alpha, ply=1)

        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, score)
    return best_move

def negamax(board, d, alpha, beta, ply=0):
    if d==0: return get_relative_eval(board)
    legal_moves = get_legal_moves(board)
    if len(legal_moves) == 0:
        if board.is_in_check():
            return -999999 + ply
        else:
            return 0
    legal_moves.sort(key=lambda m:get_move_score(m, board), reverse=True)
    max_eval = -float('inf')
    for move in legal_moves:
        temp_board = board.clone()
        temp_board.make_move(move)
        evaluation = -negamax(temp_board, d - 1, -beta, -alpha, ply + 1)

        max_eval = max(max_eval, evaluation)
        alpha = max(alpha, evaluation)

        if alpha >= beta:
            break
    return max_eval

