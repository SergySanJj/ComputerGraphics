import math
import tkinter as tk
from random import random, randrange
from tkinter import *
from typing import List

from src.misc.point import Point, area, left_most, eps, sq_dist, cross_product_orientation, left
from src.misc.polygon import draw_polygon

infitous = 10000


class SmoothConvex(Frame):
    diam = 10
    point_color = "black"
    outline_color = ''

    selected = None

    def __init__(self, parent):
        self.vertexes: List[Point] = []
        self.g: Graph = Graph()

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
        self.canv.bind("<Button 2>", self.selection)

        clear_button = Button(self, text="Clear", command=self.on_clear)
        clear_button.grid(row=1, column=1, padx=6, pady=6)

    def on_touch_left(self, event):
        self.vertexes.append(Point(event.x, event.y))
        self.g.append(Node(Point(event.x, event.y)))
        self.update_view()

    def on_touch_right(self, event):
        self.update_view()
        z = Point(event.x, event.y)
        if check_if_inside(z, self.g, self.canv):
            self.canv.create_text(200, 200, text="Inside",
                                  anchor=SE, fill="red", font=("Purisa", 18))
            print("Inside")
        else:
            print("Outside")
            self.canv.create_text(200, 200, text="Outside",
                                  anchor=SE, fill="red", font=("Purisa", 18))

    def selection(self, event):
        prev = self.selected
        self.selected = self.g.select(event.x, event.y)
        if prev is not None and self.selected is not None:
            prev.connect(self.selected)
            self.selected = None
            self.update_view()

    def update_view(self):
        self.canv.delete("all")
        if len(self.vertexes) == 0:
            return
        for p in self.vertexes:
            self.canv.create_oval(p.x - self.diam / 2, p.y - self.diam / 2, p.x + self.diam / 2,
                                  p.y + self.diam / 2, fill=self.point_color,
                                  width=2, outline=self.outline_color)

        self.g.display(self.canv)

    def on_clear(self):
        self.vertexes = []
        self.g.clear()
        self.selected = None
        self.update_view()


class Node:
    def __init__(self, point: Point):
        self.connected: List[Node] = []
        self.point = point
        self.x = point.x
        self.y = point.y

    def connect(self, other):
        self.connected.append(other)
        other.connected.append(self)

    def __eq__(self, other):
        return abs(self.x - other.x) < 1 and abs(self.y - other.y) < 1


class Edge:
    def __init__(self, start: Node, end: Node):
        self.start = start
        self.end = end

    def intersects(self, other):
        if close_by_y(self.start, other.start):
            return Point(self.start.x, self.start.y)
        if close_by_y(self.end, other.end):
            return Point(self.end.x, self.end.y)

        pl = segment_intersect([[self.start.x, self.start.y], [self.end.x, self.end.y]],
                               [[other.start.x, other.start.y], [other.end.x, other.end.y]])
        if pl is not None:
            return Point(pl[0], pl[1])
        else:
            return None


def close_by_y(a, b):
    if abs(a.x - b.x) < eps:
        return True
    return False


def slope(p1, p2):
    return (p2[1] - p1[1]) * 1. / (p2[0] - p1[0])


def y_intercept(slope, p1):
    return p1[1] - 1. * slope * p1[0]


def intersect(line1, line2):
    min_allowed = 1e-5  # guard against overflow
    big_value = 1e10  # use instead (if overflow would have occurred)
    m1 = slope(line1[0], line1[1])
    b1 = y_intercept(m1, line1[0])
    m2 = slope(line2[0], line2[1])
    b2 = y_intercept(m2, line2[0])
    if abs(m1 - m2) < min_allowed:
        x = big_value
    else:
        x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    y2 = m2 * x + b2
    return int(x), int(y)


def segment_intersect(line1, line2):
    intersection_pt = intersect(line1, line2)

    if line1[0][0] < line1[1][0]:
        if intersection_pt[0] < line1[0][0] or intersection_pt[0] > line1[1][0]:
            return None
    else:
        if intersection_pt[0] > line1[0][0] or intersection_pt[0] < line1[1][0]:
            return None

    if line2[0][0] < line2[1][0]:
        if intersection_pt[0] < line2[0][0] or intersection_pt[0] > line2[1][0]:
            return None
    else:
        if intersection_pt[0] > line2[0][0] or intersection_pt[0] < line2[1][0]:
            return None

    return intersection_pt


