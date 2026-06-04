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

    def possible_moves(self, state):
        return 

    
    