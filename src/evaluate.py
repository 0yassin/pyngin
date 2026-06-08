from pieces import *
from moves import count_vision_squares

def evaluate_position(board):
    phase = 0
    mg_score = 0
    eg_score = 0
    for i in range(64):
        piece = board.state[i]
        if piece == 0:
            continue
        piece_color = 1 if piece > 0 else -1
        pst_index = i if piece_color>0 else (i ^ 56)
        # material
        mg_score += PIECE_VALUES[abs(piece)] * piece_color
        eg_score += PIECE_VALUES[abs(piece)] * piece_color
        
        if abs(piece) == 2 or abs(piece) == 3:   phase += 1 
        elif abs(piece) == 4:                    phase += 2  
        elif abs(piece) == 5:                    phase += 4

        if abs(piece) == 1:
            mg_score += PST_PAWN[pst_index] * piece_color
            eg_score += (PST_PAWN[pst_index] * PAWN_EG_BONUS) * piece_color

        elif abs(piece) == 2:
            mg_score += PST_KNIGHT[pst_index] * piece_color
            eg_score += (PST_KNIGHT[pst_index] * KNIGHT_EG_BONUS) * piece_color 

        elif abs(piece) == 3:
            sq = count_vision_squares(i, board, BISHOP_OFFSETS)
            PST_score = PST_BISHOP[pst_index]
            b_score = (sq * BISHOP_VISION_BONUS) + PST_score
            mg_score += b_score * piece_color
            eg_score += b_score * piece_color

        elif abs(piece) == 4:
            sq = count_vision_squares(i, board, ROOK_OFFSETS)
            PST_score = PST_ROOK[pst_index]
            b_score = (sq * ROOK_VISION_BONUS) + PST_score
            mg_score += b_score * piece_color
            eg_score += b_score * piece_color

        elif abs(piece) == 5:
            sq = count_vision_squares(i, board, QUEEN_OFFSETS)
            PST_score = PST_QUEEN[pst_index]
            b_score = (sq * QUEEN_VISION_BONUS) + PST_score
            mg_score += b_score * piece_color
            eg_score += b_score * piece_color

        elif abs(piece) == 6:
            mg_score += PST_KING_MG[pst_index] * piece_color
            eg_score += PST_KING_EG[pst_index] * piece_color

    phase = min(phase, 24)
    final_score = ((mg_score * phase) + (eg_score * (24 - phase))) // 24
    return int(final_score)

def get_relative_eval(board):
    eval = evaluate_position(board)
    return eval if board.turn == "w" else eval * -1