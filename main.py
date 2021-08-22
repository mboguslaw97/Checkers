from ai import MinimaxAI, RandomAI
from board import Board
from constants import FPS, HEIGHT, RED, WHITE, WIDTH
from util import xy_to_rc
import pygame

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
pygame.font.init()
clock = pygame.time.Clock()

board = Board()
running = True

# Set AI to None for human input
white_ai = MinimaxAI(2)
red_ai = MinimaxAI(4)
# red_ai = None

while running:
    board.draw(screen)
    pygame.display.update()
    clock.tick(5)

    if not board.gameover:
        if board.turn == WHITE and white_ai is not None:
            white_ai.move(board)
        elif board.turn == RED and red_ai is not None:
            red_ai.move(board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not board.gameover and \
                (board.turn == WHITE and white_ai is None or board.turn == RED and red_ai is None):
            pos = pygame.mouse.get_pos()
            rc = xy_to_rc(pos)
            board.select(rc)