class Graph:
    def __init__(self):
        self.g: List[Node] = []
        self.stripes: List[List[Edge]] = []

    def append(self, node: Node):
        self.g.append(node)

    def display(self, canvas: Canvas):
        for p in self.g:
            lst = []
            for con in p.connected:
                lst.append(p.x)
                lst.append(p.y)
                lst.append(con.x)
                lst.append(con.y)
            if len(lst) > 3:
                canvas.create_line(lst)

    def sort_y(self):
        self.g = sorted(self.g, key=lambda x: x.y)

    def clear(self):
        self.g = []

    def add_nodes(self, points: List[Point]):
        for p in points:
            self.append(Node(p))

    def select(self, x, y):
        for n in self.g:
            if abs(x - n.x) < 20 and abs(y - n.y) < 20:
                return n
        return None

    def locate_stripe(self, p: Point, canvas: Canvas):
        self.fill_stripes(canvas)

        self.sort_y()
        i = 0
        for n in self.g:
            draw_stripe(n, canvas)
            canvas.create_text(n.x + 20, n.y + 20, text=str(i),
                               anchor=SE, fill="red", font=("Purisa", 14))
            i += 1

        found_pos = self.binary_locate(p)
        draw_stripe(self.g[found_pos], canvas, width=3)
        draw_stripe(self.g[found_pos + 1], canvas, width=3)

        if found_pos == -1:
            return False

        in_sector = find_in_stripe(self.stripes[found_pos], p)

        fill_edges(self.stripes[found_pos][in_sector], self.stripes[found_pos][in_sector + 1], canvas)
        if in_sector > 0:
            return True
        else:
            return False

    def binary_locate(self, p: Point) -> int:
        lp = 0
        rp = len(self.g) - 1
        if p.y < self.g[lp].y or p.y > self.g[rp].y:
            return -1
        else:
            while rp - lp > 1:
                mid = (lp + rp) // 2
                if p.y < self.g[mid].y:
                    rp = mid
                else:
                    lp = mid
            return lp

    def fill_stripes(self, canvas: Canvas):
        self.sort_y()
        self.stripes = []
        for i in range(0, len(self.g) - 1):
            self.stripes.append([Edge(Node(Point(- infitous, self.g[i].y)),
                                      Node(Point(- infitous, self.g[i + 1].y)))])

            edge = Edge(Node(Point(self.g[i].x - infitous, self.g[i].y)),
                        Node(Point(self.g[i].x + infitous, self.g[i].y)))
            edge1 = Edge(Node(Point(self.g[i + 1].x - infitous, self.g[i + 1].y)),
                         Node(Point(self.g[i + 1].x + infitous, self.g[i + 1].y)))

            for pc in self.g:
                for con in pc.connected:
                    e = Edge(pc, con)
                    inter = e.intersects(edge)
                    inter1 = e.intersects(edge1)
                    diam = 5
                    if inter is not None:
                        draw_misc_point(canvas, diam, inter)
                    if inter1 is not None:
                        draw_misc_point(canvas, diam, inter1)

                    if inter is None:
                        if abs(pc.y - self.g[i].y) < eps:
                            inter = Point(pc.x, pc.y)
                    if inter1 is None:
                        if abs(con.y - self.g[i + 1].y) < eps:
                            inter = Point(con.x, con.y)

                    if inter is not None and inter1 is not None:
                        canvas.create_line([inter.x, inter.y, inter1.x, inter1.y], fill="pink", width=3)
                        self.stripes[i].append(Edge(Node(inter), Node(inter1)))

            self.stripes[i].append(
                Edge(Node(Point(+ infitous, self.g[i].y)),
                     Node(Point(+ infitous, self.g[i + 1].y))))

            self.stripes[i].sort(key=lambda e: (e.start.x+e.end.x)/2.)


def draw_misc_point(canvas, diam, point):
    canvas.create_oval(point.x - diam / 2, point.y - diam / 2, point.x + diam / 2,
                       point.y + diam / 2, fill="red",
                       width=2, outline="red")


def fill_edges(e2: Edge, e1: Edge, canvas: Canvas):
    canvas.create_polygon([e1.start.x, e1.start.y, e1.end.x, e1.end.y,
                           e2.end.x, e2.end.y, e2.start.x, e2.start.y], fill="green")


def draw_stripe(p: Node, canvas: Canvas, width=1):
    canvas.create_line([p.x - infitous, p.y, p.x + infitous, p.y], width=width)


def check_if_inside(z: Point, graph: Graph, canvas: Canvas) -> bool:
    return graph.locate_stripe(z, canvas)


def find_in_stripe(stripe: List[Edge], p: Point):
    l_pos = 0
    r_pos = len(stripe) - 1
    while r_pos - l_pos > 1:
        mid = (l_pos + r_pos) // 2
        ls = Point(stripe[l_pos].start.x, stripe[l_pos].start.y)
        le = Point(stripe[l_pos].end.x, stripe[l_pos].end.y)
        l_orient = left(ls, le, p)

        ms = Point(stripe[mid].start.x, stripe[mid].start.y)
        me = Point(stripe[mid].end.x, stripe[mid].end.y)
        m_orient = left(ms, me, p)

        if same_sign(m_orient, l_orient):
            l_pos = mid
        else:
            r_pos = mid

    return l_pos


def brute_stripe(stripe: List[Edge], p: Point):
    print("stripe len", len(stripe))
    i = 0
    while i < len(stripe) - 2:
        ls = Point(stripe[i].start.x, stripe[i].start.y)
        le = Point(stripe[i].end.x, stripe[i].end.y)
        l_orient = left(ls, le, p)

        rs = Point(stripe[i + 1].start.x, stripe[i + 1].start.y)
        r_e = Point(stripe[i + 1].end.x, stripe[i + 1].end.y)
        r_orient = left(rs, r_e, p)

        if not same_sign(l_orient, r_orient):
            return i
        i += 1
    return len(stripe) - 2


def same_sign(a, b):
    if a is True and b is True:
        return True
    elif a is False and b is False:
        return True
    else:
        return False


def task3_runner():
    root = Tk()
    root.geometry("1000x800")
    root.resizable(False, False)
    app = SmoothConvex(root)

    root.mainloop()
