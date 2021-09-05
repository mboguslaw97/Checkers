from ai import MinimaxAI, RandomAI
from board import Board
from constants import HEIGHT, WIDTH
from util import xy_to_rc
import pygame

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
pygame.font.init()
clock = pygame.time.Clock()

board = Board()
running = True

# Set AI to None for human input
# red_ai = MinimaxAI(8)
white_ai = MinimaxAI(8)
red_ai = None
# white_ai = None
# white_ai = RandomAI()

while running:
    board.draw(screen)
    pygame.display.update()
    clock.tick(5)

    if not board.gameover:
        if board.reds_turn and red_ai is not None:
            red_ai.move(board)
        elif not board.reds_turn and white_ai is not None:
            white_ai.move(board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not board.gameover and \
                (board.reds_turn and red_ai is None or not board.reds_turn and white_ai is None):
            pos = pygame.mouse.get_pos()
            rc = xy_to_rc(pos)
            board.select(rc)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                board.undo_move()
