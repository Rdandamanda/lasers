from tkinter import *
from tkinter import ttk

class Source:
    generated_segments = []
    def generate_segments(self, parent_screen):
        for interactor in parent_screen.ray_interactors:
            print(interactor.collide())

class Interactor:
    def collide(self, ray_source):
        return f"Collision of a ray {ray_source} with interactor {self}"

class Glass_Rectangle(Interactor):
    pass

class Screen:
    ray_sources = []
    ray_interactors = []
    tk_frame = Frame()
    tk_canvas = Canvas(master=tk_frame, bg="red", width=20, height=20) #TODO: is this going to be class-wide or per-instance?
    def __init__(self):
        pass
    def solve_collisions(self):
        for source in self.ray_sources:
            return f"solve collision for source {source}"
    def draw_all(self):
        pass

load_debug_screen = True

root = Tk()
root.title("Laser visualiser tool")

ntb_Screens = ttk.Notebook()
ntb_Screens.grid()

if load_debug_screen == True:
    pass
    #startup_Screen = Screen()
    #ntb_Screens.add(startup_Screen.tk_frame, text="Debug Screen")

#startup_Screen.ray_sources.append(Source())
#startup_Screen.ray_interactors.append(Glass_Rectangle())
#startup_Screen.solve_collisions()
#startup_Screen.draw_all()

root.mainloop()