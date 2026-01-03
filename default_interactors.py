from core_classes import *

from math import degrees, sin, asin

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

def snell_in(angle) -> float:
    if angle >= 0:
        #print(f"Angle: {angle}")
        angle += 360
    # sin(beta) = sin(alpha) / ratio
    print(degrees( asin(sin(radians(angle)) / 1.1) ))
    return degrees( asin(sin(radians(angle)) / 1.1) )
def snell_out(angle) -> float:
    if angle >= 0:
        #print(f"Angle: {angle}")
        angle += 360
    # sin(beta) = sin(alpha) / ratio
    print(degrees( asin(sin(radians(angle)) * 1.1) ))
    return degrees( asin(sin(radians(angle)) * 1.1) )

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
            if ray.angle < 0:
                print(f"Angle < 0! {ray.angle}")
            # Collide with horizontal line:
            dy = self.y0 - ray.start_y
            if dy > 0:
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, snell_in(90 - ray.angle))))
            if self.y0 <= ray.start_y and ray.start_y < self.y1:
                dy = self.y1 - ray.start_y
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segment=Segment(potential_endx, potential_endy, snell_out(90 - ray.angle))))
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
                line = self.tk_canvas.create_line(segment.start_x, segment.start_y, end_x, end_y, fill=colour_final)
                self.canvas_lines.append(line)
                #self.tk_canvas.create_line(300, 100, 0, 100, fill="black")