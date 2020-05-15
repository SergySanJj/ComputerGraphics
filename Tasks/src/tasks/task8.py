import math
import tkinter as tk
from random import random, randrange
from tkinter import *
from typing import List

from src.misc.point import Point, area, left_most, eps, right_most, left, cross_product_orientation
from src.misc.polygon import draw_polygon


class SmoothConvex(Frame):
    diam = 10
    point_color = "black"
    outline_color = ''

    def __init__(self, parent):
        self.vertexes: List[Point] = []
        self.hull: List[Point] = []

        Frame.__init__(self, parent)
        self.parent = parent

        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(6,
                             weight=1)
        self.rowconfigure(2, weight=1)

        self.canv = Canvas(self, bg="white")
        self.canv.grid(row=2, column=0, columnspan=7,
                       padx=5, pady=5,
                       sticky=E + W + S + N)

        self.canv.bind("<Button 1>", self.on_touch_left)
        self.canv.bind("<Button 3>", self.on_touch_right)

        clear_button = Button(self, text="Clear", command=self.on_clear)
        clear_button.grid(row=1, column=1, padx=6, pady=6)

    def on_touch_left(self, event):
        self.vertexes.append(Point(event.x, event.y))
        self.update_view()

    def on_touch_right(self, event):
        self.update_view()
        self.hull = simple_polygon_hull(self.vertexes, self.canv)
        draw_polygon(self.hull, self.canv, width=3)

    def update_view(self):
        self.canv.delete("all")
        if len(self.vertexes) == 0:
            return
        for p in self.vertexes:
            self.canv.create_oval(p.x - self.diam / 2, p.y - self.diam / 2, p.x + self.diam / 2,
                                  p.y + self.diam / 2, fill=self.point_color,
                                  width=2, outline=self.outline_color)

        draw_polygon(self.vertexes, self.canv)

    def on_clear(self):
        self.vertexes = []
        self.update_view()


def next_in(vertexes: List[Point], curr: int) -> (Point, int):
    if curr + 1 < len(vertexes):
        return vertexes[curr + 1], curr + 1
    else:
        return vertexes[0], 0


def prev_in(vertexes: List[Point], curr: int) -> (Point, int):
    if curr - 1 < 0:
        return vertexes[len(vertexes) - 1], len(vertexes) - 1
    else:
        return vertexes[curr - 1], curr - 1


def simple_polygon_hull(vertexes: List[Point], canvas: Canvas) -> List[Point]:
    q0, left_ind = left_most(vertexes)
    qm, right_ind = right_most(vertexes)

    Q = get_chain_hull(vertexes, left_ind, right_ind) + get_chain_hull(vertexes, right_ind, left_ind)

    return Q


def get_chain_hull(chain: List[Point], left_ind, right_ind) -> List[Point]:
    half_hull: List[Point] = []
    first = chain[left_ind]

    dummyNode = Point(first.x, first.y - eps)
    half_hull.append(dummyNode)
    half_hull.append(first)

    i = left_ind
    while i != right_ind:
        print(len(half_hull))
        next_to_peek = half_hull[len(half_hull) - 2]
        curr_node = chain[i]

        if not left(next_to_peek, curr_node, half_hull[len(half_hull) - 1]):
            if left(chain[right_ind], half_hull[len(half_hull) - 1], curr_node) or i == right_ind:
                half_hull.append(curr_node)
            p, i = next_in(chain, i)
        else:
            half_hull.pop()

    return half_hull


def task8_runner():
    root = Tk()
    root.geometry("1000x800")
    root.resizable(False, False)
    app = SmoothConvex(root)

    root.mainloop()
