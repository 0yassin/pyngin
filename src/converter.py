piece_table = {
    "p":-1,
    "r":-4,
    "n":-2,
    "b":-3,
    "q":-5,
    "k":-6,

    "P":1,
    "R":4,
    "N":2,
    "B":3,
    "Q":5,
    "K":6,
}


def load_fen(fen:str, board):
    parts = fen.split(" ")
    ranks = parts[0].split("/")
    curr_square = 0
    for rank in ranks:
        for piece in rank:
            if piece in piece_table:
                board.state[curr_square] = piece_table.get(piece)
                curr_square+=1
            else:
                empty_squares = int(piece)
                for i in range(empty_squares):
                    board.state[curr_square] = 0
                    curr_square+=1


    board.turn = 'w' if parts[1] == 'w' else 'b'
    
    board.turn = parts[1]

    if "K" in parts[2]:
        board.castling_rights['wk'] = True
    if "Q" in parts[2]:
        board.castling_rights['wq'] = True


    if "k" in parts[2]:
        board.castling_rights['bk'] = True
    if "q" in parts[2]:
        board.castling_rights['bq'] = True
    
    if parts[3] != "-":
        file_char = parts[3][0].lower()
        rank_char = parts[3][1]
        col = ord(file_char) - ord('a')
        row = 8 - int(rank_char)
        board.en_passant_target = row * 8 + col
    else:
        board.en_passant_target = None

    board.move_n = int(parts[5])

