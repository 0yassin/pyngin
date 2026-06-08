from pieces import *

def get_move_score(board, move):
    start, end = move
    moving_piece = abs(board.state[start])
    victim_piece = abs(board.state[end])
    if victim_piece != 0:
        score = (9999) + (victim_piece * 10) - moving_piece
        return score
    if moving_piece == 1:
        if end // 8 == 0 or end // 8 == 7:
            score = 9999
            return score
        else:
            score = PST_PAWN[end]*2 if PST_PAWN[end] > 0 else 0
            return score
    score = 0
    if moving_piece == 2:
        score += PST_KNIGHT[end] * 2 if PST_KNIGHT[end]>0 else 0
        return score
    elif moving_piece == 3:
        score += PST_BISHOP[end] * 2 if PST_BISHOP[end]>0 else 0
        return score
    elif moving_piece == 4:
        score += PST_ROOK[end] * 2 if PST_ROOK[end]>0 else 0
        return score
    elif moving_piece == 5:
        score += PST_QUEEN[end] * 2 if PST_QUEEN[end] >0 else 0
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
    psuedo_moves = get_psudo_moves(board)
    curent_turn = board.turn
    opponent_turn = 'b' if board.turn == 'w' else 'w'

    for move in psuedo_moves:
        start, end = move
        temp_state = list(board.state)
        piece_moving = board.state[start]
        is_castling_move = (abs(piece_moving) == 6 and abs(start - end) == 2)

        board.state[end] = board.state[start]
        board.state[start] = 0

        if abs(piece_moving) == 1 and (start % 8 != end % 8) and temp_state[end] == 0:
            victim_square = end + 8 if piece_moving > 0 else end - 8
            board.state[victim_square] = 0

        board.turn = opponent_turn

        king_value = 6 if curent_turn == "w" else -6
        king_index = board.state.index(king_value)
        enemy_responses = get_psudo_moves(board)
        king_is_safe = True
        for enemy_move in enemy_responses:
            enemy_start, enemy_end = enemy_move
            if enemy_end == king_index:
                king_is_safe = False
                break
            if is_castling_move:
                transit_square = (start + end) // 2
                if enemy_end == start or enemy_end == transit_square:
                    king_is_safe = False
                    break

        if king_is_safe:
            legal_moves.append(move)

        board.state = temp_state
        board.turn = curent_turn
    return legal_moves

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
