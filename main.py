from tkinter import *
from tkinter import ttk
from math import tan, radians
from random import randint

#Better would be to make this a function and import os inside, making it a local symbol
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
    def generate_segments(self, parent_screen):
        #First segment
        self.generated_segments.append(Segment(self.x, self.y, self.angle))
        #If any collisions, add their segments
        for interactor in parent_screen.ray_interactors:
            print(interactor.collide(self.generated_segments[0])) #Give the first segment, for now #TODO: There is nothing here

class Interactor:
    def collide(self, ray_source) -> tuple[bool, int, int]:
        return (True, randint(0, 100), randint(0, 100))
        return f"Collision of a ray {ray_source} with interactor {self}" #TODO: There is literally nothing here, also this should be a __string__() function

class Glass_Rectangle(Interactor): #TODO: Decide how such objects will be stored
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
    def __str__(self):
        return "Glass Rectangle"
    def collide(self, ray_source) -> tuple[bool, int, int]:

        return (True, randint(0, 100), randint(0, 1)) #(isCollided, x, y)

class Screen:
    ray_sources = []
    ray_interactors = []
    def __init__(self, canvas_width=700, canvas_height=400):
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
        for source in self.ray_sources:
            for segment in source.generated_segments:
                if debug_level >= 2:
                    print(f"Drawing line for segment {segment}")
                    print(f"Tangens = {tan(radians(segment.angle))}")
                #TODO: Make just one case (and maybe edge cases) and use modulo 90° and 
                if segment.angle >= 360:
                    if debug_level >= 1:
                        print(f"WARN: Segment's angle is high: {segment.angle}")
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
                self.tk_canvas.create_line(segment.start_x, segment.start_y, end_x, end_y, fill="blue")
                #self.tk_canvas.create_line(300, 100, 0, 100, fill="black")
        for interactor in self.ray_interactors:
            self.tk_canvas.create_rectangle(interactor.x0, interactor.y0, interactor.x1, interactor.y1, fill="#9bc8d1", outline="#aad9e3", width=2)

load_debug_screen = True
load_extra_debug_screens = True
debug_level = 1

root = Tk()
root.title("Ray optics tool")

ntb_Screens = ttk.Notebook()
ntb_Screens.grid()

#The debug screen
if load_debug_screen == True:
    #Tab setup
    startup_Screen = Screen()
    ntb_Screens.add(startup_Screen.tk_frame, text="Debug Screen")

    #Populating it with objects
    for n in range(16):
        startup_Screen.ray_sources.append(Source(300, 140, (180+22.5*n)%360))
    startup_Screen.ray_interactors.append(Glass_Rectangle(200, 200, 500, 400))

    #Solve and draw
    startup_Screen.solve_collisions()
    startup_Screen.draw_all()

#Stuff for showing off the tabs. New screens, differentiated by colour. Happy with the high ease of adding them
if load_extra_debug_screens == True:
    startup_Screen1 = Screen()
    startup_Screen1.tk_canvas.configure(bg="yellow")
    ntb_Screens.add(startup_Screen1.tk_frame, text="Další plocha")
    startup_Screen2 = Screen()
    startup_Screen2.tk_canvas.configure(bg="lavender")
    ntb_Screens.add(startup_Screen2.tk_frame, text="Plocha 3")

root.mainloop()
