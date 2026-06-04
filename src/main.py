import pygame
from board import Board





pygame.init()


dark = (0,0,0)
light = (255,255,255)

sq_size = 60

font = pygame.font.SysFont("Arial", 40)



board = Board()

screen = pygame.display.set_mode((720, sq_size*8))
clock = pygame.time.Clock()
running = True


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")


    for r in range(8):
        for c in range(8):
            if (r+c) % 2 == 0:
                color = light
            else:
                color=dark
            

            gui_board = pygame.draw.rect(screen, color, (c*sq_size+60, r*sq_size, sq_size, sq_size))
            index = (r*8)+c
            text_surface = font.render(str(board.state[index]), True, "purple")


            screen.blit(text_surface, (c*sq_size+60, r*sq_size))





    pygame.draw.rect(screen, "gray", (0,0, sq_size, screen.get_height()))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()