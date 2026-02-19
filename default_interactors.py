from core_classes import *
from drag_and_drop import *

from math import degrees, sin, asin

class Glass_Rectangle(Interactor): #TODO: Decide how such objects will be stored
    def __init__(self, x0, y0, x1, y1):
        if x0 >= x1 or y0 >= y1:
            raise Exception("Wrong order or the same")
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.canvas_rectangle: int | None = None
    def __str__(self):
        return "Glass Rectangle"
    def collide(self, ray: Segment) -> list[tuple[bool, int, int]]:
        return_list: list[Collision] = []
        if ray.angle == 90:
            if self.x0 <= ray.start_x and ray.start_x <= self.x1 and ray.start_y < self.y0:
                return_list.append(Collision(boolean=True, segments=[Segment(angle=270, start_x=ray.start_x, start_y=self.y0)]))
        elif ray.angle == 270:
            if self.x0 <= ray.start_x and ray.start_x <= self.x1 and ray.start_y > self.y1:
                return_list.append(Collision(boolean=True, segments=[Segment(angle=90, start_x=ray.start_x, start_y=self.y1)]))
        elif ray.angle == 180:
            if self.y0 <= ray.start_y and ray.start_y <= self.y1 and ray.start_x > self.x1:
                return_list.append(Collision(boolean=True, segments=[Segment(angle=0, start_x=self.x1, start_y=ray.start_y)]))
        elif ray.angle == 0:
            if self.y0 <= ray.start_y and ray.start_y <= self.y1 and ray.start_x < self.x0:
                return_list.append(Collision(boolean=True, segments=[Segment(angle=180, start_x=self.x0, start_y=ray.start_y)]))
        elif ray.angle < 90:
            # Collide with horizontal line:
            dy = self.y0 - ray.start_y
            if dy > 0:
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segments=[Segment(potential_endx, potential_endy, 360 - ray.angle)]))
            # Collide with vertical line:
            dx = self.x0 - ray.start_x
            if dx > 0:
                dy = tan(radians(ray.angle)) * dx
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.y0 < potential_endy and potential_endy < self.y1:
                    return_list.append(Collision(boolean=True, segments=[Segment(potential_endx, potential_endy, 180 - ray.angle)]))
        elif ray.angle < 180:
            # Collide with horizontal line:
            dy = self.y0 - ray.start_y
            if dy > 0:
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segments=[Segment(potential_endx, potential_endy, 360 - ray.angle)]))
            # Collide with vertical line:
            dx = self.x1 - ray.start_x
            if dx < 0:
                dy = tan(radians(ray.angle)) * dx
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.y0 < potential_endy and potential_endy < self.y1:
                    return_list.append(Collision(boolean=True, segments=[Segment(potential_endx, potential_endy, 180 - ray.angle)]))
        elif ray.angle < 270:
            # Collide with horizontal line:
            dy = self.y1 - ray.start_y
            if dy < 0:
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segments=[Segment(potential_endx, potential_endy, 360 - ray.angle)]))
            # Collide with vertical line:
            dx = self.x1 - ray.start_x
            if dx < 0:
                dy = tan(radians(ray.angle)) * dx
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.y0 < potential_endy and potential_endy < self.y1:
                    return_list.append(Collision(boolean=True, segments=[Segment(potential_endx, potential_endy, 180 - ray.angle)]))
        elif ray.angle < 360:
            # Collide with horizontal line:
            dy = self.y1 - ray.start_y
            if dy < 0:
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segments=[Segment(potential_endx, potential_endy, 360 - ray.angle)]))
            # Collide with vertical line:
            dx = self.x0 - ray.start_x
            if dx > 0:
                dy = tan(radians(ray.angle)) * dx
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.y0 < potential_endy and potential_endy < self.y1:
                    return_list.append(Collision(boolean=True, segments=[Segment(potential_endx, potential_endy, 540 - ray.angle)]))

        else:
            #raise Exception("Angle unhandled")
            print("angle not handled")
            return_list.append(Collision(False, None))

        for collision in return_list:
            try:
                for seg in collision.segments:
                    if collision.boolean == False:
                        continue
                    if (seg.start_x == ray.start_x and seg.start_y == ray.start_y):
                        return_list.remove(seg) #TODO: This is intentionally cursed, remove as soon as feeling like it
            except:
                print(collision)
                breakpoint
        
        if len(return_list) == 0:
            return [Collision(False, None)]
        else:
            return return_list
    def plot_self(self, screen: Screen):
        # Deletes this object off that canvas
        if self.canvas_rectangle != None:
            screen.tk_canvas.delete(self.canvas_rectangle)

        # Creates the object for this... object
        self.canvas_rectangle = screen.tk_canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill="#CCCCCC", outline="#E5E5E5", width=2)

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
                return_list.append(Collision(boolean=True, segments=[Segment(angle=90, start_x=ray.start_x, start_y=self.y0)]))
        elif ray.angle == 270:
            if self.x0 <= ray.start_x and ray.start_x <= self.x1 and ray.start_y > self.y1:
                return_list.append(Collision(boolean=True, segments=[Segment(angle=270, start_x=ray.start_x, start_y=self.y1)]))
        elif ray.angle == 180:
            if self.y0 <= ray.start_y and ray.start_y <= self.y1 and ray.start_x > self.x1:
                return_list.append(Collision(boolean=True, segments=[Segment(angle=180, start_x=self.x1, start_y=ray.start_y)]))
        elif ray.angle == 0:
            if self.y0 <= ray.start_y and ray.start_y <= self.y1 and ray.start_x < self.x0:
                return_list.append(Collision(boolean=True, segments=[Segment(angle=0, start_x=self.x0, start_y=ray.start_y)]))
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
                    return_list.append(Collision(boolean=True, segments=[Segment(potential_endx, potential_endy, snell_in(90 - ray.angle))]))
            if self.y0 <= ray.start_y and ray.start_y < self.y1:
                dy = self.y1 - ray.start_y
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segments=[Segment(potential_endx, potential_endy, snell_out(90 - ray.angle))]))
            # Collide with vertical line:
            dx = self.x0 - ray.start_x
            if dx > 0:
                dy = tan(radians(ray.angle)) * dx
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.y0 < potential_endy and potential_endy < self.y1:
                    return_list.append(Collision(boolean=True, segments=[Segment(potential_endx, potential_endy, 180 - ray.angle)]))
        elif ray.angle < 180:
            # Collide with horizontal line:
            dy = self.y0 - ray.start_y
            if dy > 0:
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segments=[Segment(potential_endx, potential_endy, 360 - ray.angle)]))
            # Collide with vertical line:
            dx = self.x1 - ray.start_x
            if dx < 0:
                dy = tan(radians(ray.angle)) * dx
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.y0 < potential_endy and potential_endy < self.y1:
                    return_list.append(Collision(boolean=True, segments=[Segment(potential_endx, potential_endy, 180 - ray.angle)]))
        elif ray.angle < 270:
            # Collide with horizontal line:
            dy = self.y1 - ray.start_y
            if dy < 0:
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segments=[Segment(potential_endx, potential_endy, 360 - ray.angle)]))
            # Collide with vertical line:
            dx = self.x1 - ray.start_x
            if dx < 0:
                dy = tan(radians(ray.angle)) * dx
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.y0 < potential_endy and potential_endy < self.y1:
                    return_list.append(Collision(boolean=True, segments=[Segment(potential_endx, potential_endy, 180 - ray.angle)]))
        elif ray.angle < 360:
            # Collide with horizontal line:
            dy = self.y1 - ray.start_y
            if dy < 0:
                dx = (1/tan(radians(ray.angle))) * dy
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.x0 < potential_endx and potential_endx < self.x1:
                    return_list.append(Collision(boolean=True, segments=[Segment(potential_endx, potential_endy, 360 - ray.angle)]))
            # Collide with vertical line:
            dx = self.x0 - ray.start_x
            if dx > 0:
                dy = tan(radians(ray.angle)) * dx
                potential_endx = ray.start_x + dx
                potential_endy = ray.start_y + dy
                if self.y0 < potential_endy and potential_endy < self.y1:
                    return_list.append(Collision(boolean=True, segments=[Segment(potential_endx, potential_endy, 540 - ray.angle)]))

        else:
            #raise Exception("Angle unhandled")
            print("angle not handled")
            return_list.append(Collision(False, None))

        for collision in return_list:
            if collision.boolean == False:
                continue
            if (collision.segments.start_x == ray.start_x and collision.segments.start_y == ray.start_y):
                return_list.remove(collision) #TODO: This is intentionally cursed, remove as soon as feeling like it
        
        if len(return_list) == 0:
            return [Collision(False, None)]
        else:
            return return_list