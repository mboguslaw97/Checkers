from constants import HEIGHT, RED, WHITE, WIDTH
import random


def random_move(board):
    moves = []
    for rc1, rc2s in board.get_moves().items():
        moves.extend([(rc1, rc2) for rc2 in rc2s])
    move = random.choice(moves)
    board.move_and_update_turn(*move)
