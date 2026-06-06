import moves
from moves import get_psudo_moves

class Board:

    def __init__(self, state=None):
        if state is None:
            self.state:list[int] = [0]*64
        else:
            self.state = list(state)

        self.white_to_move = True
        self.castling_rights = {
            'wK': True, 'wQ': True,
            'bK': True, 'bQ': True  
        }
        self.en_passant_square = None
        self.move_n = 1
        self.turn = 'w'


    # TO BE CHANGED
    def get_possible_moves(self):
        return get_psudo_moves(self)
        

    def make_move(self, move):
        print(f"made move: {move}")
        # starting square
        self.state[move[1]] = self.state[move[0]] 
        captured_piece = self.state[move[1]]
        self.state[move[0]] = 0
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = "w"
        return move, captured_piece
    