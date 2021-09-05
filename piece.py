from constants import CROWN, GREY, RED, SQUARE_SIZE, WHITE
from util import draw_circle, rc_to_xy


class Piece:
    def __init__(self, rc, red, king=True):
        self.rc = rc
        self.red = red
        self.color = RED if red else WHITE
        self.king = king
        self.selected = False

    def draw(self, screen):
        radius = SQUARE_SIZE // 2 - 15
        outline = 4 if self.selected else 2
        draw_circle(screen, GREY, self.rc, radius + outline)
        draw_circle(screen, self.color, self.rc, radius)
        x, y = rc_to_xy(self.rc)
        if self.king:
            screen.blit(CROWN, (x - CROWN.get_width() //
                        2, y - CROWN.get_height() // 2))
