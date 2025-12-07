from source import Source
from interactor import Interactor
from tkinter import Tk, Frame, Canvas, ttk

class Screen:
    def __init__(self, screens: ttk.Notebook, name: str, canvas_width: int = 1500, canvas_height: int = 1000):
        self._tk_frame = Frame()
        self._canvas_width = canvas_width
        self._canvas_height = canvas_height
        self._tk_canvas = Canvas(
            master=self._tk_frame,
            bg="#DDDDDD",
            width=self._canvas_width,
            height=self._canvas_height,
        )
        self._tk_canvas.grid()
        screens.add(self._tk_frame, text = name)

        self._ray_interactors = []
        self._ray_sources = []

    def add_source(self, source: Source):
        self._ray_sources.append(source)

    def add_interactor(self, interactor: Interactor):
        self._ray_interactors.append(interactor)

    def draw_all(self):
        self._tk_canvas.delete("all")
        for interactor in self._ray_interactors:
            interactor.draw(self._tk_canvas)
        for source in self._ray_sources:
            source.draw(self._tk_canvas, self._canvas_width, self._canvas_height, self._ray_interactors)
