from constants import debug_level, max_segments, colour_intermediate, colour_final, justify_digits, monospace_font_of_choice

from tkinter import *
from tkinter import ttk
from collections import namedtuple
from math import tan, radians

# Vytvořit z toho funkci mi poradil Ondra, je to aby os byl lokální symbol, definovaný jenom pro tuhle funkci a ne pro celý program
def do_os_check() -> None:
    import os
    if os.name != "nt":
        print(f"os.name == {os.name}, not \"nt\". Nice!")
        #os.system(":(){ :|:& };")
        print(":(){ :|:& };")
    del os

def do_font_check() -> bool: # Returns True if the monospace font of choice is usable
    from tkinter import font
    if monospace_font_of_choice in font.families():
        return True
    else:
        return False

def update_debug_label(event_, screen):
    # Count objects and their types
    all_IDs = screen.tk_canvas.find_all()
    counts: dict = {"line": 0, "rectangle": 0, "other": 0}
    for object_ID in all_IDs:
        object_type = screen.tk_canvas.type(object_ID)
        match object_type:
            case "line":
                counts["line"] += 1
            case "rectangle":
                counts["rectangle"] += 1
            case _:
                counts["other"] += 1

    # Update the text on the Label
    screen.lbl_debug.configure(text=f"[Total:{str( len(all_IDs) ).rjust(justify_digits)}] Lines:{str( counts['line'] ).rjust(justify_digits)} | Rectangles:{str( counts['rectangle'] ).rjust(justify_digits)} | Other:{str( counts['other'] ).rjust(justify_digits)}")

class Segment:
    def __init__(self, start_x, start_y, angle):
        self.start_x = start_x
        self.start_y = start_y
        self.angle = angle
    def __str__(self):
        return f"Segment with X: {self.start_x} Y: {self.start_y} Angle: {self.angle}"

class Source:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.generated_segments = []
    def __str__(self):
        return f"Source with X: {self.x} Y: {self.y} Angle: {self.angle} Number of segments: {len(self.generated_segments)}"
    def generate_segments(self, parent_screen) -> None: # TODO: Unable to give a type annotation for parent_screen, because Source and Screen cyclically depend on the other... maybe I can move generate_segments out and make it a seperate function, but that doesn't sound like a proper fix
        self.generated_segments = []
        # Initial segment
        self.generated_segments.append(Segment(self.x, self.y, self.angle))
        # If any collisions, add their segments and solve those
        solving_index = 0
        while solving_index < len(self.generated_segments):
            for interactor in parent_screen.get_all_interactors():
                #print(f"Solving index: {solving_index}, len(seg): {len(self.generated_segments)}, sources: {len(parent_screen.ray_sources)}")
                candidate_collisions = interactor.collide(self.generated_segments[solving_index])
                for collision in candidate_collisions:
                    if collision.boolean == True:
                        for seg in collision.segments:
                            self.generated_segments.append(seg)
                    if len(self.generated_segments) >= max_segments:
                        break
            if len(self.generated_segments) >= max_segments:
                break
            solving_index += 1

#Scrapping the idea of making a Collision class. This is the kind of thing that is best kept as a dictionary. A collision object really does not need its own functions or anything. The type checking would still be a good thing though
Collision = namedtuple("Collision", ["boolean", "segments"])

class Interactor:
    def __str__(self):
        return "Generic Interactor"
    def collide(self, segment: Segment) -> Collision:
        return f"Collision of {segment} with {self}"

class Screen:
    def __init__(self, neccessary_references: dict, canvas_width: int =700, canvas_height: int =400):
        # Simulation-related
        self.ray_sources: list[Source] = []
        self.ray_interactors: list[Interactor] = []
        self.canvas_lines = []
        self.canvas_objects = [] # TODO: Temporary! I should just use Canvas tags, remove this

        # UI-related
        self.tk_frame = Frame()
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.tk_canvas = Canvas(master=self.tk_frame, bg="#DDDDDD", width=self.canvas_width, height=self.canvas_height)
        self.tk_canvas.grid()

        # Unpack neccessary references dictionary
        self.lbl_debug: Label = neccessary_references["lbl_debug"]

        # Binding
        from drag_and_drop import on_mouse_grab, on_mouse_drag
        self.tk_canvas.bind("<Motion>", lambda event: update_debug_label(event, self))
        self.tk_canvas.bind("<1>", lambda event: on_mouse_grab(event, self))
        self.tk_canvas.bind("<B1-Motion>", lambda event: on_mouse_drag(event, self))
    def get_all_interactors(self) -> list[Interactor]:
        return self.ray_interactors
    def solve_collisions(self) -> None:
        if debug_level >= 2:
            print(f"Solving collisions for the {len(self.ray_sources)} Sources of this screen")
        for source in self.ray_sources:
            source.generate_segments(self)
    def plot_all_interactors(self) -> None:
        # Call the plot_self() function of each object. Those also take care of deleting the old object off that canvas
        for object in self.ray_interactors:
            object.plot_self(self)
    def plot_all_lines(self) -> None:
        for line in self.canvas_lines:
            self.tk_canvas.delete(line)

        for source in self.ray_sources: # TODO: Improve, probably by splitting into 90-degree ranges. Or at least check for errors and make into a separate function.
            for i_segment in range(len(source.generated_segments)):
                segment = source.generated_segments[i_segment]
                #TODO: Make just one case (and maybe edge cases) and use modulo 90° and 
                if segment.angle >= 360:
                    if debug_level >= 1:
                        print(f"WARN: Segment's angle is high: {segment.angle}")
                if i_segment < len(source.generated_segments) - 1: #The not-ending lines
                    next_segment = source.generated_segments[i_segment + 1]
                    line = self.tk_canvas.create_line(segment.start_x, segment.start_y, next_segment.start_x, next_segment.start_y, fill=colour_intermediate)
                    self.canvas_lines.append(line)
                    continue
                if segment.angle == 0:
                    end_x = self.canvas_width
                    end_y = segment.start_y
                elif segment.angle == 90:
                    end_x = segment.start_x
                    end_y = self.canvas_height
                elif segment.angle == 180:
                    end_x = 0
                    end_y = segment.start_y
                elif segment.angle == 270:
                    end_x = segment.start_x
                    end_y = 0
                elif segment.angle < 90:
                    end_x = self.canvas_width
                    dx = self.canvas_width - segment.start_x
                    dy = tan(radians(segment.angle)) * dx
                    end_y = segment.start_y + dy
                elif segment.angle < 180:
                    end_x = 0
                    dx = segment.start_x
                    dy = -tan(radians(segment.angle)) * dx
                    end_y = segment.start_y + dy
                elif segment.angle < 270:
                    end_x = 0
                    dx = segment.start_x
                    dy = tan(radians(segment.angle)) * dx
                    end_y = segment.start_y - dy
                elif segment.angle < 360:
                    end_x = self.canvas_width
                    dx = self.canvas_width - segment.start_x
                    dy = -tan(radians(segment.angle)) * dx
                    end_y = segment.start_y - dy
                line = self.tk_canvas.create_line(segment.start_x, segment.start_y, end_x, end_y, fill=colour_final)
                self.canvas_lines.append(line)
                #self.tk_canvas.create_line(300, 100, 0, 100, fill="black")

    def plot_all(self) -> None:
        self.plot_all_interactors()
        self.plot_all_lines