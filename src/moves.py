from pieces import *

def get_move_score(move, board):
    start, end = move
    moving_piece = abs(board.state[start])
    victim_piece = abs(board.state[end])
    score = 0
    if victim_piece != 0:
        score = (9999) + (victim_piece * 10) - moving_piece
        return score
    if moving_piece == 1:
        if end // 8 == 0 or end // 8 == 7:
            score += 9999
    piece_color = 1 if board.state[start] > 0 else -1
    pst_index = end if piece_color > 0 else (end ^ 56)
    if moving_piece == 1:
        score += PST_PAWN[pst_index] * 2
    elif moving_piece == 2:
        score += PST_KNIGHT[pst_index] * 2
    elif moving_piece == 3:
        score += PST_BISHOP[pst_index] * 2
    elif moving_piece == 4:
        score += PST_ROOK[pst_index] * 2
    elif moving_piece == 5:
        score += PST_QUEEN[pst_index] * 2

    # TODO: add king move bonuses

    return score


def get_knight_moves(board, index):
    res = []
    offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
    turn = 'w' if board.state[index] > 0 else 'b'
    for offset in offsets: 
        tar_square = index + offset
        if tar_square > 63 or tar_square < 0:
            pass
        elif abs(tar_square % 8 - index % 8) != 1 and abs(tar_square % 8 - index % 8) !=2:
            pass
        elif is_current_turn_piece(board.state[tar_square], turn):
            pass
        else:
            res.append((index, tar_square))
    return res
def get_bishop_moves(board, index):
    res = []
    offsets = [-9, -7, 9, 7]
    start_col = index % 8
    for offset in offsets:
        tar_square =  index
        prev_col = start_col
        while True:
            tar_square+=offset
            if tar_square > 63 or tar_square < 0:
                break
            target_col = tar_square % 8
            
            if abs(target_col - prev_col) != 1:
                break
            prev_col = target_col
            turn = 'w' if board.state[index] > 0 else 'b'
            if board.state[tar_square] == 0:
                res.append((index, tar_square))
            elif is_current_turn_piece(board.state[tar_square], turn):
                break
            else:
                res.append((index, tar_square))
                break
    return res
def get_rook_moves(board, index):
    res = []
    offsets = [-8, 8, -1, 1]
    start_col = index % 8
    for offset in offsets:
        tar_square = index
        prev_col = start_col
        while True:
            tar_square+=offset
            if tar_square > 63 or tar_square < 0:
                break
            tar_col = tar_square % 8
            if offset in [1, -1] and abs(tar_col - prev_col) != 1:
                break
            if offset in [-8, 8] and tar_col != prev_col:
                break  
            prev_col = tar_col
            turn = 'w' if board.state[index] > 0 else 'b'
            if board.state[tar_square] == 0:
                res.append((index, tar_square))
            elif is_current_turn_piece(board.state[tar_square], turn):
                break
            else:
                res.append((index, tar_square))
                break
    return res

def get_pawn_moves(board, index):
    res = []
    offsets = [-8] if board.state[index]>0 else [8]
    capt_offsets = [-7, -9] if board.state[index]>0 else [7, 9]
    row = index // 8
    if row == 1 and board.state[index]<0:
        offsets.append(16)
    if row == 6 and board.state[index]>0:
        offsets.append(-16)
    for offset in offsets:
        tar_square = index + offset
        if tar_square > 63 or tar_square<0:
            break
        if index % 8 != tar_square % 8:
            break
        if board.state[tar_square] != 0:
            break
        res.append((index, tar_square))
    for offset in capt_offsets:
        tar_square = index + offset
        if tar_square > 63 or tar_square<0:
            continue
        if abs((tar_square % 8) - (index % 8)) != 1:
            continue

        turn = 'w' if board.state[index] > 0 else 'b'
        if board.state[tar_square] == 0 :
            if board.en_passant_target is not None and tar_square == board.en_passant_target:
                res.append((index, tar_square))
            continue
        if is_current_turn_piece(board.state[tar_square], turn):
            continue
        res.append((index, tar_square))
    return res

def get_queen_moves(board, index):
    res = []
    offsets = [-8, 8, -1, 1,-9, -7, 9, 7]
    for offset in offsets:
        tar_square = index
        prev_col = index % 8
        while True:
            tar_square+=offset
            tar_col = tar_square % 8
            if tar_square > 63 or tar_square < 0:
                break
            if offset in [-8, 8] and tar_col != prev_col:
                break  
            if offset in [-9, -7, 9, 7, 1, -1] and abs(tar_col - prev_col) != 1:
                break
            prev_col = tar_col
            turn = 'w' if board.state[index] > 0 else 'b'
            if board.state[tar_square] == 0:
                res.append((index, tar_square))
            elif is_current_turn_piece(board.state[tar_square], turn):
                break
            else:
                res.append((index, tar_square))
                break
    return res

