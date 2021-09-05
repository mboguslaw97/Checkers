import time
from util import inc_attr
from copy import deepcopy
import random


def get_moves(board):
    moves = []
    for rc1, rc2s in board.get_moves().items():
        moves.extend([(rc1, rc2) for rc2 in rc2s])
    random.shuffle(moves)
    return moves


class RandomAI:
    def move(self, board):
        moves = get_moves(board)
        board.move(*moves[0])


class MinimaxAI:
    def __init__(self, depth):
        self.depth = depth
        self.cache = {}

    def move(self, board):
        self.leafs = 0
        self.copy_time = 0
        t0 = time.time()

        moves = get_moves(board)
        if len(moves) == 1:
            move = moves.pop()
        else:
            self.red = board.reds_turn
            _, move = self.minimax(board, self.depth)
        board.move(*move)

        # Debugging
        move_history = [x[0] for x in board.history]
        print(move_history)
        print('Leaf nodes visited:', self.leafs)
        print('Time spent copying:', self.copy_time)
        print('Total time spent thinknig:', time.time() - t0)
        print()

    def minimax(self, board, depth, alpha=-float('inf'), beta=float('inf')):
        board_score = self.get_score(board)
        if depth == 0 or board.gameover:
            self.leafs += 1
            return board_score, None

        maximize = board.reds_turn == self.red
        moves = get_moves(board)

        # Minimax
        best_score = -float('inf') if maximize else float('inf')
        best_move = None

        for move in moves:
            # Slower but simpler
            # score = self.move_deep_copy(board, move, depth, alpha, beta)
            score = self.move_in_place(board, move, depth, alpha, beta)

            if maximize and score > best_score:
                alpha = max(alpha, score)
                best_score = score
                best_move = move
            elif not maximize and score < best_score:
                beta = min(beta, score)
                best_score = score
                best_move = move
            if beta <= alpha:
                break

        return best_score, best_move

    def move_deep_copy(self, board, move, depth, alpha, beta):
        t0 = time.time()
        board2 = deepcopy(board)
        self.copy_time += time.time() - t0

        board2.move(*move)
        depth2 = depth if board.reds_turn == board2.reds_turn else depth - 1
        score, _ = self.minimax(board2, depth2, alpha, beta)
        return score

    def move_in_place(self, board, move, depth, alpha, beta):
        was_reds_turn = board.reds_turn
        board.move(*move)

        depth2 = depth if was_reds_turn == board.reds_turn else depth - 1
        score, _ = self.minimax(board, depth2, alpha, beta)

        t0 = time.time()
        board.undo_move()
        self.copy_time += time.time() - t0

        return score

    def get_score(self, board):
        s1, s2 = board.white_score, board.red_score
        if self.red:
            s1, s2 = s2, s1
        if s2 == 0:
            return float('inf')
        return s1 / s2

        # Alternate scoring system
        # return s1 - s2
