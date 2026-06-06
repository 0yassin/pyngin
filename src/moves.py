

def get_knight_moves(board, index):
    res = []
    offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
    for offset in offsets: 
        tar_square = index + offset
        if tar_square > 63 or tar_square < 0:
            pass
        elif abs(tar_square % 8 - index % 8) != 1 and abs(tar_square % 8 - index % 8) !=2:
            pass

        elif is_current_turn_piece(board.state[tar_square], board.turn):
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

            if board.state[tar_square] == 0:
                res.append((index, tar_square))
            elif is_current_turn_piece(board.state[tar_square], board.turn):
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

            if board.state[tar_square] == 0:
                res.append((index, tar_square))
            elif is_current_turn_piece(board.state[tar_square], board.turn):
                break
            else:
                res.append((index, tar_square))
                break
    return res




def get_psudo_moves(board):
    p_moves = []
    for i in range(64):
        piece = board.state[i]
        if is_current_turn_piece(piece, board.turn):
            if abs(piece) == 2:
                p_moves.extend(get_knight_moves(board, i))
            if abs(piece) == 3:
                p_moves.extend(get_bishop_moves(board, i))
            if abs(piece) == 4:
                p_moves.extend(get_rook_moves(board, i))
    return p_moves



def is_current_turn_piece(piece, turn):
    # piece > 0 means white
    if piece > 0 and turn == "w":
        return True
    elif piece < 0 and turn == "b":
        return True
    else:
        return False


