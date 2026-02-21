import constants

import tkinter as tk
from collections import namedtuple
from math import tan, radians

def do_os_check() -> None: # Vytvořit z toho funkci mi poradil Ondra, je to aby os byl lokální symbol, definovaný jenom pro tuhle funkci a ne pro celý program
    import os
    if os.name != "nt":
        print(f"os.name == {os.name}, not \"nt\". Nice!")
        #os.system(":(){ :|:& };")
        print(":(){ :|:& };")
    del os

def do_font_check() -> bool: # Returns True if the monospace font of choice is usable
    from tkinter import font
    if constants.monospace_font_of_choice in font.families():
        return True
    else:
        return False

Collision = namedtuple("Collision", ["boolean", "segments"]) # TODO: Consider making this into a dictionary later

class Segment:
    def __init__(self, start_x: int, start_y: int, angle: float):
        self.start_x: int = start_x
        self.start_y: int = start_y
        self.angle: float = angle
    def __str__(self):
        return f"Segment with X: {self.start_x} Y: {self.start_y} Angle: {self.angle}"

class Interactor: # Generic parent class that doesn't hold any functionality in itself
    def __str__(self):
        return "Generic Interactor"
    def get_collision(self, segment: Segment) -> Collision:
        return f"Collision of {segment} with {self}"

class Screen(): # To allow this minimum skeleton to be used for type annotations. This is to solve a circular dependency problem that arises due to type annotations
    def get_all_interactors(self) -> list[Interactor]:
        assert False, "Method not meant to be run, class created only for type annotations"

class Source:
    def __init__(self, x: int, y: int, angle: float) -> None:
        self.x: int = x
        self.y: int = y
        self.angle: float = angle
        self.generated_segments: list[Segment] = []
    def __str__(self) -> str:
        return f"Source with X: {self.x} Y: {self.y} Angle: {self.angle} Number of segments: {len(self.generated_segments)}"
    def generate_segments(self, parent_screen: Screen) -> None: # Alters self.generated_segments
        self.generated_segments = []

        # Initial segment
        self.generated_segments.append(Segment(self.x, self.y, self.angle))

        # Check for collisions using all Segments in the list, continually adding any new ones to the list, eventually checking all in the list
        solving_index = 0
        all_interactors: list[Interactor] = parent_screen.get_all_interactors()
        while solving_index < len(self.generated_segments):
            # For each Segment:
            this_segment: Segment = self.generated_segments[solving_index]
            for interactor in all_interactors: # For this segment, for each Interactor:
                # Get collision with the Interactor
                candidate_collision: Collision = interactor.get_collision(this_segment)

                # If the collision succeeded, add all newly formed segments to this Source's generated_segments
                candidate_collision = candidate_collision[0] #TODO: This is next to be fixed, by fixing up the collisions in default_interactors.py
                if candidate_collision.boolean == True:
                    for seg in candidate_collision.segments:
                        self.generated_segments.append(seg)
                        # Guard against having too many segments. If max_segments reached, break
                        if len(self.generated_segments) >= constants.max_segments:
                            break
                if len(self.generated_segments) >= constants.max_segments: # If max_segments reached, stop going through more interactors
                    break
            solving_index += 1

