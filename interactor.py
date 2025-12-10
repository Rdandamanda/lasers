from source import Source
from math import pi, sin, asin, cos, acos
from random import randint
from tkinter import Tk, Frame, Canvas, ttk
class Interactor:
    def __init__(self, left: int, top: int, right: int, bottom: int, refractive_index: float, fill: str = "#9bc8d1", outline: str = "#aad9e3", border_width: int = 2) -> None:
        self._left = left
        self._top = top
        self._right = right
        self._bottom = bottom
        self._index = refractive_index
        self._fill = fill
        self._outline = outline
        self._border_width = border_width

    def draw(self, canvas: Canvas) -> None:
        canvas.create_rectangle(self._left, self._bottom, self._right, self._top, fill=self._fill, outline=self._outline, width=self._border_width)

    def collision_check(self, source: Source) -> tuple[int, int] | None:
        return source.collide_box(self._left, self._top, self._right, self._bottom)

    def collide(self, source: Source, x: int, y: int) -> list[Source]:
        if source._depth <= 1:
            return []
        ray_angle = source._angle * (pi / 180)
        wall_antinormal = pi if x == self._right else (3/ 2) * pi if y == self._bottom else 0 if x == self._left else (pi / 2)
        alpha = (ray_angle - wall_antinormal) % (2 * pi)
        if alpha <= (3 / 2) * pi and alpha >= pi / 2:
            try:
                wall_antinormal = (wall_antinormal + pi) % (2 * pi)
                alpha = (ray_angle - wall_antinormal) % (2 * pi)
                beta = asin(sin(alpha) * self._index)
            except ValueError as e:
                if str(e) != 'math domain error':
                    raise e
                beta = (pi - alpha) % (2 * pi)
                final_angle = ((beta + wall_antinormal) * (180 / pi)) % 360
                return [Source(x, y, source._angle, source._color, source._depth  - 1)]
        else:
            beta = asin(sin(alpha) / self._index)
        final_angle = ((beta + wall_antinormal) * (180 / pi)) % 360
        return [Source(x, y, final_angle, source._color, source._depth  - 1)]

class Mirror(Interactor):
    def __init__(self, left: int, top: int, right: int, bottom: int, fill: str = "#9bc8a1", outline: str = "#aad9e3", border_width: int = 2) -> None:
        super().__init__(left, top, right, bottom, 0, fill, outline, border_width)

    def collide(self, source: Source, x: int, y: int) -> list[Source]:
        if source._depth <= 1:
            return []
        ray_angle = source._angle * (pi / 180)
        wall_antinormal = 0 if x == self._right else (1 / 2) * pi if y == self._bottom else pi if x == self._left else (3 / 2) * pi
        alpha = (ray_angle - wall_antinormal) % (2 * pi)
        beta = (pi - alpha) % (2 * pi)
        final_angle = ((beta + wall_antinormal) * (180 / pi)) % 360
        return [Source(x, y, final_angle, source._color, source._depth  - 1)]

