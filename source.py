from math import pi, cos, sin
from tkinter import Tk, Frame, Canvas, ttk


class Source:
    def __init__(self, x: int, y: int, angle: float, color: str = "red", depth: int = 8) -> None:
        self._x = x
        self._y = y
        self._angle = angle
        self._color = color
        self._depth = depth
        self._next = []

    def collide_vertical(self, x: int, top: int, bottom: int) -> int | None:
        try:
            angle = self._angle * (pi / 180)
            t = (x - self._x) / cos(angle)
            if t <= 0:
                return None
            c_y = self._y + t * sin(angle)
            if c_y >= top and c_y <= bottom:
                return c_y
        except ZeroDivisionError:
            pass
        return None

    def collide_horizontal(self, y: int, left: int, right: int) -> int | None:
        try:
            angle = self._angle * (pi / 180)
            t = (y - self._y) / sin(angle)
            if t <= 0:
                return None
            c_x = self._x + t * cos(angle)
            if c_x >= left and c_x <= right:
                return c_x
        except ZeroDivisionError:
            pass
        return None

    def collide_box(self, left: int, top: int, right: int, bottom: int) -> tuple[int, int] | None:
        tests = [
            (left, self.collide_vertical(left, top, bottom)),
            (right, self.collide_vertical(right, top, bottom)),
            (self.collide_horizontal(top, left, right), top),
            (self.collide_horizontal(bottom, left, right), bottom),
            ]
        tests = [test for test in tests if test[0] is not None and test[1] is not None]
        if len(tests) == 0:
            return None
        return min(tests, key = lambda e: (e[0] - self._x) ** 2 + (e[1] - self._y) ** 2)

    def draw(self, canvas: Canvas, container_width: int, container_height: int, interactors: list) -> None:
        possible_collisions = [
            (collision, interactor)
            for interactor in interactors
            if (collision := interactor.collision_check(self)) is not None
        ]
        if len(possible_collisions) == 0:
            test = self.collide_box(0, 0, container_width, container_height)
            if test is not None:
                canvas.create_line(self._x, self._y, test[0], test[1], fill=self._color, width=self._depth)
            return
        collision_point = min(possible_collisions, key = lambda e: e[0][0] ** 2 + e[0][1] ** 2)
        canvas.create_line(self._x, self._y, collision_point[0][0], collision_point[0][1], fill=self._color, width=self._depth)
        self._next = collision_point[1].collide(self, collision_point[0][0], collision_point[0][1])
        for ray in self._next:
            ray.draw(canvas, container_width, container_height, interactors)
