import datetime
import chess.pgn
import pygame
from engine import get_engine_move
import queue
import threading
import queue
from converter import load_fen
import pygame
from board import Board
from moves import is_current_turn_piece

play_as = "w"
dark = (0,0,0)
light = (255,255,255)
sq_size = 60
depth = 3

pygame.init()
screen = pygame.display.set_mode((sq_size*8, sq_size*8))
clock = pygame.time.Clock()
running = True
font = pygame.font.Font("assets/dogicapixel.ttf", 25)

board = Board()
position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
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

w_text_surface = font.render("You won!", True, "Purple")
l_text_surface = font.render("You lost! skill issue lol", True, "Purple")

gui_pieces_paths = {
    1: "assets/wp.png",
    2: "assets/wn.png",
    3: "assets/wb.png",
    4: "assets/wr.png",
    5: "assets/wq.png",
    6: "assets/wk.png",

    -1: "assets/bp.png",
    -2: "assets/bn.png",
    -3: "assets/bb.png",
    -4: "assets/br.png",
    -5: "assets/bq.png",
    -6: "assets/bk.png"
}

gui_pieces_table = {}

def load_game_assets():
    for piece_value, path in gui_pieces_paths.items():
        try:
            raw_image = pygame.image.load(path).convert_alpha()
            scaled_image = pygame.transform.smoothscale(raw_image, (sq_size, sq_size))
            gui_pieces_table[piece_value] = scaled_image
        except pygame.error as e:
            print(f"Error loading asset {path}: {e}")

load_game_assets()
selected_square = None
selected_piece = (None, None)
possible_moves = board.get_possible_moves()

en_queue = queue.Queue()
en_thinking = False

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
                #CHANGED FOR DEBUG
                # if play_as == board.turn:
                c = (mouse_x) // sq_size
                r = mouse_y // sq_size
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
                    # CHANGED FOR DEBUG: board.turn instead of play_as
                    if is_current_turn_piece(board.state[selected_square], board.turn):
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

    screen.fill("purple")
    for r in range(8):
        for c in range(8):
            index = (r * 8) + c
            if (r + c) % 2 == 0:
                color = light
            else:
                color = dark
            if selected_piece[0] is not None:
                if (selected_piece[0], index) in possible_moves:
                    color = (100, 100,100)
            if selected_piece[0] == index:
                color = "purple"
            xpos_ = c*sq_size
            ypos_ = r*sq_size
            gui_board = pygame.draw.rect(screen, color, (xpos_, ypos_, sq_size, sq_size))
            index = (r*8)+c            

            piece_image = gui_pieces_table.get(board.state[index])
            if piece_image:
                screen.blit(piece_image, (xpos_, ypos_))

    if board.game_state != '-':
        game.headers["Event"] = "a phenomenal display of skill issue" if board.game_state != play_as else "Friendly Match"
        _rect = pygame.Rect(0, 0, screen.get_width(), 120)
        _rect.center = screen.get_rect().center
        pygame.draw.rect(screen, 'gray', _rect)
        if board.game_state == "w":
            text_rect = w_text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(w_text_surface, text_rect)
            game.headers["Results"] = "0-1"
        else:
            text_rect = l_text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(l_text_surface, text_rect)
            game.headers["Results"] = "1-0"
            
    print(game)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()