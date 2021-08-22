from constants import WHITE
from copy import deepcopy
import random


def get_moves(board):
    moves = []
    for rc1, rc2s in board.get_moves().items():
        moves.extend([(rc1, rc2) for rc2 in rc2s])
    random.shuffle(moves)
    return moves


def random_move(board):
    move = get_moves(board)[0]
    board.move_and_update_turn(*move)


def minimax_move(board):
    def metric(board):
        if color == WHITE:
            c1, c2 = board.white_count, board.red_count
        else:
            c1, c2 = board.red_count, board.white_count
        if c2 == 0:
            return 20
        return c1 / c2

    def recurse(board, depth):
        if depth == 0 or board.gameover:
            return metric(board), None

        use_max = board.turn == color
        depth2 = depth if board.can_jump() else depth - 1
        best_val = -1 if use_max else 20
        best_move = None
        for move in get_moves(board):
            board2 = deepcopy(board)
            board2.move_and_update_turn(*move)
            val, _ = recurse(board2, depth2)
            if depth == 4:
                print(val, move)
            # Optimization: undo move instead of creating copy
            # board.undo_move_and_update_turn(*move)
            if use_max and val > best_val or not use_max and val < best_val:
                best_val = val
                best_move = move
        return best_val, best_move

    color = board.turn
    _, move = recurse(board, 4)
    board.move_and_update_turn(*move)
