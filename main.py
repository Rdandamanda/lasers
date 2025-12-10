
from tkinter import *
from tkinter import ttk
from math import tan, radians, asin, degrees, sin
from collections import namedtuple

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
    def generate_segments(self, parent_screen) -> None:
        #First segment
        self.generated_segments.append(Segment(self.x, self.y, self.angle))
        #If any collisions, add their segments and solve those
        solving_index = 0
        while solving_index < len(self.generated_segments):
            for interactor in parent_screen.ray_interactors:
                candidate_collisions = interactor.collide(self.generated_segments[solving_index]) #TODO: Enable for this to return a list of new segments
                for collision in candidate_collisions: #TODO: FIX
                    if collision.boolean == True:
                        self.generated_segments.append(collision.segment)
                    if len(self.generated_segments) >= max_segments:
                        solving_index = len(self.generated_segments) #TODO: This is a horrific way to do this
            solving_index += 1

#Scrapping the idea of making a Collision class. This is the kind of thing that is best kept as a dictionary. A collision object really does not need its own functions or anything. The type checking would still be a good thing though

Collision = namedtuple("Collision", ["boolean", "segment"])

class Interactor:
    def collide(self, ray_source) -> Collision: #Out with {"boolean:bool", "segment:Segment"}!
        return f"Collision of a ray {ray_source} with interactor {self}" #TODO: There is literally nothing here, also this should be a __string__() function

class Glass_Rectangle(Interactor): #TODO: Decide how such objects will be stored
    def __init__(self, x0, y0, x1, y1):
        if x0 >= x1 or y0 >= y1:
            raise Exception("Wrong order or the same")
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
    def __str__(self):
        return "Glass Rectangle"
    def collide(self, ray: Segment) -> list[tuple[bool, int, int]]:
        return_list = []
        if ray.angle == 90:
            if self.x0 <= ray.start_x and ray.start_x <= self.x1 and ray.start_y < self.y0:
                return_list.append(Collision(boolean=True, segment=Segment(angle=270, start_x=ray.start_x, start_y=self.y0)))
        elif ray.angle == 270:
            if self.x0 <= ray.start_x and ray.start_x <= self.x1 and ray.start_y > self.y1:
                return_list.append(Collision(boolean=True, segment=Segment(angle=90, start_x=ray.start_x, start_y=self.y1)))
        elif ray.angle == 180:
            if self.y0 <= ray.start_y and ray.start_y <= self.y1 and ray.start_x > self.x1:
                return_list.append(Collision(boolean=True, segment=Segment(angle=0, start_x=self.x1, start_y=ray.start_y)))
        elif ray.angle == 0:
            if self.y0 <= ray.start_y and ray.start_y <= self.y1 and ray.start_x < self.x0:
                return_list.append(Collision(boolean=True, segment=Segment(angle=180, start_x=self.x0, start_y=ray.start_y)))
        elif ray.angle < 90:
            # Collide with horizontal line:
            dy = self.y0 - ray.start_y
            if dy > 0:
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, 360 - ray.angle)))
            # Collide with vertical line:
            dx = self.x0 - ray.start_x
            if dx > 0:
                dy = tan(radians(ray.angle)) * dx
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.y0 < potential_endy and potential_endy < self.y1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, 180 - ray.angle)))
        elif ray.angle < 180:
            # Collide with horizontal line:
            dy = self.y0 - ray.start_y
            if dy > 0:
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, 360 - ray.angle)))
            # Collide with vertical line:
            dx = self.x1 - ray.start_x
            if dx < 0:
                dy = tan(radians(ray.angle)) * dx
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.y0 < potential_endy and potential_endy < self.y1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, 180 - ray.angle)))
        elif ray.angle < 270:
            # Collide with horizontal line:
            dy = self.y1 - ray.start_y
            if dy < 0:
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, 360 - ray.angle)))
            # Collide with vertical line:
            dx = self.x1 - ray.start_x
            if dx < 0:
                dy = tan(radians(ray.angle)) * dx
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.y0 < potential_endy and potential_endy < self.y1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, 180 - ray.angle)))
        elif ray.angle < 360:
            # Collide with horizontal line:
            dy = self.y1 - ray.start_y
            if dy < 0:
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, 360 - ray.angle)))
            # Collide with vertical line:
            dx = self.x0 - ray.start_x
            if dx > 0:
                dy = tan(radians(ray.angle)) * dx
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.y0 < potential_endy and potential_endy < self.y1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, 540 - ray.angle)))

        else:
            #raise Exception("Angle unhandled")
            print("angle not handled")
            return_list.append(Collision(False, None))

        for collision in return_list:
            if collision.boolean == False:
                continue
            if (collision.segment.start_x == ray.start_x and collision.segment.start_y == ray.start_y):
                return_list.remove(collision) #TODO: This is intentionally cursed, remove as soon as feeling like it
        
        if len(return_list) == 0:
            return [Collision(False, None)]
        else:
            return return_list

