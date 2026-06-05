

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


def get_psudo_moves(board):
    p_moves = []
    for i in range(64):
        piece = board.state[i]
        if is_current_turn_piece(piece, board.turn):
            if abs(piece) == 2:
                p_moves.extend(get_knight_moves(board, i))
    return p_moves



def is_current_turn_piece(piece, turn):
    # piece > 0 means white
    if piece > 0 and turn == "w":
        return True
    elif piece < 0 and turn == "b":
        return True
    else:
        return False


