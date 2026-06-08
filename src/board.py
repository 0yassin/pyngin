from moves import translate_move
from chess import Move
from moves import get_legal_moves, get_psudo_moves

class Board:
    def __init__(self, state=None):
        if state is None:
            self.state:list[int] = [0]*64
        else:
            self.state = list(state)

        self.castling_rights = {
            'wk': True, 'wq': True,
            'bk': True, 'bq': True  
        }
        self.en_passant_target = None
        self.move_n = 1
        self.turn = 'w'
        self.game_state = "-"
        self.pgn_node = None

    def get_possible_moves(self):
        return get_legal_moves(self)
        
    def make_move(self,move, pgn_game = None):
        start, end = move
        piece_moving = self.state[start]

        next_ep_target = None

        if self.pgn_node is not None:
            chess_move = Move.from_uci(translate_move(move))
            self.pgn_node = self.pgn_node.add_main_variation(chess_move)

        if abs(piece_moving) == 6:
            if start == 60 and end == 62:
                self.state[61] = self.state[63] # Move Rook from h1 to f1
                self.state[63] = 0
            elif start == 60 and end == 58:
                self.state[59] = self.state[56]
                self.state[56] = 0

            elif start == 4 and end == 6:
                self.state[5] = self.state[7]
                self.state[7] = 0
            
            elif start == 4 and end == 2:
                self.state[3] = self.state[0]
                self.state[0] = 0

        if piece_moving == 6:
            self.castling_rights['wk'] = False
            self.castling_rights['wq'] = False
        if piece_moving == -6:
            self.castling_rights['bk'] = False
            self.castling_rights['bq'] = False

        if abs(piece_moving) == 4:
            if start == 63: self.castling_rights['wk'] = False
            if start == 56: self.castling_rights['wq'] = False
            if start == 7: self.castling_rights['bk'] = False
            if start == 0: self.castling_rights['bq'] = False

        if end == 63: self.castling_rights['wk'] = False
        if end == 56: self.castling_rights['wq'] = False
        if end == 7: self.castling_rights['bk'] = False
        if end == 0: self.castling_rights['bq'] = False

        if abs(piece_moving) == 1:
            start_row = start // 8
            end_row = end // 8
            if abs(end_row - start_row) == 2:
                next_ep_target = (start + end) // 2
  

        if abs(piece_moving) == 1 and end == self.en_passant_target:
            victim_square = end + 8 if piece_moving > 0 else end - 8
            self.state[victim_square] = 0

        if abs(piece_moving) == 1:
            if end // 8 == 0 or end // 8 == 7:
                color_sign = 1 if piece_moving > 0 else -1
                self.state[end] = 5 * color_sign
            else:
                self.state[end] = piece_moving
        else:
            self.state[end] = piece_moving

        if pgn_game != None:
            pgn_game.add_main_variation(Move.from_uci(translate_move(move)))


        self.state[start] = 0

        self.en_passant_target = next_ep_target
        self.move_n += 1 if self.turn == "b" else 0
        self.turn = "b" if self.turn == "w" else "w"

    def clone(self):
        new_board = Board()
        new_board.state = list(self.state)
        new_board.castling_rights = dict(self.castling_rights)
        new_board.en_passant_target = self.en_passant_target
        new_board.move_n = self.move_n
        new_board.turn = self.turn
        return new_board

    def is_in_check(self):
        king_p = 6 if self.turn == 'w' else -6
        king_sq = -1

        for i in range(64):
            if self.state[i] == king_p:
                king_sq = i
            else:
                continue
        if king_sq == -1: return False

        og_turn = self.turn
        self.turn = 'b' if og_turn == 'w' else 'w'
        opp_moves = get_psudo_moves(self)
        self.turn = og_turn

        for move in opp_moves:
            start, end = move
            if end == king_sq:
                return True
        return False