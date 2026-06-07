
from pieces import *

def evaluate_position(board):
    phase = 0
    mg_score = 0
    eg_score = 0
    for i in range(64):
        piece = board.state[i]
        if piece == 0:
            continue
        piece_color = 1 if piece > 0 else -1
        # material
        mg_score += PIECE_VALUES[abs(piece)] * piece_color
        eg_score += PIECE_VALUES[abs(piece)] * piece_color
        
        if abs(piece) == 2 or abs(piece) == 3:   phase += 1 
        elif abs(piece) == 4:                    phase += 2  
        elif abs(piece) == 5:                    phase += 4

        if abs(piece) == 1:
            if piece_color>0:
                mg_score += PST_PAWN[i] 
                eg_score += PST_PAWN[i] * PAWN_EG_BONUS
            else:
                black_i = ((7 - (i // 8)) * 8) + (i % 8)
                mg_score -= PST_PAWN[black_i]
                eg_score -= PST_PAWN[black_i] * PAWN_EG_BONUS

        elif abs(piece) == 2:
            mg_score += PST_KNIGHT[i] * piece_color
            eg_score += (PST_KNIGHT[i] * KNIGHT_EG_BONUS) * piece_color 

        elif abs(piece) == 3:
            sq = count_vision_squares(i, board, BISHOP_OFFSETS)
            b_score = sq * BISHOP_VISION_BONUS
            if piece>0:
                mg_score += b_score
                eg_score += b_score
            else:
                mg_score -= b_score
                eg_score -= b_score

        elif abs(piece) == 4:
            sq = count_vision_squares(i, board, ROOK_OFFSETS)
            b_score = sq * ROOK_VISION_BONUS
            if piece>0:
                mg_score += b_score
                eg_score += b_score
            else:
                mg_score -= b_score
                eg_score -= b_score

        elif abs(piece) == 5:
            sq = count_vision_squares(i, board, QUEEN_OFFSETS)
            b_score = sq * QUEEN_VISION_BONUS
            if piece>0:
                mg_score += b_score
                eg_score += b_score
            else:
                mg_score -= b_score
                eg_score -= b_score



        elif abs(piece) == 6:
            if piece>0:
                mg_score += PST_KING_MG[i] 
                eg_score += PST_KING_EG[i]
            else:
                black_i = ((7 - (i // 8)) * 8) + (i % 8)
                mg_score -= PST_KING_MG[black_i] 
                eg_score -= PST_KING_EG[black_i]

    phase = min(phase, 24)
    final_score = ((mg_score * phase) + (eg_score * (24 - phase))) // 24

    return final_score

def count_vision_squares(piece_index, board, offsets):
    count = 0
    for offset in offsets:
        tar_square = piece_index
        prev_col = piece_index % 8
        while True:
            tar_square += offset
            tar_col = tar_square % 8
            if tar_square > 63 or tar_square < 0:
                break
            elif offset in [-8, 8] and tar_col != prev_col:
                break  
            elif offset in [-9, -7, 9, 7, 1, -1] and abs(tar_col - prev_col) != 1:
                break
            count += 1
            if board.state[tar_square] != 0:
                break
            prev_col = tar_col

    return count

def get_relative_eval(board):
    eval = evaluate_position(board)
    return eval if board.turn == "w" else eval * -1