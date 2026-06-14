import datetime
import chess.pgn
import pygame
import queue
import threading
import queue
from pyngin.converter import load_fen
from pyngin.board import Board
from pyngin.moves import is_current_turn_piece
from pyngin.engine import get_engine_move

play_as = "w"
dark = (120, 79, 72)
light = (226, 213, 161)
sq_size = 60
piece_size = 46
depth = 5
hint_size = 24

prpl = (64, 54, 65)

pygame.init()
screen = pygame.display.set_mode((sq_size*8+20, sq_size*8+20))
clock = pygame.time.Clock()
running = True
font = pygame.font.Font("assets/dogicapixel.ttf", 24)
font_ = pygame.font.Font("assets/dogicapixel.ttf", 16)

board = Board()
position = "8/2qk4/8/8/4K3/8/8/8 b - - 0 1"
load_fen(position, board)

game_history = [(tuple(board.state), board.turn)]

game = chess.pgn.Game()
game.headers["Event"] = "Friendly Match"
game.headers["White"] = "Player" if play_as == "w" else "Computer"
game.headers["Black"] = "Computer" if play_as == "w" else "Player"

game.headers["SetUp"] = "1"
game.headers["FEN"] = position
game.headers["Date"] = datetime.datetime.now().strftime("%Y.%m.%d")
board.pgn_node = game

w_text_surface = font.render("at least you won once ig".upper(), True, prpl)
l_text_surface = font.render("You lost! skill issue lol".upper(), True, prpl)

w_spritesheet = pygame.image.load("assets/w_pieces.png").convert_alpha()
d_spritesheet = pygame.image.load("assets/d_pieces.png").convert_alpha()
move_hint = pygame.image.load("assets/m_hint.png").convert_alpha()
overlay = pygame.image.load("assets/overlay.png").convert_alpha()

selected_square = None
selected_piece = (None, None)
possible_moves = board.get_possible_moves()

en_queue = queue.Queue()
en_thinking = False

pimg_width = 16
pimg_height = 16

def get_piece_img(row, col, type):
    spritesheet = w_spritesheet if type == 'w' else d_spritesheet
    piece_rect = pygame.Rect(col * pimg_width, row * pimg_height, pimg_width, pimg_height)
    return pygame.transform.scale(spritesheet.subsurface(piece_rect), (piece_size, piece_size))

pieces = {
    1:get_piece_img(0, 0, 'w'),
    2:get_piece_img(0, 1, 'w'),
    3:get_piece_img(0, 3, 'w'),
    4:get_piece_img(0, 2, 'w'),
    5:get_piece_img(0, 5, 'w'),
    6:get_piece_img(0, 4, 'w'),

    -1:get_piece_img(0, 0, 'b'),
    -2:get_piece_img(0, 1, 'b'),
    -3:get_piece_img(0, 3, 'b'),
    -4:get_piece_img(0, 2, 'b'),
    -5:get_piece_img(0, 5, 'b'),
    -6:get_piece_img(0, 4, 'b'),
}

def engine_worker_thread(board_clone, depth, communication_queue, game_history_):
    engine_move = get_engine_move(board_clone, depth, game_history=game_history_)
    communication_queue.put(engine_move)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if board.game_state == '-':
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if play_as == board.turn:
                    c = (mouse_x - 5) // sq_size
                    r = (mouse_y - 5) // sq_size
                    if 0 <= c <= 7 and 0 <= r <= 7:
                        if (selected_square, (r*8) + c ) in possible_moves:
                                board.make_move((selected_square, (r*8) + c))
                                game_history.append((tuple(board.state), board.turn))
                                selected_piece = (None, None)
                                selected_square = None
                                possible_moves = board.get_possible_moves()
                                if len(possible_moves) == 0 and board.is_in_check():
                                    board.game_state = play_as

                        else:
                            selected_square = (r * 8) + c
                            if is_current_turn_piece(board.state[selected_square], play_as):
                                selected_piece = (selected_square, board.state[selected_square])
                            else:
                                selected_piece = (None, None)

    if board.game_state == '-':
        if board.turn != play_as and not en_thinking and running:
            en_thinking = True
            board_clone = board.clone()
            threading.Thread(
                target=engine_worker_thread,
                args=(board_clone, depth, en_queue, list(game_history)),
                daemon=True
            ).start()

        if en_thinking and not en_queue.empty():
            en_move = en_queue.get()
            if en_move:
                board.make_move(en_move)
                game_history.append((tuple(board.state), board.turn))
            possible_moves = board.get_possible_moves()
            if len(possible_moves) == 0 and board.is_in_check():
                board.game_state = 'b' if play_as == "w" else "w"
            en_thinking = False

    screen.fill(prpl)
    for r in range(8):
        for c in range(8):
            index = (r * 8) + c
            xpos_ = c*sq_size + 10
            ypos_ = r*sq_size + 10
            if (r + c) % 2 == 0:
                color = light
            else:
                color = dark

            gui_board = pygame.draw.rect(screen, color, (xpos_, ypos_, sq_size, sq_size))

            if selected_piece[0] == index:
                screen.blit(pygame.transform.scale(overlay, (sq_size, sq_size)), (xpos_, ypos_))


            if selected_piece[0] is not None:
                if (selected_piece[0], index) in possible_moves:
                    screen.blit(pygame.transform.scale(move_hint, (hint_size, hint_size)), (xpos_+((sq_size-hint_size) // 2), ypos_+((sq_size-hint_size) // 2)))


            piece_image = pieces.get(board.state[index])
            if piece_image:
                offset = (sq_size - piece_size) // 2
                screen.blit(piece_image, (xpos_+offset, ypos_+offset))
            if r == 7:
                if c % 2 == 0:
                    color_ = light
                else:
                    color_ = dark
                txt = font_.render(chr(c+97), True, color_)
                txt_rect = txt.get_rect(center=(xpos_+45, ypos_+45))
                screen.blit(txt, txt_rect)
            if c == 0:
                if r % 2 != 0:
                    color_ = light
                else:
                    color_ = dark
                txt = font_.render(f"{8-r}".upper(), True, color_)
                txt_rect = txt.get_rect(center=(xpos_+15, ypos_+15))
                screen.blit(txt, txt_rect)

    if board.game_state != '-':
        game.headers["Event"] = "a phenomenal display of skill issue" if board.game_state != play_as else "Friendly Match"
        _rect = pygame.Rect(0, 0, screen.get_width(), 90)
        _rect.center = screen.get_rect().center
        pygame.draw.rect(screen, light, _rect)
        border_rect = _rect.inflate(10, 10)
        pygame.draw.rect(screen, prpl, border_rect, width=5)
        if board.game_state == "w":
            text_rect = w_text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(w_text_surface, text_rect)
            game.headers["Results"] = "0-1"
        else:
            text_rect = l_text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(l_text_surface, text_rect)
            game.headers["Results"] = "1-0"
            
    # print(game)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()