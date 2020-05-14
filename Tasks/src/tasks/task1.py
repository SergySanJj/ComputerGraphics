import math
import tkinter as tk
from random import random, randrange
from tkinter import *
from typing import List

from src.misc.point import Point, area, left, eps
from src.misc.polygon import draw_polygon


class SmoothConvex(Frame):
    diam = 10
    point_color = "black"
    outline_color = ''

    def __init__(self, parent):
        self.vertexes = []

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
        z = Point(event.x, event.y)
        if check_if_inside(z, self.vertexes, self.canv):
            self.canv.create_text(200, 200, text="Inside",
                                  anchor=SE, fill="red", font=("Purisa", 18))
            print("Inside")
        else:
            print("Outside")
            self.canv.create_text(200, 200, text="Outside",
                                  anchor=SE, fill="red", font=("Purisa", 18))

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


def check_if_inside(z: Point, vertexes: List[Point], canvas: Canvas) -> bool:
    if len(vertexes) < 3:
        return False
    canvas.create_line([z.x, z.y, z.x + 10000, z.y], fill="red")
    a = vertexes[0]
    inside = ray_intersects_segment(z, vertexes[len(vertexes) - 1], a)
    for i in range(0, len(vertexes[1:])):
        b = vertexes[1:][i]
        if ray_intersects_segment(z, a, b):
            inside = not inside

        a = b

    return inside


def ray_intersects_segment(p: Point, a: Point, b: Point) -> bool:
    return (a.y >= p.y + eps) != (b.y - eps >= p.y) and p.x <= (b.x - a.x) * (p.y - a.y) / (b.y - a.y) + a.x


def task1_runner():
    root = Tk()
    root.geometry("1000x800")
    root.resizable(False, False)
    app = SmoothConvex(root)

    root.mainloop()
