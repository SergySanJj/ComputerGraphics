import math
import tkinter as tk
from tkinter import *
from typing import List

from src.misc.point import Point, area, left_most
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
        z = Point(event.x, event.y)
        # if check_if_inside(z, self.hull, self.canv):
        #     self.canv.create_text(200, 200, text="Inside",
        #                           anchor=SE, fill="red", font=("Purisa", 18))
        #     print("Inside")
        # else:
        #     print("Outside")
        #     self.canv.create_text(200, 200, text="Outside",
        #                           anchor=SE, fill="red", font=("Purisa", 18))

    def update_view(self):
        self.canv.delete("all")
        if len(self.vertexes) == 0:
            return
        for p in self.vertexes:
            self.canv.create_oval(p.x - self.diam / 2, p.y - self.diam / 2, p.x + self.diam / 2,
                                  p.y + self.diam / 2, fill=self.point_color,
                                  width=2, outline=self.outline_color)

        l = left_most(self.vertexes)
        r = Point(l.x, l.y - 0.001)
        self.hull = quick_hull(l, r, self.vertexes, [])
        draw_polygon(self.hull, self.canv)

    def on_clear(self):
        self.vertexes = []
        self.update_view()


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
        del actual_candidates[best]
        quick_hull(l, chosen, actual_candidates, quick_hull_res)
        quick_hull_res.append(chosen)
        quick_hull(chosen, r, actual_candidates, quick_hull_res)

    return quick_hull_res


def hull_median(hull: List[Point]) -> Point:
    median: Point = Point(0, 0)
    if len(hull) < 3:
        return median
    for i in range(0, 3):
        p = hull[i]
        median.x += p.x
        median.y += p.y
    median.x = median.x / 3
    median.y = median.y / 3
    return median


# def check_if_inside(z: Point, hull: List[Point], canvas: Canvas) -> bool:
#     median = hull_median(hull)
#     canvas.create_oval(median.x - 5, median.y - 5, median.x + 5, median.y + 5, fill="black",
#                        width=4, outline="green")
#     h = sorted(hull, key=lambda point: point.polar_angle(median))
#     i = 0
#     for p in h:
#         canvas.create_text(p.x, p.y, text=str(i),
#                            anchor=SE, fill="red", font=("Purisa", 18))
#         i += 1
#     return inside_check(z, h, median)


# def inside_check(z: Point, hull: List[Point], median: Point) -> bool:
#     n = len(hull)
#     pq = Point(z.x - hull[0].x, z.y - hull[0].y)
#
#     l = 0
#     r = len(hull)
#     while r - l > 1:
#         mid = (l + r) // 2
#         cur = Point(hull[mid].x - hull[0].x, hull[mid].y - hull[0].y)
#         if cross_product(cur, pq) < 0:
#             r = mid
#         else:
#             l = mid
#     print("found between ", l, r)
#
#     if l == n - 1:
#         return sq_dist(hull[0], z) <= sq_dist(hull[0], hull[l])
#     else:
#         left_vector = Point(hull[l + 1].x - hull[l].x, hull[l + 1].y - hull[l].y)
#         right_vector = Point(z.x - hull[l].x, z.y - hull[l].y)
#     return cross_product(left_vector, right_vector) >= 0


def task5_runner():
    root = Tk()
    root.geometry("1000x800")
    root.resizable(False, False)
    app = SmoothConvex(root)

    root.mainloop()
