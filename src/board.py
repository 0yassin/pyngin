from moves import get_legal_moves
import moves
from moves import get_psudo_moves

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


    # TO BE CHANGED
    def get_possible_moves(self):
        return get_legal_moves(self)
        

    def make_move(self,move):
        print(f"made move: {move}")
        # starting square

        start, end = move
        piece_moving = self.state[start]

        next_ep_target = None

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

        self.state[end] = piece_moving
        self.state[start] = 0

        self.en_passant_target = next_ep_target
        self.turn = "b" if self.turn == "w" else "w"
        self.move_n += 1 if self.turn == "b" else 0