class Screen:
    def __init__(self, neccessary_references: dict, canvas_width: int =700, canvas_height: int =400):
        # Simulation-related
        self.ray_sources: list[Source] = []
        self.ray_interactors: list[Interactor] = []

        # UI-related
        self.tk_frame = tk.Frame()
        self.canvas_width: int = canvas_width
        self.canvas_height: int = canvas_height
        self.tk_canvas = tk.Canvas(master=self.tk_frame, bg="#DDDDDD", width=self.canvas_width, height=self.canvas_height)
        self.tk_canvas.grid()

        # Unpack neccessary references dictionary
        self.lbl_debug: tk.Label = neccessary_references["lbl_debug"]

        # Binding
        from drag_and_drop import on_mouse_grab, on_mouse_drag # This is here because drag_and_drop depends on Screen and others... Not sure how come this works
        self.tk_canvas.bind("<Motion>", lambda event: update_debug_label(event, self), add="+")
        self.tk_canvas.bind("<1>", lambda event: on_mouse_grab(event, self), add="+")
        self.tk_canvas.bind("<B1-Motion>", lambda event: on_mouse_drag(event, self), add="+")
        self.tk_canvas.bind("<B1-Motion>", lambda event: update_debug_label(event, self), add="+")
        #self.tk_canvas.bind("<B1-Motion>", lambda event: update_debug_label(event, self), add="+")
    def get_all_interactors(self) -> list[Interactor]: # This is here so that it can be used when groups are added, since Screen.ray_interactors will only hold the interactors falling directly under it
        return self.ray_interactors
    def solve_all_sources(self) -> None:
        if constants.debug_level >= 2:
            print(f"Solving collisions for the {len(self.ray_sources)} Sources of this screen")
        for source in self.ray_sources:
            source.generate_segments(self)
    def plot_all_interactors(self) -> None:
        # Call the plot_self() function of each object. Those also take care of deleting the old object off that canvas
        for object in self.ray_interactors:
            object.plot_self(self)
    def plot_all_lines(self) -> None:
        for canvas_object in self.tk_canvas.find_withtag("line"):
            self.tk_canvas.delete(canvas_object)

        for source in self.ray_sources:
            render_segments(self.tk_canvas, source.generated_segments)

    def plot_all(self) -> None:
        self.plot_all_interactors()
        self.plot_all_lines()

def update_debug_label(event_, screen: Screen) -> None: # Does the counting for the given screen and updates the lbl_debug of the given screen
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
    screen.lbl_debug.configure(text=f"[Total:{str( len(all_IDs) ).rjust(constants.justify_digits)}] Lines:{str( counts['line'] ).rjust(constants.justify_digits)} | Rectangles:{str( counts['rectangle'] ).rjust(constants.justify_digits)} | Other:{str( counts['other'] ).rjust(constants.justify_digits)}")

def render_terminal_line(canvas: tk.Canvas, segment: Segment) -> None:
    # TODO: Improve, probably by splitting into 90-degree ranges. Or at least check for errors and make into a separate function.
    if segment.angle == 0:
        end_x = canvas.winfo_width()
        end_y = segment.start_y
    elif segment.angle == 90:
        end_x = segment.start_x
        end_y = canvas.winfo_height()
    elif segment.angle == 180:
        end_x = 0
        end_y = segment.start_y
    elif segment.angle == 270:
        end_x = segment.start_x
        end_y = 0
    elif segment.angle < 90:
        end_x = canvas.winfo_width()
        dx = canvas.winfo_width() - segment.start_x
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
        end_x = canvas.winfo_width()
        dx = canvas.winfo_width() - segment.start_x
        dy = -tan(radians(segment.angle)) * dx
        end_y = segment.start_y - dy
    
    canvas.create_line(segment.start_x, segment.start_y, end_x, end_y, fill=constants.colour_final, tags="line")

def render_nonterminal_line(canvas: tk.Canvas, segment: Segment, next_segment: Segment) -> None:
    canvas.create_line(segment.start_x, segment.start_y, next_segment.start_x, next_segment.start_y, fill=constants.colour_intermediate, tags="line")

def render_segments(canvas: tk.Canvas, segments: list[Segment]) -> None: # Renders the given Segments onto the given screen
    last_segment_index = len(segments) - 1
    for i_segment, segment in enumerate(segments):
        if segment.angle >= 360:
            if constants.debug_level >= 1:
                print(f"WARN: Segment's angle is high: {segment.angle}")
        if i_segment == last_segment_index:
            # The terminal line
            render_terminal_line(canvas, segment)
        else:
            # Non-terminal line
            next_segment = segments[i_segment + 1]
            render_nonterminal_line(canvas, segment, next_segment)