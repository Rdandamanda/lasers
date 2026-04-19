from core_classes import *
from collisions import collide_seg_box
from random import randint

class Glass_Rectangle(Interactor):
    def __init__(self, parent_screen, x0, y0, x1, y1, editing_name: str ="Zrcadlo", editing_type: str = "Zrcadlo"):
        self.parent_screen = parent_screen
        # Ensures coordinates are in the correct order x0 <= x1; y0 <= y1
        # If they are the same (x0 == x1 or y0 == y1), it still warns, and still switches them (which has no effect), but lets them be the same
        if x0 >= x1 or y0 >= y1:
            if constants.debug_warnings:
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
        self._editing_name: str = f"{editing_name} #{randint(1111, 9999)}"
        self.editing_type: str = editing_type
        self._editing_frame_generated: bool = False
        self._editing_frame: None | tk.Frame = None
    def __str__(self):
        return f"Glass Rectangle ({self._editing_name})"
    def get_editing_name(self) -> str: # The name that should show up in the editing panel
        return self._editing_name
    def set_editing_name(self, name) -> None:
        self._editing_name = name
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
        if self._editing_frame_generated:
            self.lbl_coordinates.configure(text=f"Souřadnice: X:{self.x1} Y:{-self.y1}") # Minus because I don't fell like explaining to the user why the y is flipped and counted from the top left corner)
    def edit_size(self, _a, _b, _c) -> None: # Those three arguments supplied by the tk.StringVar trace
        if constants.debug_editing:
            print("Attempting edit...")

        # Sanitise input
        try:
            new_width = int(self.var_width.get())
            new_height = int(self.var_height.get())
        except:
            return
        if new_width < 1 or new_height < 1:
            return
        
        # Set own width and height
        self.x1 = self.x0 + new_width
        self.y1 = self.y0 + new_height

        # Run the updates
        self.parent_screen.solve_all_sources()
        self.parent_screen.plot_all()
        if constants.debug_editing:
            print(f"Worked, newly: {self.var_width.get()}, {self.var_height.get(), 1}")
    def _generate_editing_frame(self) -> None:
        self._editing_frame = tk.Frame(master=self.parent_screen.lfr_editing)
        frm = self._editing_frame # Shorthand
        if constants.debug_background_colors:
            frm.configure(background="green")

        # Coordinates label
        self.lbl_coordinates = tk.Label(master=frm, text=f"Souřadnice: X:{self.x1} Y:{-self.y1}") # Minus because I don't fell like explaining to the user why the y is flipped and counted from the top left corner
        self.lbl_coordinates.grid(row=0, column=0, columnspan=2)

        # Size entry
        self.lbl_width = tk.Label(master=frm, text="Šířka: ")
        self.lbl_width.grid(row=1, column=0, sticky="e")
        self.var_width = tk.StringVar()
        self.var_width.set(self.x1 - self.x0) # Display current width
        self.var_width.trace("w", self.edit_size) # Takes care of all three types of setting
        self.spb_width = tk.Spinbox(master=frm, textvariable=self.var_width, from_=1, to=100000)
        self.spb_width.grid(row=1, column=1)
        
        self.lbl_height = tk.Label(master=frm, text="Výška: ")
        self.lbl_height.grid(row=2, column=0, sticky="e")
        self.var_height = tk.StringVar()
        self.var_height.set(self.y1 - self.y0) # Display current height
        self.var_height.trace("w", self.edit_size) # Takes care of all three types of setting
        self.spb_height = tk.Spinbox(master=frm, textvariable=self.var_height, from_=1, to=100000)
        self.spb_height.grid(row=2, column=1)

        self.lbl_pixels = tk.Label(master=frm, text="(Vše udáváno v pixelech)")
        self.lbl_pixels.grid(row=3, column=0, columnspan=2, pady=7)

        self._editing_frame_generated = True
    def get_editing_frame(self) -> tk.Frame:
        if not self._editing_frame_generated:
            self._generate_editing_frame()
        
        return self._editing_frame

class Obstacle_Rectangle(Interactor):
    def __init__(self, parent_screen, x0, y0, x1, y1, editing_name: str ="Překážka", editing_type: str = "Překážka"):
        self.parent_screen = parent_screen
        # Ensures coordinates are in the correct order x0 <= x1; y0 <= y1
        # If they are the same (x0 == x1 or y0 == y1), it still warns, and still switches them (which has no effect), but lets them be the same
        if x0 >= x1 or y0 >= y1:
            if constants.debug_warnings:
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
        self._editing_frame_generated: bool = False
        self._editing_frame: None | tk.Frame = None
    def __str__(self):
        return f"Obstacle Rectangle ({self.editing_name})"
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
        if self._editing_frame_generated:
            self.lbl_coordinates.configure(text=f"Souřadnice: X:{self.x1} Y:{-self.y1}") # Minus because I don't fell like explaining to the user why the y is flipped and counted from the top left corner)
    def edit_size(self, _a, _b, _c) -> None: # Those three arguments supplied by the tk.StringVar trace
        if constants.debug_editing:
            print("Attempting edit...")

        # Sanitise input
        try:
            new_width = int(self.var_width.get())
            new_height = int(self.var_height.get())
        except:
            return
        if new_width < 1 or new_height < 1:
            return
        
        # Set own width and height
        self.x1 = self.x0 + new_width
        self.y1 = self.y0 + new_height

        # Run the updates
        self.parent_screen.solve_all_sources()
        self.parent_screen.plot_all()
        if constants.debug_editing:
            print(f"Worked, newly: {self.var_width.get()}, {self.var_height.get(), 1}")
    def _generate_editing_frame(self) -> None:
        self._editing_frame = tk.Frame(master=self.parent_screen.lfr_editing)
        frm = self._editing_frame # Shorthand
        if constants.debug_background_colors:
            frm.configure(background="green")

        # Coordinates label
        self.lbl_coordinates = tk.Label(master=frm, text=f"Souřadnice: X:{self.x1} Y:{-self.y1}") # Minus because I don't fell like explaining to the user why the y is flipped and counted from the top left corner
        self.lbl_coordinates.grid(row=0, column=0, columnspan=2)

        # Size entry
        self.lbl_width = tk.Label(master=frm, text="Šířka: ")
        self.lbl_width.grid(row=1, column=0, sticky="e")
        self.var_width = tk.StringVar()
        self.var_width.set(self.x1 - self.x0) # Display current width
        self.var_width.trace("w", self.edit_size) # Takes care of all three types of setting
        self.spb_width = tk.Spinbox(master=frm, textvariable=self.var_width, from_=1, to=100000)
        self.spb_width.grid(row=1, column=1)
        
        self.lbl_height = tk.Label(master=frm, text="Výška: ")
        self.lbl_height.grid(row=2, column=0, sticky="e")
        self.var_height = tk.StringVar()
        self.var_height.set(self.y1 - self.y0) # Display current height
        self.var_height.trace("w", self.edit_size) # Takes care of all three types of setting
        self.spb_height = tk.Spinbox(master=frm, textvariable=self.var_height, from_=1, to=100000)
        self.spb_height.grid(row=2, column=1)

        self.lbl_pixels = tk.Label(master=frm, text="(Vše udáváno v pixelech)")
        self.lbl_pixels.grid(row=3, column=0, columnspan=2, pady=7)

        self._editing_frame_generated = True
    def get_editing_frame(self) -> tk.Frame:
        if not self._editing_frame_generated:
            self._generate_editing_frame()
        
        return self._editing_frame