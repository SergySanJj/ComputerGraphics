import math
from typing import List

eps = 0.00001


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_duplicate(self, other):
        return self.x == other.x and self.y == other.y

    def polar_angle(self, origin):
        dx = self.x - origin.x
        dy = self.y - origin.y
        th = math.atan2(dy, dx)
        return th


def sq_dist(a, b):
    return (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)


def cross_product(a, b):
    return a.x * b.y - b.x * a.y


def cross_product_orientation(a: Point, b: Point, c: Point):
    return (b.y - a.y) * \
           (c.x - a.x) - \
           (b.x - a.x) * \
           (c.y - a.y)


def area(a: Point, b: Point, c: Point):
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


def left_most(candidates: List[Point]) -> (Point, int):
    i = 0
    res_i = 0
    res = candidates[0]
    for p in candidates:
        if p.x < res.x:
            res = p
            res_i = i
        i += 1
    return res, res_i


def right_most(candidates: List[Point]) -> (Point, int):
    i = 0
    res_i = 0
    res = candidates[0]
    for p in candidates:
        if p.x > res.x:
            res = p
            res_i = i
        i += 1
    return res, res_i


def left(a, b, c) -> bool:
    return area(a, b, c) > 0


def collinear(a, b, c) -> bool:
    return area(a, b, c) == 0


def between(a, b, point) -> bool:
    return abs(point.x - a.x) <= abs(b.x - a.x) and abs(point.y - a.y) <= abs(
        b.y - a.y)
