from copy import deepcopy
from constants import BLACK, BLUE, COLS, HEIGHT, RED, ROWS, SQUARE_SIZE, WHITE, WIDTH
from util import add_to_dict_val, draw_circle, get_mid_rc, inc_attr
from piece import Piece
import pygame
import pygame.gfxdraw


class Board():
    def __init__(self):
        self.reds_turn = True
        self.gameover = False
        self.red_score = 15
        self.white_score = 15
        self.moves_since_jump = 0
        self.selected = None
        self.selected_locked = False
        self.history = []
        self.slides = {}
        self.jumps = {}
        self.board = {}
        for r in range(ROWS):
            for c in range(COLS):
                rc = (r, c)
                if c % 2 == (r + 1) % 2:
                    if r < 3:
                        self.create_piece(rc, False)
                    elif r > 4:
                        self.create_piece(rc, True)
        self.calc_all_moves()

        # Load a position from a list of moves
        moves = [((5, 2), (4, 3)), ((2, 7), (3, 6)), ((5, 6), (4, 7)), ((2, 1), (3, 0)), ((6, 1), (5, 2)), ((2, 3), (3, 4)), ((4, 3), (3, 2)), ((1, 2), (2, 3)), ((6, 5), (5, 6)), ((2, 3), (4, 1)), ((5, 0), (3, 2)), ((3, 4), (4, 3)), ((5, 2), (3, 4)), ((2, 5), (4, 3)), ((4, 3), (6, 5)), ((7, 6), (5, 4)), ((0, 1), (1, 2)), ((4, 7), (2, 5)), ((1, 4), (3, 6)), ((5, 6), (4, 5)), ((1, 6), (2, 7)), ((6, 7), (5, 6)), ((0, 3), (1, 4)), ((7, 0), (6, 1)), ((
            3, 0), (4, 1)), ((6, 1), (5, 2)), ((1, 2), (2, 3)), ((5, 2), (3, 0)), ((2, 3), (4, 1)), ((6, 3), (5, 2)), ((4, 1), (6, 3)), ((7, 4), (5, 2)), ((3, 6), (4, 7)), ((5, 2), (4, 3)), ((4, 7), (6, 5)), ((4, 3), (3, 2)), ((6, 5), (7, 6)), ((3, 0), (2, 1)), ((7, 6), (6, 5)), ((5, 4), (4, 3)), ((1, 4), (2, 3)), ((3, 2), (1, 4)), ((1, 0), (3, 2)), ((3, 2), (5, 4)), ((1, 4), (0, 3)), ((0, 7), (1, 6)), ((4, 5), (3, 4)), ((0, 5), (1, 4))]
        self.load(moves)

    def create_piece(self, rc, red, king=False):
        self.board[rc] = Piece(rc, red, king)

    def load(self, history):
        for move in history:
            self.move(*move)

    def select(self, rc):
        if rc in self.get_moves():
            self.clear_selected()
            self.selected = self.get_piece(rc)
            self.selected.selected = True
        elif rc in self.get_selected_moves():
            self.move(self.selected.rc, rc)
        elif not self.selected_locked:
            self.clear_selected()

    def get_selected_moves(self):
        return set() if self.selected is None else self.get_moves()[self.selected.rc]

    def get_moves(self):
        return self.jumps if len(self.jumps) > 0 else self.slides

    def calc_all_moves(self):
        self.clear_moves()
        for piece in self.board.values():
            if piece.red == self.reds_turn:
                self.calc_piece_moves(piece.rc)

    def calc_piece_moves(self, rc):
        r, c = rc
        piece = self.board[rc]
        for dr in [-1, 1]:
            for dc in [-1, 1]:
                rc2 = r + dr, c + dc
                if self.is_in_bounds(rc2) and (piece.king or (dr == -1 and self.reds_turn or dr == 1 and not self.reds_turn)):
                    piece2 = self.get_piece(rc2)
                    if piece2 is None:
                        add_to_dict_val(self.slides, piece.rc, rc2)
                    elif piece2.red != self.reds_turn:
                        rc3 = (r + 2*dr, c + 2*dc)
                        if self.is_in_bounds(rc3) and self.get_piece(rc3) is None:
                            add_to_dict_val(self.jumps, piece.rc, rc3)

    def move(self, rc1, rc2):
        metadata = self.get_metadata()

        if self.can_jump():
            jumped = True
            promo, jumped = self.jump_and_update_turn(rc1, rc2)
        else:
            jumped = None
            promo = self.slide_and_update_turn(rc1, rc2)

        self.history.append(((rc1, rc2), promo, jumped, metadata))

    def undo_move(self):
        (rc1, rc2), promo, jumped, metadata = self.history.pop()
        self.slide(rc2, rc1)
        if promo:
            self.board[rc1].king = False
        if jumped is not None:
            self.board[jumped.rc] = jumped
        self.reds_turn, self.gameover, self.red_score, self.white_score, self.moves_since_jump, self.selected_locked = metadata
        self.clear_selected()
        self.clear_moves()

        if self.selected_locked:
            self.calc_piece_moves(rc1)
        else:
            self.calc_all_moves()

    def get_metadata(self):
        return (
            self.reds_turn,
            self.gameover,
            self.red_score,
            self.white_score,
            self.moves_since_jump,
            self.selected_locked
        )

    def jump_and_update_turn(self, rc1, rc2):
        self.slide(rc1, rc2)
        mid_rc = get_mid_rc(rc1, rc2)
        piece = self.board.pop(mid_rc)
        promo = self.check_promo(rc2)

        del_score = -1.5 if piece.king else -1
        score_key = 'white_score' if self.reds_turn else 'red_score'
        inc_attr(self, score_key, del_score)

        self.moves_since_jump = 0
        self.clear_moves()
        self.calc_piece_moves(rc2)

        if not promo and self.can_jump():
            self.selected_locked = True
        else:
            self.change_turn()
            self.selected_locked = False

        return promo, deepcopy(piece)

    def can_jump(self):
        return len(self.jumps) > 0

    def slide_and_update_turn(self, rc1, rc2):
        self.slide(rc1, rc2)
        promo = self.check_promo(rc2)
        self.moves_since_jump += 1
        self.change_turn()
        return promo

    def slide(self, rc1, rc2):
        piece = self.board.pop(rc1)
        piece.rc = rc2
        self.board[rc2] = piece

    def check_promo(self, rc):
        piece = self.board[rc]
        if not piece.king and rc[0] in (0, 7):
            piece.king = True
            score_key = 'red_score' if piece.red else 'white_score'
            inc_attr(self, score_key, 0.5)
            return True
        return False

    def change_turn(self):
        self.reds_turn = not self.reds_turn
        self.clear_selected()
        self.calc_all_moves()
        self.check_gameover()

    def clear_selected(self):
        if self.selected is not None:
            self.selected.selected = False
        self.selected = None

    def clear_moves(self):
        self.slides = {}
        self.jumps = {}

    def get_piece(self, rc):
        return self.board.get(rc, None)

    def is_in_bounds(self, rc):
        r, c = rc
        return r >= 0 and r < ROWS and c >= 0 and c < COLS

    def check_gameover(self):
        no_moves = len(self.get_moves()) == 0
        if no_moves and self.reds_turn:
            self.end_game('White wins')
        elif no_moves and not self.reds_turn:
            self.end_game('Red wins')
        elif self.moves_since_jump == 50:
            self.end_game('Draw')

    def end_game(self, msg):
        self.gameover = True
        self.gameover_msg = msg

    def draw(self, screen):
        screen.fill(BLACK)
        for r in range(ROWS):
            for c in range(COLS):
                if r % 2 == c % 2:
                    pygame.draw.rect(screen, RED, (r * SQUARE_SIZE,
                                                   c * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        for piece in self.board.values():
            piece.draw(screen)

        for move in self.get_selected_moves():
            draw_circle(screen, BLUE, move, 15)

        if self.gameover:
            text = pygame.font.SysFont('cambria', 100, True).render(
                self.gameover_msg, True, WHITE, BLACK)
            text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(text, text_rect)
