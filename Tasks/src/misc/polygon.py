from tkinter import Canvas
from typing import List

from src.misc.point import Point


def draw_polygon(vertexes: List[Point], canvas: Canvas, width=1):
    if len(vertexes) < 2:
        return
    line_values = []
    for p in vertexes:
        line_values.append(p.x)
        line_values.append(p.y)
    p = vertexes[0]
    line_values.append(p.x)
    line_values.append(p.y)
    canvas.create_line(line_values, width=width)
