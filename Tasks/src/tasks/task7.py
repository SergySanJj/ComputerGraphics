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

        draw_polygon(self.vertexes, self.canv)

    def on_clear(self):
        self.vertexes = []
        self.update_view()


def preparata(prevHull: List[Point], newPoint: Point):
    pass
#     n = len(prevHull)
#     if n == 2:
#         second = prevHull[1]
#         second.adj().add(newPoint)
#         newPoint.adj().add(second)
#
#     elif n == 1:
#         first = prevHull[0]
#         first.adj().add(newPoint)
#         newPoint.adj().add(first)
#
#     elif n == 0:
#         prevHull.append(newPoint)
#     else:
#         if getRegion(prevHull, newPoint) is None:
#             left = getSupportingLineNode(newPoint, prevHull, True)
#             right = getSupportingLineNode(newPoint, prevHull, False)
#             removeChainBetween(left, right, prevHull)
#
#             if Edge(left, right).pointIsOnRightSide(newPoint) and len(prevHull) > 2:
#                 left.adj().remove(right)
#                 right.adj().remove(left)
#
#             left.adj().add(newPoint)
#             newPoint.adj().add(left)
#             right.adj().add(newPoint)
#             newPoint.adj().add(right)
#             prevHull.append(newPoint)
#
#
# def getRegion(graph, pointToLocate) :
#         if (len(graph) < 3):
#             return None
#
#         edges = []
#         prevNode = graph[0]
#         currNode = prevNode.adj().iterator().next()
#         nextNode = None
#         edges.append(Edge(prevNode, currNode))
#         while nextNode != graph.get(0):
#             finalPrevNode = prevNode
#             nextNode = currNode.adj().findFirstNotEqal(finalPrevNode)
#             edges.append(Edge(currNode, nextNode))
#             prevNode = currNode
#             currNode = nextNode
#
#
#         leftmost = left_most(graph)
#         farPoint = Point(leftmost.x - 1, pointToLocate.getY())
#         testEdge = Edge(pointToLocate, farPoint)
#
#         counter = 0
#         i = 0
#         while i < len(edges) :
#             if Edge.intersects(testEdge, edges[i]) :
#                 if graph.contains(Node(Edge.getIntersectionPoint(testEdge, edges.get(i)))) :
#                     int prevY = testEdge.getEnd().getY();
#                     testEdge.getEnd().setY(prevY + 1);
#                     counter = 0;
#                     i = 0;
#                     continue;
#                 else :
#                     counter+=1
#
#             i+=1
#
#         if (counter % 2 == 0) :
#             return None;
#
#         return Huller.edgesToPoints(edges);


def task7_runner():
    root = Tk()
    root.geometry("1000x800")
    root.resizable(False, False)
    app = SmoothConvex(root)

    root.mainloop()
