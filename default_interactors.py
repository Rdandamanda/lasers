from core_classes import *
from collisions import collide_seg_box
from random import randint

class Glass_Rectangle(Interactor):
    def __init__(self, parent_screen, x0, y0, x1, y1, editing_name: str ="Zrcadlo", editing_type: str = "Zrcadlo"):
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
        # TODO: This can eventually be switched out for a materials system, for easier and cleaner-defined defaults and convenient customisation in the GUI
        self.color_fill = "#CCCCCC"
        self.color_outline = "#E5E5E5"
        # attributes specific to the editing panel
        self.editing_name: str = f"{editing_name} #{randint(1111, 9999)}"
        self.editing_type: str = editing_type
    def __str__(self):
        return "Glass Rectangle"
    def get_editing_name(self) -> str: # The name that should show up in the editing panel
        return self.editing_name
    def get_editing_type(self) -> str: # The type name that should show up in the editing panel
        return self.editing_type
    def get_collision(self, segment: Segment) -> dict:
        same_interactor = True if segment.last_collided_interactor == self else False
        return_dict = collide_seg_box(segment.start_x, segment.start_y, segment.angle, self.x0, self.y0, self.x1, self.y1, same_interactor, segment.last_collided_line)
        return_dict["origin_interactor"] = self
        if return_dict.get("origin_line") == None:
            return_dict["origin_line"] = None
        return return_dict
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


class Obstacle_Rectangle(Interactor):
    def __init__(self, parent_screen, x0, y0, x1, y1, editing_name: str ="Překážka", editing_type: str = "Překážka"):
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
        # TODO: This can eventually be switched out for a materials system, for easier and cleaner-defined defaults and convenient customisation in the GUI
        self.color_fill = "#000000"
        self.color_outline = "#000000"
        # attributes specific to the editing panel
        self.editing_name: str = f"{editing_name} #{randint(1111, 9999)}"
        self.editing_type: str = editing_type
    def __str__(self):
        return "Obstacle Rectangle"
    def get_editing_name(self) -> str: # The name that should show up in the editing panel
        return self.editing_name
    def get_editing_type(self) -> str: # The type name that should show up in the editing panel
        return self.editing_type
    def get_collision(self, segment: Segment) -> dict:
        same_interactor = True if segment.last_collided_interactor == self else False
        return_dict = collide_seg_box(segment.start_x, segment.start_y, segment.angle, self.x0, self.y0, self.x1, self.y1, same_interactor, segment.last_collided_line)
        return_dict["origin_interactor"] = self
        return_dict["resulting_segments"] = []
        if return_dict.get("origin_line") == None:
            return_dict["origin_line"] = None
        return return_dict
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