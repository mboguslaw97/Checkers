from constants import BLACK, BLUE, COLS, HEIGHT, RED, ROWS, SQUARE_SIZE, WHITE, WIDTH
from util import add_to_dict_val, draw_circle, get_mid_rc
from piece import Piece
import pygame
import pygame.gfxdraw


class Board:
    def __init__(self):
        self.turn = RED
        self.gameover = False
        self.moves_since_jump = 0
        self.board = {}
        for r in range(ROWS):
            for c in range(COLS):
                rc = (r, c)
                if c % 2 == (r + 1) % 2:
                    if r < 3:
                        self.board[rc] = Piece(rc, WHITE)
                    elif r > 4:
                        self.board[rc] = Piece(rc, RED)
        self.clear_moves()
        self.clear_selected()
        self.calc_all_moves()

    def select(self, rc):
        if rc in self.get_moves():
            self.selected = self.get_piece(rc)
        elif rc in self.get_selected_moves():
            self.move_and_update_turn(self.selected.rc, rc)
        elif not self.selected_locked:
            self.clear_selected()

    def get_selected_moves(self):
        return set() if self.selected is None else self.get_moves()[self.selected.rc]

    def get_moves(self):
        return self.jumps if len(self.jumps) > 0 else self.slides

    def move_and_update_turn(self, rc1, rc2):
        if self.can_jump():
            self.jump_and_update_turn(rc1, rc2)
        else:
            self.slide_and_update_turn(rc1, rc2)
        if rc2[0] in (0, 7):
            self.board[rc2].king = True

    def slide_and_update_turn(self, rc1, rc2):
        self.slide(rc1, rc2)
        self.moves_since_jump += 1
        self.change_turn()

    def slide(self, rc1, rc2):
        selected = self.board.pop(rc1)
        selected.rc = rc2
        self.board[rc2] = selected

    def jump_and_update_turn(self, rc1, rc2):
        self.jump(rc1, rc2)
        self.moves_since_jump = 0

        self.clear_moves()
        self.calc_piece_moves(rc2)
        if self.can_jump():
            self.selected_locked = True
        else:
            self.change_turn()

    def jump(self, rc1, rc2):
        self.slide(rc1, rc2)
        mid_rc = get_mid_rc(rc1, rc2)
        del self.board[mid_rc]

    def can_jump(self):
        return len(self.jumps) > 0

    def change_turn(self):
        self.turn = RED if self.turn == WHITE else WHITE
        self.clear_selected()
        self.calc_all_moves()
        self.check_gameover()
        # self.debug()

    def clear_selected(self):
        self.selected = None
        self.selected_locked = False

    def calc_all_moves(self):
        self.clear_moves()
        for piece in self.board.values():
            if piece.color == self.turn:
                self.calc_piece_moves(piece.rc)

    def clear_moves(self):
        self.slides = {}
        self.jumps = {}

    def calc_piece_moves(self, rc):
        r, c = rc
        piece = self.board[rc]
        for dr in [-1, 1]:
            for dc in [-1, 1]:
                rc2 = r + dr, c + dc
                if self.is_in_bounds(rc2) and (piece.king or (dr == 1 and self.turn == WHITE or dr == -1 and self.turn == RED)):
                    piece2 = self.get_piece(rc2)
                    if piece2 is None:
                        add_to_dict_val(self.slides, piece.rc, rc2)
                    elif piece2.color != self.turn:
                        rc3 = (r + 2*dr, c + 2*dc)
                        if self.is_in_bounds(rc3) and self.get_piece(rc3) is None:
                            add_to_dict_val(self.jumps, piece.rc, rc3)

    def get_piece(self, rc):
        return self.board.get(rc, None)

    def is_in_bounds(self, rc):
        r, c = rc
        return r >= 0 and r < ROWS and c >= 0 and c < COLS

    def check_gameover(self):
        no_moves = len(self.get_moves()) == 0
        if no_moves and self.turn == WHITE:
            self.end_game('Red wins')
        elif no_moves and self.turn == RED:
            self.end_game('White wins')
        elif self.moves_since_jump == 20:
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

    def debug(self):
        print('turn:', self.turn)
        print('slides:', self.slides)
        print('jumps:', self.jumps)
        print()