def get_king_moves(board, index):
    offsets = [-8, 8, -1, 1,-9, -7, 9, 7]
    res = []
    if board.turn == "w" and index == 60:
        if board.castling_rights['wk'] and board.state[61] == 0 and board.state[62] == 0:
            res.append((60, 62))
        if board.castling_rights['wq'] and board.state[59] == 0 and board.state[58] == 0 and board.state[57] == 0:
            res.append((60, 58))

    if board.turn == "b" and index == 4:
        if board.castling_rights['bk'] and board.state[5] == 0 and board.state[6] == 0:
            res.append((4, 6))
        if board.castling_rights['bq'] and board.state[3] == 0 and board.state[2] == 0 and board.state[1] == 0:
            res.append((4, 2))
    start_col = index % 8
    for offset in offsets:
        tar_square = index + offset
        turn = 'w' if board.state[index] > 0 else 'b'
        if tar_square>63 or tar_square<0:
            continue
        tar_col = tar_square % 8
        if offset in [-8, 8] and tar_col != start_col:
            continue  
        if offset in [-9, -7, 9, 7, 1, -1] and abs(tar_col - start_col) != 1:
            continue
        if is_current_turn_piece(board.state[tar_square], turn):
            continue
        prev_col = tar_col
        res.append((index, tar_square))
    return res

def get_psudo_moves(board):
    p_moves = []
    for i in range(64):
        piece = board.state[i]
        if is_current_turn_piece(piece, board.turn):
            if abs(piece) == 1:
                p_moves.extend(get_pawn_moves(board, i))
            if abs(piece) == 2:
                p_moves.extend(get_knight_moves(board, i))
            if abs(piece) == 3:
                p_moves.extend(get_bishop_moves(board, i))
            if abs(piece) == 4:
                p_moves.extend(get_rook_moves(board, i))
            if abs(piece) == 5:
                p_moves.extend(get_queen_moves(board, i))
            if abs(piece) == 6:
                p_moves.extend(get_king_moves(board, i))
    return p_moves

def get_legal_moves(board):
    legal_moves = []
    pseudo_moves = get_psudo_moves(board)
    king_index = board.bk_index if board.turn == "b" else board.wk_index
    opponent_color = 'b' if board.turn == 'w' else 'w'
    ep_captured_piece = 0

    for move in pseudo_moves:
        start, end = move
        piece_moving = board.state[start]
        captured_piece = board.state[end]
        is_castling_move = (abs(piece_moving) == 6 and abs(start - end) == 2)
        is_king_moving = (abs(piece_moving) == 6)

        board.state[end] = piece_moving
        board.state[start] = 0

        ep_victim_square = None
        if abs(piece_moving) == 1 and (start % 8 != end % 8) and captured_piece == 0:
            ep_victim_square = end + 8 if piece_moving > 0 else end - 8
            ep_captured_piece = board.state[ep_victim_square]
            board.state[ep_victim_square] = 0
        temp_king_idx = end if is_king_moving else king_index
        king_is_safe = not is_square_attacked(temp_king_idx, board, opponent_color)
        if king_is_safe and is_castling_move:
            transit_square = (start + end) // 2
            if is_square_attacked(start, board, opponent_color) or \
               is_square_attacked(transit_square, board, opponent_color):
                king_is_safe = False
        if king_is_safe:
            legal_moves.append(move)

        board.state[start] = piece_moving
        board.state[end] = captured_piece
        if ep_victim_square is not None:
            board.state[ep_victim_square] = ep_captured_piece

    return legal_moves

def is_square_attacked(square, board, opp_color):
    start_row = square // 8
    start_col = square % 8
    is_opp_white = (opp_color == "w")

    kn_deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    target_knight = 2 if is_opp_white else -2
    
    for dr, dc in kn_deltas:
        r, c = start_row + dr, start_col + dc
        if 0 <= r < 8 and 0 <= c < 8: 
            if board.state[r * 8 + c] == target_knight:
                return True

    target_pawn = 1 if is_opp_white else -1
    p_row_delta = 1 if is_opp_white else -1
    
    for p_col_delta in [-1, 1]:
        r, c = start_row + p_row_delta, start_col + p_col_delta
        if 0 <= r < 8 and 0 <= c < 8:
            if board.state[r * 8 + c] == target_pawn:
                return True

    ortho_deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    target_orthos = [4, 5] if is_opp_white else [-4, -5]
    
    for dr, dc in ortho_deltas:
        r, c = start_row + dr, start_col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            piece = board.state[r * 8 + c]
            if piece != 0:
                if piece in target_orthos:
                    return True
                break  
            r += dr
            c += dc

    diag_deltas = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    target_diags = [3, 5] if is_opp_white else [-3, -5]
    
    for dr, dc in diag_deltas:
        r, c = start_row + dr, start_col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            piece = board.state[r * 8 + c]
            if piece != 0:
                if piece in target_diags:
                    return True
                break  # Ray is blocked
            r += dr
            c += dc
    target_king = 6 if is_opp_white else -6
    king_deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in king_deltas:
        r, c = start_row + dr, start_col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            if board.state[r * 8 + c] == target_king:
                return True
    return False

def is_current_turn_piece(piece, turn):
    # piece > 0 means white
    if piece > 0 and turn == "w":
        return True
    elif piece < 0 and turn == "b":
        return True
    else:
        return False

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


def translate_move(move):
    st_row = move[0] // 8
    end_row = move[1] // 8
    st_col = move[0] % 8
    end_col = move[1] % 8

    st_file = chr(ord('a') + st_col)
    st_rank = str(8 - st_row)
    end_file = chr(ord('a') + end_col)
    end_rank = str(8 - end_row)

    return st_file + st_rank + end_file + end_rank