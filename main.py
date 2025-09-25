from tkinter import *
from tkinter import ttk
from math import tan, radians

class Segment:
    def __init__(self, start_x, start_y, angle):
        self.start_x = start_x
        self.start_y = start_y
        self.angle = angle
    def __str__(self):
        return f"X: {self.start_x} Y: {self.start_y} Angle: {self.angle}"

class Source:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.generated_segments = []
    def generate_segments(self, parent_screen):
        self.generated_segments.append(Segment(self.x, self.y, self.angle))
        for interactor in parent_screen.ray_interactors:
            print(interactor.collide(self)) #TODO: There is nothing here

class Interactor:
    def collide(self, ray_source):
        return f"Collision of a ray {ray_source} with interactor {self}" #TODO: There is literally nothing here, also this should be a __string__() function

class Glass_Rectangle(Interactor): #TODO: Decide how such objects will be stored
    pass

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
                if segment.angle < 90:
                    end_x = self.canvas_width
                end_y = segment.start_y + (self.canvas_width-segment.start_x) * tan(radians(segment.angle))
                if segment.angle == 90:
                    end_x = segment.start_x
                    end_y = self.canvas_height
                if segment.angle >= 90 and segment.angle <= 270:
                    end_x = 0
                self.tk_canvas.create_line(segment.start_x, segment.start_y, end_x, end_y, fill="black")

load_debug_screen = True
load_extra_debug_screens = True
debug_level = 2

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
    for n in range(15):
        startup_Screen.ray_sources.append(Source(100, 100, 22.5*n))
    #startup_Screen.ray_interactors.append(Glass_Rectangle())
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