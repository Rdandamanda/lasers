#!/bin/python3
from tkinter import Tk, Frame, Canvas
from tkinter import ttk
from math import tan, radians

load_debug_screen: bool = True
load_extra_debug_screens: bool = True
debug_level: int = 2

class Segment:
    def __init__(self, start_x: int, start_y: int, degrees: float) -> None:
        self.start_x: int = start_x
        self.start_y: int = start_y
        self.degrees: float = degrees
    def __str__(self) -> str:
        return f"X: {self.start_x} Y: {self.start_y} Angle: {self.degrees}"

class Source:
    def __init__(self, x: int, y: int, degrees: float) -> None:
        self.x: int = x
        self.y: int = y
        self.degrees: int = degrees
        self.generated_segments: list[Segment] = []
    def generate_segments(self, parent_screen: any) -> None:
        self.generated_segments.append(Segment(self.x, self.y, self.degrees))
        for interactor in parent_screen.ray_interactors:
            print(interactor.collide(self)) #TODO: There is nothing here

class Interactor:
    def collide(self, ray_source: Source) -> str:
        return f"Collision of a ray {ray_source} with interactor {self}" #TODO: There is literally nothing here, also this should be a __string__() function

class Glass_Rectangle(Interactor): #TODO: Decide how such objects will be stored
    ...

class Screen:
    ray_sources: list[Source] = []
    ray_interactors: list[Interactor] = []
    def __init__(self, canvas_width: int = 700, canvas_height: int = 400) -> None:
        self.tk_frame: Frame = Frame()
        self.canvas_width: int = canvas_width
        self.canvas_height: int = canvas_height
        self.tk_canvas: Canvas = Canvas(master=self.tk_frame, bg="#DDDDDD", width=self.canvas_width, height=self.canvas_height)
        self.tk_canvas.grid()
    def solve_collisions(self) -> None:
        for source in self.ray_sources:
            source.generate_segments(self)
            #TODO Add some debug print statements maybe
    def draw_all(self) -> None:
        for source in self.ray_sources:
            for segment in source.generated_segments:
                if debug_level >= 2:
                    print(f"Drawing line for segment {segment}")
                    print(f"Tangens = {tan(radians(segment.degrees))}")
                if segment.degrees < 90:
                    end_x: int = self.canvas_width
                end_y: int = segment.start_y + (self.canvas_width-segment.start_x) * tan(radians(segment.angle))
                if segment.degrees == 90:
                    end_x: int = segment.start_x
                    end_y: int = self.canvas_height
                if segment.degrees >= 90 and segment.degrees <= 270:
                    end_x: int = 0
                self.tk_canvas.create_line(segment.start_x, segment.start_y, end_x, end_y, fill="black")

def main() -> None:
    root: Tk = Tk()
    root.title("Ray optics tool")

    ntb_Screens: ttk.Notebook = ttk.Notebook()
    ntb_Screens.grid()

    #The debug screen
    if load_debug_screen == True:
        #Tab setup
        startup_Screen = Screen()
        ntb_Screens.add(startup_Screen.tk_frame, text="Debug Screen")

        #Populating it with objects
        for n in range(15):
            startup_Screen.ray_sources.append(Source(100, 100, 22.5*n))
        #startup_Screen.ray_interactors.append(Glass_Rectangle())
        startup_Screen.solve_collisions()
        startup_Screen.draw_all()

    #Stuff for showing off the tabs. New screens, differentiated by colour. Happy with the high ease of adding them
    if load_extra_debug_screens == True:
        startup_Screen1: Screen = Screen()
        startup_Screen1.tk_canvas.configure(bg="yellow")
        ntb_Screens.add(startup_Screen1.tk_frame, text="Další plocha")
        startup_Screen2: Screen = Screen()
        startup_Screen2.tk_canvas.configure(bg="lavender")
        ntb_Screens.add(startup_Screen2.tk_frame, text="Plocha 3")

    root.mainloop()

if __name__ == "__main__":
    main()
