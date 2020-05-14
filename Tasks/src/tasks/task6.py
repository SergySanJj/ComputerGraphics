import math
import tkinter as tk
from tkinter import *
from typing import List

from src.misc.point import Point, area, left_most, left, collinear, between
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

        clear_button = Button(self, text="Clear", command=self.on_clear)
        clear_button.grid(row=1, column=1, padx=6, pady=6)

    def on_touch_left(self, event):
        self.vertexes.append(Point(event.x, event.y))
        self.update_view()

    def update_view(self):
        self.canv.delete("all")
        if len(self.vertexes) == 0:
            return
        for p in self.vertexes:
            self.canv.create_oval(p.x - self.diam / 2, p.y - self.diam / 2, p.x + self.diam / 2,
                                  p.y + self.diam / 2, fill=self.point_color,
                                  width=2, outline=self.outline_color)

        self.hull = jarvis_hull(self.vertexes)
        draw_polygon(self.hull, self.canv)

    def on_clear(self):
        self.vertexes = []
        self.update_view()


def jarvis_hull(vertexes: List[Point]) -> List[Point]:
    _, start = left_most(vertexes)
    convex_hull: List[Point] = [vertexes[start]]
    selected = [False] * len(vertexes)
    while True:
        best = -1
        previous = convex_hull[len(convex_hull) - 1]
        for i in range(0, len(vertexes)):
            if not selected[i]:
                if best == -1:
                    best = i
                elif left(previous, vertexes[best], vertexes[i]):
                    best = i
                elif (collinear(previous, vertexes[best], vertexes[i]) and between(previous, vertexes[best],
                                                                                   vertexes[i])):
                    best = i

        if best == -1 or left(previous, vertexes[best], vertexes[start]):
            break
        else:
            selected[best] = True
            convex_hull.append(vertexes[best])

    return convex_hull


def task6_runner():
    root = Tk()
    root.geometry("1000x800")
    root.resizable(False, False)
    app = SmoothConvex(root)

    root.mainloop()
