import math
from typing import List


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


def left(candidates: List[Point]) -> Point:
    res = candidates[0]
    for p in candidates:
        if p.x < res.x:
            res = p
    return res
