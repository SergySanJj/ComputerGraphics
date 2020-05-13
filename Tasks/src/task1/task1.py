import tkinter as tk
from tkinter import *
from typing import List


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_duplicate(self, other):
        return self.x == other.x and self.y == other.y


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

        l = left(self.vertexes)
        r = Point(l.x, l.y - 0.001)
        hull = quick_hull(l, r, self.vertexes, [])
        print([p.x for p in hull])
        draw_hull(hull, self.canv)

    def on_clear(self):
        self.vertexes = []
        self.update_view()


def area(a: Point, b: Point, c: Point):
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


def quick_hull(l: Point, r: Point, candidates: List[Point], quick_hull_res: List[Point]):
    best = 0
    actual_candidates: List[Point] = []
    for candidate in candidates:
        if area(l, r, candidate) >= 0:
            actual_candidates.append(candidate)
            if area(l, r, candidate) >= area(l, r, actual_candidates[best]):
                best = len(actual_candidates) - 1
    if len(actual_candidates) > 0:
        chosen = actual_candidates[best]
        quick_hull_res.append(chosen)
        del actual_candidates[best]
        quick_hull(l, chosen, actual_candidates, quick_hull_res)
        quick_hull(chosen, r, actual_candidates, quick_hull_res)

    return quick_hull_res


def left(candidates: List[Point]):
    res = candidates[0]
    for p in candidates:
        if p.x < res.x:
            res = p
    return res


def draw_hull(vertexes: List[Point], canvas: Canvas):
    if len(vertexes) < 2:
        return
    line_values = []
    for p in vertexes:
        line_values.append(p.x)
        line_values.append(p.y)
    canvas.create_line(line_values)


def task1_runner():
    root = Tk()
    root.geometry("1000x800")
    root.resizable(False, False)
    app = SmoothConvex(root)

    root.mainloop()
