from core_classes import *

class Glass_Rectangle(Interactor):
    def __init__(self, parent_screen, x0, y0, x1, y1):
        self.parent_screen = parent_screen
        # Ensures coordinates are in the correct order x0 <= x1; y0 <= y1
        # If they are the same (x0 == x1 or y0 == y1), it still warns, and still switches them (which has no effect), but lets them be the same
        if x0 >= x1 or y0 >= y1:
            if constants.debug_level >= 1:
                print("WARN: Rectangle coordinates specified in the wrong order or are the same")
            if x0 >= x1:
                x0, x1 = x1, x0
            if y0 >= y1:
                y0, y1 = y1, y0
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.canvas_rectangle: int | None = None
        # Constants specific to this type of interactor - in this case, customisation colours
        self.color_fill = "#CCCCCC"
        self.color_outline = "#E5E5E5"
        # TODO: This can eventually be switched out for a materials system, for easier and cleaner-defined defaults and convenient customisation in the GUI
    def __str__(self):
        return "Glass Rectangle"
    def get_collision(self, ray: Segment) -> list[Collision]: # TODO: This is the big thing to fix
        #How many hours of sleep was I on when writing this?
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
    def plot_self(self):
        screen = self.parent_screen
        # Deletes this object off that canvas
        if self.canvas_rectangle != None:
            screen.tk_canvas.delete(self.canvas_rectangle)
            del screen.ID_to_interactor_dict[self.canvas_rectangle]

        # Creates the canvas object for this... object
        self.canvas_rectangle = screen.tk_canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=self.color_fill, outline=self.color_outline, width=2)

        # Registers the canvas object with the screen
        screen.ID_to_interactor_dict[self.canvas_rectangle] = self
    def move(self, x, y) -> None:
        self.x0 += x
        self.x1 += x
        self.y0 += y
        self.y1 += y