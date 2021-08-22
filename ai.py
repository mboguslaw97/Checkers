from constants import RED
from copy import deepcopy
import random


def get_moves(board):
    moves = []
    for rc1, rc2s in board.get_moves().items():
        moves.extend([(rc1, rc2) for rc2 in rc2s])
    random.shuffle(moves)
    return moves


class RandomAI:
    def move(board):
        move = get_moves(board)[0]
        board.move(*move)


class MinimaxAI:
    def __init__(self, depth):
        self.depth = depth

    def move(self, board):
        self.color = board.turn
        _, move = self.minimax(board, self.depth)
        board.move(*move)

    def minimax(self, board, depth):
        if depth == 0 or board.gameover:
            return self.metric(board), None

        use_max = board.turn == self.color
        depth2 = depth if board.can_jump() else depth - 1
        best_val = -float('inf') if use_max else float('inf')
        best_move = None
        for move in get_moves(board):
            board2 = deepcopy(board)
            board2.move(*move)
            val, _ = self.minimax(board2, depth2)
            if use_max and val > best_val or not use_max and val < best_val:
                best_val = val
                best_move = move
        return best_val, best_move

    def metric(self, board):
        s1, s2 = board.white_score, board.red_score
        if self.color == RED:
            s1, s2 = s2, s1
        if s2 == 0:
            return float('inf')
        return s1 / s2
