from constants import debug_level, max_segments, colour_intermediate, colour_final

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

class Segment:
    def __init__(self, start_x, start_y, angle):
        self.start_x = start_x
        self.start_y = start_y
        self.angle = angle
    def __str__(self):
        return f"Ray with X: {self.start_x} Y: {self.start_y} Angle: {self.angle}"

class Source:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.generated_segments = []
    def __str__(self):
        return f"Source with X: {self.x} Y: {self.y} Angle: {self.angle}"
    def generate_segments(self, parent_screen) -> None:
        self.generated_segments = [] # TODO: Maybe this is wrong?
        #First segment
        self.generated_segments.append(Segment(self.x, self.y, self.angle))
        #If any collisions, add their segments and solve those
        solving_index = 0
        while solving_index < len(self.generated_segments):
            for interactor in parent_screen.ray_interactors:
                #print(f"Solving index: {solving_index}, len(seg): {len(self.generated_segments)}, sources: {len(parent_screen.ray_sources)}")
                candidate_collisions = interactor.collide(self.generated_segments[solving_index]) #TODO: Enable for this to return a list of new segments
                for collision in candidate_collisions: #TODO: FIX
                    if collision.boolean == True:
                        self.generated_segments.append(collision.segment)
                    if len(self.generated_segments) >= max_segments:
                        solving_index = len(self.generated_segments) #TODO: This is a horrific way to do this
                        break
            solving_index += 1

#Scrapping the idea of making a Collision class. This is the kind of thing that is best kept as a dictionary. A collision object really does not need its own functions or anything. The type checking would still be a good thing though
Collision = namedtuple("Collision", ["boolean", "segment"])

class Interactor:
    def collide(self, ray_source) -> Collision: #Out with {"boolean:bool", "segment:Segment"}!
        return f"Collision of a ray {ray_source} with interactor {self}" #TODO: There is literally nothing here, also this should be a __string__() function

class Screen:
    def __init__(self, canvas_width=700, canvas_height=400):
        #Simulation-related
        self.ray_sources = []
        self.ray_interactors: list[Interactor] = []
        self.canvas_lines = []
        self.canvas_objects = [] # TODO: Temporary! I should just use Canvas tags, remove this

        #UI-related
        self.tk_frame = Frame()
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.tk_canvas = Canvas(master=self.tk_frame, bg="#DDDDDD", width=self.canvas_width, height=self.canvas_height)
        self.tk_canvas.grid()
    def solve_collisions(self):
        for source in self.ray_sources:
            source.generate_segments(self)
            #TODO Add some debug print statements maybe
    def draw_all(self):
        # Delete all canvas objects
        for o in self.canvas_objects:
            self.tk_canvas.delete(o)
        for o in self.canvas_lines:
            self.tk_canvas.delete(o)
        #TODO: Temporary! Remove when fixing everything. Maybe I should use Canvas tags.
        self.canvas_objects = [] #TODO: Temporary! Remove this when fixing everything. Maybe I should use Canvas tags.
        for interactor in self.ray_interactors:
            o = self.tk_canvas.create_rectangle(interactor.x0, interactor.y0, interactor.x1, interactor.y1, fill="#b4d5ff", outline="#92c1ff", width=2)
            self.canvas_objects.append(o)
        for source in self.ray_sources:
            for i_segment in range(len(source.generated_segments)):
                segment = source.generated_segments[i_segment]
                if debug_level >= 2:
                    print(f"Drawing line for segment {segment}")
                    print(f"Tangens = {tan(radians(segment.angle))}")
                #TODO: Make just one case (and maybe edge cases) and use modulo 90° and 
                if segment.angle >= 360:
                    if debug_level >= 1:
                        print(f"WARN: Segment's angle is high: {segment.angle}")
                if i_segment < len(source.generated_segments) - 1: #The not-ending lines
                    next_segment = source.generated_segments[i_segment + 1]
                    line = self.tk_canvas.create_line(segment.start_x, segment.start_y, next_segment.start_x, next_segment.start_y, fill=colour_intermediate)
                    self.canvas_lines.append(line)
                    if debug_level >= 2:
                        print(f"Creating line to X: {next_segment.start_x} Y: {next_segment.start_y}")
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
                if debug_level >= 2:
                    print(f"Creating line to X: {end_x} Y: {end_y}")
                line = self.tk_canvas.create_line(segment.start_x, segment.start_y, end_x, end_y, fill=colour_final)
                self.canvas_lines.append(line)
                #self.tk_canvas.create_line(300, 100, 0, 100, fill="black")