class Screen:
    def __init__(self, canvas_width=700, canvas_height=400):
        #Simulation-related
        self.ray_sources = []
        self.ray_interactors: list[Interactor] = []
        self.canvas_lines = []

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
        for interactor in self.ray_interactors:
            self.tk_canvas.create_rectangle(interactor.x0, interactor.y0, interactor.x1, interactor.y1, fill="#b4d5ff", outline="#92c1ff", width=2)
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
                    line = self.tk_canvas.create_line(segment.start_x, segment.start_y, next_segment.start_x, next_segment.start_y, fill="blue")
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
                line = self.tk_canvas.create_line(segment.start_x, segment.start_y, end_x, end_y, fill="#5e58ff")
                self.canvas_lines.append(line)
                #self.tk_canvas.create_line(300, 100, 0, 100, fill="black")
                
def snell_in(angle) -> float:
    # sin(beta) = sin(alpha) / ratio
    return degrees( asin(sin(radians(angle)) / 1.5) )
def snell_out(angle) -> float:
    # sin(beta) = sin(alpha) / ratio
    return degrees( asin(sin(radians(angle)) * 1.5) )

class Refraction_Rectangle(Interactor): #TODO: What the hell was I doing here
    def __init__(self, x0, y0, x1, y1):
        if x0 >= x1 or y0 >= y1:
            raise Exception("Wrong order or the same")
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
    def __str__(self):
        return "Refractive Rectangle"
    def collide(self, ray: Segment) -> list[tuple[bool, int, int]]:
        return_list = []
        if ray.angle == 90:
            if self.x0 <= ray.start_x and ray.start_x <= self.x1 and ray.start_y < self.y0:
                return_list.append(Collision(boolean=True, segment=Segment(angle=90, start_x=ray.start_x, start_y=self.y0)))
        elif ray.angle == 270:
            if self.x0 <= ray.start_x and ray.start_x <= self.x1 and ray.start_y > self.y1:
                return_list.append(Collision(boolean=True, segment=Segment(angle=270, start_x=ray.start_x, start_y=self.y1)))
        elif ray.angle == 180:
            if self.y0 <= ray.start_y and ray.start_y <= self.y1 and ray.start_x > self.x1:
                return_list.append(Collision(boolean=True, segment=Segment(angle=180, start_x=self.x1, start_y=ray.start_y)))
        elif ray.angle == 0:
            if self.y0 <= ray.start_y and ray.start_y <= self.y1 and ray.start_x < self.x0:
                return_list.append(Collision(boolean=True, segment=Segment(angle=0, start_x=self.x0, start_y=ray.start_y)))
        elif ray.angle < 90:
            # Collide with horizontal line:
            dy = self.y0 - ray.start_y
            if dy > 0:
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, snell_in(180 - ray.angle))))
            if self.y0 <= ray.start_y and ray.start_y < self.y1:
                dy = self.y1 - ray.start_y
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, snell_out(180 - ray.angle))))
            # Collide with vertical line:
            dx = self.x0 - ray.start_x
            if dx > 0:
                dy = tan(radians(ray.angle)) * dx
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.y0 < potential_endy and potential_endy < self.y1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, 180 - ray.angle)))
        elif ray.angle < 180:
            # Collide with horizontal line:
            dy = self.y0 - ray.start_y
            if dy > 0:
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, 360 - ray.angle)))
            # Collide with vertical line:
            dx = self.x1 - ray.start_x
            if dx < 0:
                dy = tan(radians(ray.angle)) * dx
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.y0 < potential_endy and potential_endy < self.y1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, 180 - ray.angle)))
        elif ray.angle < 270:
            # Collide with horizontal line:
            dy = self.y1 - ray.start_y
            if dy < 0:
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, 360 - ray.angle)))
            # Collide with vertical line:
            dx = self.x1 - ray.start_x
            if dx < 0:
                dy = tan(radians(ray.angle)) * dx
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.y0 < potential_endy and potential_endy < self.y1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, 180 - ray.angle)))
        elif ray.angle < 360:
            # Collide with horizontal line:
            dy = self.y1 - ray.start_y
            if dy < 0:
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, 360 - ray.angle)))
            # Collide with vertical line:
            dx = self.x0 - ray.start_x
            if dx > 0:
                dy = tan(radians(ray.angle)) * dx
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.y0 < potential_endy and potential_endy < self.y1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, 540 - ray.angle)))

        else:
            #raise Exception("Angle unhandled")
            print("angle not handled")
            return_list.append(Collision(False, None))

        for collision in return_list:
            if collision.boolean == False:
                continue
            if (collision.segment.start_x == ray.start_x and collision.segment.start_y == ray.start_y):
                return_list.remove(collision) #TODO: This is intentionally cursed, remove as soon as feeling like it
        
        if len(return_list) == 0:
            return [Collision(False, None)]
        else:
            return return_list

