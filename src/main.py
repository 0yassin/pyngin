from engine import get_engine_move
import queue
import threading
import queue
from converter import load_fen
import pygame
from board import Board
from moves import is_current_turn_piece
from evaluate import evaluate_position

play_as = "w"
dark = (0,0,0)
light = (255,255,255)
sq_size = 60
depth = 3

pygame.init()
screen = pygame.display.set_mode((540, sq_size*8))
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont("Arial", 40)

board = Board()
position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
load_fen(position, board)

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

def engine_worker_thread(board_clone, depth, communication_queue):
    engine_move = get_engine_move(board_clone, depth)
    communication_queue.put(engine_move)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x >= 60:
                #CHANGED FOR DEBUG
                # if play_as == board.turn:
                    c = (mouse_x - 60) // sq_size
                    r = mouse_y // sq_size
                    if (selected_square, (r*8) + c ) in possible_moves:
                            board.make_move((selected_square, (r*8) + c))
                            selected_piece = (None, None)
                            selected_square = None
                            possible_moves = board.get_possible_moves()
                    else:
                        selected_square = (r * 8) + c
                        # CHANGED FOR DEBUG: board.turn instead of play_as
                        if is_current_turn_piece(board.state[selected_square], board.turn):
                            selected_piece = (selected_square, board.state[selected_square])

                        else:
                            selected_piece = (None, None)

    if board.turn != play_as and not en_thinking and running:
        if len(possible_moves) == 0:
            print("Game Over!")
        else: 
            en_thinking = True
            board_clone = board.clone()
            threading.Thread(
                target=engine_worker_thread,
                args=(board_clone, depth, en_queue),
                daemon=True
            ).start()

    if en_thinking and not en_queue.empty():
        en_move = en_queue.get()
        if en_move:
            board.make_move(en_move)
        possible_moves = board.get_possible_moves()
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
            xpos_ = c*sq_size+60 
            ypos_ = r*sq_size
            gui_board = pygame.draw.rect(screen, color, (xpos_, ypos_, sq_size, sq_size))
            index = (r*8)+c            

            if gui_pieces_table.get(board.state[index]):
                # pyrefly: ignore [bad-argument-type]
                screen.blit(gui_pieces_table.get(board.state[index]), (xpos_, ypos_))

    pygame.draw.rect(screen, "gray", (0,0, sq_size, screen.get_height()))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()