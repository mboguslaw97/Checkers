from constants import SQUARE_SIZE
import pygame.gfxdraw


def inc_attr(obj, key, amt):
    val = getattr(obj, key)
    setattr(obj, key, val + amt)


def add_to_dict_val(d, k, v):
    s = d.get(k, set())
    s.add(v)
    d[k] = s


def get_mid_rc(rc1, rc2):
    def get_mid(a, b):
        return (a + b) // 2

    return get_mid(rc1[0], rc2[0]), get_mid(rc1[1], rc2[1])


def xy_to_rc(xy):
    return xy[1] // SQUARE_SIZE, xy[0] // SQUARE_SIZE


def rc_to_xy(rc):
    def get_real(n):
        return SQUARE_SIZE * n + SQUARE_SIZE // 2

    return get_real(rc[1]), get_real(rc[0])


def draw_circle(surface, color, rc, radius):
    x, y = rc_to_xy(rc)
    pygame.gfxdraw.aacircle(surface, x, y, radius, color)
    pygame.gfxdraw.filled_circle(surface, x, y, radius, color)
