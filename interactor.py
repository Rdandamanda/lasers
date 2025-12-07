from source import Source
from math import pi, tan, atan
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
        canvas.create_rectangle(self._left, self._top, self._right, self._bottom, fill=self._fill, outline=self._outline, width=self._border_width)

    def collision_check(self, source: Source) -> tuple[int, int] | None:
        return source.collide_box(self._left, self._top, self._right, self._bottom)

    def collide(self, source: Source, x: int, y: int) -> list[Source]:
        if source._depth <= 1:
            return []
        return [Source(x, y, source._angle + randint(-10, 10), source._color, source._depth - 1) for _ in range(2)]
