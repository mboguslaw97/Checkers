from constants import CROWN, GREY, SQUARE_SIZE
from util import draw_circle, rc_to_xy


class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, rc, color):
        self.rc = rc
        self.color = color
        self.king = False

    def draw(self, screen):
        radius = SQUARE_SIZE // 2 - self.PADDING
        draw_circle(screen, GREY, self.rc, radius + self.OUTLINE)
        draw_circle(screen, self.color, self.rc, radius)
        x, y = rc_to_xy(self.rc)
        if self.king:
            screen.blit(CROWN, (x - CROWN.get_width() //
                                2, y - CROWN.get_height() // 2))