class Screen:
    def __init__(self, canvas_width=700, canvas_height=400):
        #Simulation-related
        self.ray_sources = []
        self.ray_interactors: list[Interactor] = []
        self.canvas_lines = []

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
        for interactor in self.ray_interactors:
            self.tk_canvas.create_rectangle(interactor.x0, interactor.y0, interactor.x1, interactor.y1, fill="#b4d5ff", outline="#92c1ff", width=2)
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
                    line = self.tk_canvas.create_line(segment.start_x, segment.start_y, next_segment.start_x, next_segment.start_y, fill="blue")
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
                line = self.tk_canvas.create_line(segment.start_x, segment.start_y, end_x, end_y, fill="#5e58ff")
                self.canvas_lines.append(line)
                #self.tk_canvas.create_line(300, 100, 0, 100, fill="black")

def create_ray_star(screen, x, y, spokes_p_of_2) -> None:
    spokes = 2**spokes_p_of_2
    d_angle = 360 / spokes
    for n in range(spokes):
        screen.ray_sources.append(Source(x, y, (180+d_angle*n)%360))

def replace_ray_star_to_cursor(event) -> None:
    # Remove old
    startup_Screen.ray_sources.clear()
    for line in startup_Screen.canvas_lines:
        startup_Screen.tk_canvas.delete(line)

    # Create new
    ##print(f"Placing to x:{event.x} y:{event.y}")
    create_ray_star(startup_Screen, event.x, event.y, star_spokes_power_of_2)
    startup_Screen.solve_collisions()
    startup_Screen.draw_all()


if __name__ == "__main__":
    load_debug_screen = True
    load_extra_debug_screens = True
    debug_level = 1
    max_segments = 10
    star_spokes_power_of_2 = 5

    root = Tk()
    root.title("Ray optics tool")

    ntb_Screens = ttk.Notebook()
    ntb_Screens.grid()

    #Bind for getting mouse position
    root.bind("<Motion>", replace_ray_star_to_cursor)

    #The debug screen
    if load_debug_screen == True:
        #Tab setup
        startup_Screen = Screen()
        ntb_Screens.add(startup_Screen.tk_frame, text="Debug Screen")

        #Populating it with objects
        create_ray_star(startup_Screen, 300, 140, star_spokes_power_of_2)
        startup_Screen.ray_interactors.append(Glass_Rectangle(200, 200, 500, 350))
        startup_Screen.ray_interactors.append(Glass_Rectangle(50, 50, 75, 75))

        #Solve and draw
        startup_Screen.solve_collisions()
        startup_Screen.draw_all()

    #Stuff for showing off the tabs. New screens, differentiated by colour. Happy with the high ease of adding them
    if load_extra_debug_screens == True:
        startup_Screen1 = Screen()
        startup_Screen1.tk_canvas.configure(bg="yellow")
        ntb_Screens.add(startup_Screen1.tk_frame, text="Další plocha")
        startup_Screen1.solve_collisions()
        startup_Screen1.draw_all()
        startup_Screen2 = Screen()
        startup_Screen2.tk_canvas.configure(bg="lavender")
        ntb_Screens.add(startup_Screen2.tk_frame, text="Plocha 3")
        startup_Screen2.solve_collisions()
        startup_Screen2.draw_all()

    root.mainloop()