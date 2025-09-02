from tkinter import *
from tkinter import ttk

class Source:
    def __init__(self):
        self.generated_segments = []
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
    def __init__(self):
        self.tk_frame = Frame()
        self.tk_canvas = Canvas(master=self.tk_frame, bg="#DDDDDD", width=700, height=400)
        self.tk_canvas.grid()
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

#The debug screen
if load_debug_screen == True:
    startup_Screen = Screen()
    ntb_Screens.add(startup_Screen.tk_frame, text="Debug Screen")
    startup_Screen1 = Screen()
    startup_Screen1.tk_canvas.configure(bg="yellow")
    ntb_Screens.add(startup_Screen1.tk_frame, text="Další plocha")
    startup_Screen2 = Screen()
    startup_Screen2.tk_canvas.configure(bg="lavender")
    ntb_Screens.add(startup_Screen2.tk_frame, text="Plocha 3")

#startup_Screen.ray_sources.append(Source())
#startup_Screen.ray_interactors.append(Glass_Rectangle())
#startup_Screen.solve_collisions()
#startup_Screen.draw_all()

root.mainloop()