import math
import random
from .vector import *


def noise(x, y, seed):
    floor_x = math.floor(x) & 255
    floor_y = math.floor(y) & 255
    xf = x - math.floor(x)
    yf = y - math.floor(y)

    top_right = Vector(xf - 1, yf - 1)
    top_left = Vector(xf, yf - 1)
    bottom_right = Vector(xf - 1, yf)
    bottom_left = Vector(xf, yf)

    p = permutation(seed)

    value_top_right = p[p[floor_x + 1] + floor_y + 1]
    value_top_left = p[p[floor_x] + floor_y + 1]
    value_bottom_right = p[p[floor_x + 1] + floor_y]
    value_bottom_left = p[p[floor_x] + floor_y]

    dot_top_right = top_right.dot(constant_vector(value_top_right))
    dot_top_left = top_left.dot(constant_vector(value_top_left))
    dot_bottom_right = bottom_right.dot(constant_vector(value_bottom_right))
    dot_bottom_left = bottom_left.dot(constant_vector(value_bottom_left))

    u = fade(xf)
    v = fade(yf)
    return lerp(u, lerp(v, dot_bottom_left, dot_top_left), lerp(v, dot_bottom_right, dot_top_right))


def permutation(seed):
    p = list(range(256))
    random.Random(seed).shuffle(p)
    p = 2 * p
    return p


def constant_vector(v):
    h = v & 3
    if h == 0:
        vector = Vector(1, 1)
    elif h == 1:
        vector = Vector(-1, 1)
    elif h == 2:
        vector = Vector(-1, -1)
    else:
        vector = Vector(1, -1)
    return vector


def lerp(t, x1, x2):
    return x1 + t * (x2 - x1)


def fade(t):
    return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3
