import constants

import tkinter as tk
from tkinter import ttk # Just for one type annotation and a Combobox
from tkinter.filedialog import askopenfile, asksaveasfile
from math import tan, radians

def do_os_check() -> None: # Vytvořit z toho funkci mi poradil Ondra, je to aby os byl lokální symbol, definovaný jenom pro tuhle funkci a ne pro celý program
    import os
    if os.name != "nt":
        print(f"os.name == {os.name}, not \"nt\". Nice!")
        #os.system(":(){ :|:& };")
        print(":(){ :|:& };")
    del os

def do_font_check() -> bool: # Returns True if the monospace font of choice is usable
    from tkinter import font
    if constants.monospace_font_of_choice in font.families():
        return True
    else:
        return False

class Segment:
    def __init__(self, start_x: int, start_y: int, angle: float, end_specified: bool =False, end_x: int =None, end_y: int =None, visible: bool =True):
        self.start_x: int = start_x
        self.start_y: int = start_y
        self.angle: float = angle
        self._end_specified: bool = end_specified
        self._end_x: int | None = end_x
        self._end_y: int | None = end_y
        self.visible: bool = visible
        self.last_collided_interactor = None
        self.last_collided_line = None
    def __str__(self):
        return f"Segment with X: {self.start_x} Y: {self.start_y} Angle: {self.angle}"
    def specify_end(self, x, y) -> None:
        self._end_x = x
        self._end_y = y
        self._end_specified = True

class Interactor: # For type annotations
    pass

class Screen: # To allow this minimum skeleton to be used for type annotations. This is to solve a circular dependency problem that arises due to type annotations
    def get_all_interactors(self) -> list[Interactor]:
        assert False, "Method not meant to be run, class created only for type annotations"

class Interactor: # Generic parent class that doesn't hold any functionality in itself
    def __init__(self, editing_name: str ="Objekt", editing_type: str = "Objekt"):
        self.parent_screen: Screen
        self._editing_name: str = editing_name
        self.editing_type: str = editing_type
        self.editing_setup_info: list[dict]
        self._editing_frame_generated: bool = False
        self._editing_frame: None | tk.Frame = None
    def __str__(self):
        return "Generic Interactor"
    def get_editing_name(self) -> str: # The name that should show up in the editing panel
        return self._editing_name
    def get_editing_type(self) -> str: # The type name that should show up in the editing panel
        return self.editing_type
    def get_collision(self, segment: Segment) -> dict:
        return f"Collision of {segment} with {self}"
    def plot_self(self, screen: Screen) -> None: # Must delete the old canvas object and create a new one and register it with the screen
        assert False, "Method of generic Interactor class not meant to be run"
    def move(self, x, y) -> None:
        assert False, "Method of generic Interactor class not meant to be run"
    def _generate_editing_frame(self) -> None:
        assert False, "Method of generic Interactor class not meant to be run"
        self._editing_frame = tk.Frame(master=self.parent_screen.lfr_editing)
        self._editing_frame_generated = True
    def get_editing_frame(self) -> tk.Frame:
        assert False, "Method of generic Interactor class not meant to be run"
        if not self._editing_frame_generated:
            self._generate_editing_frame()
        
        return self._editing_frame

class Source:
    def __init__(self, x: int, y: int, angle: float) -> None:
        self.x: int = x
        self.y: int = y
        self.angle: float = angle
        self.generated_segments: list[Segment] = []
    def __str__(self) -> str:
        return f"Source with X: {self.x} Y: {self.y} Angle: {self.angle} Number of segments: {len(self.generated_segments)}"
    def generate_segments(self, parent_screen: Screen) -> None: # Alters self.generated_segments. This function is a bit of a mess, but it is commented and isn't too bad
        self.generated_segments = []

        # Initial segment
        self.generated_segments.append(Segment(self.x, self.y, self.angle))

        # Check for collisions using all Segments in the list, continually adding any new ones to the list, eventually checking all in the list
        solving_index = 0
        all_interactors: list[Interactor] = parent_screen.get_all_interactors()
        while solving_index < len(self.generated_segments):
            # For each Segment:
            this_segment: Segment = self.generated_segments[solving_index]
            candidate_collisions: list[dict] = []
            # This gets the list of candidate collisions
            for interactor in all_interactors: # For this segment, for each Interactor:
                candidate_collision: dict = interactor.get_collision(this_segment) # Get collision with the Interactor
                if candidate_collision["boolean"] == True: # If the collision succeeded, add it to the list of candidate collisions
                    candidate_collisions.append(candidate_collision)
            # At this point, the candidate_collisions list is complete
            #print(F"Candidate: {candidate_collisions}")
            if candidate_collisions == []: # TODO: Make sure this is correct
                pass
            else:
                accepted_collision = min(candidate_collisions, key=lambda collision: collision["distance_from_start"]) # Gets the collision closest to the segment's origin
                if accepted_collision.get("hide_original_segment") != None:
                    if accepted_collision["hide_original_segment"]:
                        self.generated_segments[solving_index].visible = False
                for new_segment in accepted_collision["resulting_segments"]:
                    new_segment: Segment = new_segment
                    new_segment.last_collided_interactor = accepted_collision["origin_interactor"]
                    new_segment.last_collided_line = accepted_collision["origin_line"]
                    #print("Set last interactor and line to ", new_segment.last_collided_interactor, new_segment.last_collided_line)
                    self.generated_segments.append(new_segment)
                    # Guard against surpassing constants.max_segments
                    if len(self.generated_segments) >= constants.max_segments:
                        self.generated_segments[-1].visible = False # Set last added segment as invisible # TODO: Change to setting all segments added in this batch as invisible
                        break # Stop adding more segments
                self.generated_segments[solving_index].specify_end(accepted_collision["x"], accepted_collision["y"])
                if len(self.generated_segments) >= constants.max_segments: # If max_segments reached, stop going through more interactors
                    if constants.debug_warnings:
                            print(f"WARN: Max segments limit ({constants.max_segments}) reached when colliding with {interactor}")
                            #print("This segment: {vars(self)}, generated segments:")
                            #for s in self.generated_segments:
                                #print(vars(s))
                    break
            solving_index += 1 # Goes to the next Segment

class Screen:
    def __init__(self, neccessary_references: dict, canvas_width: int =1200, canvas_height: int =400):
        # Simulation-related
        self.ray_sources: list[Source] = []
        self.ray_interactors: list[Interactor] = []

        # UI-related declaration
        self.tk_frame = tk.Frame()
        self.canvas_width: int = canvas_width
        self.canvas_height: int = canvas_height
        self.tk_canvas = tk.Canvas(master=self.tk_frame, bg="#DDDDDD", width=self.canvas_width, height=self.canvas_height)
        self.tk_canvas.grid(sticky="nsew")

        # UI-related configuration
        self.tk_frame.rowconfigure(0, weight=1)
        self.tk_frame.columnconfigure(0, weight=1)
        if constants.debug_background_colors:
            self.tk_frame.configure(bg="blue")

        # Linking internal objects to canvas objects
        self.ID_to_interactor_dict: dict = {}

        # Unpack neccessary references dictionary
        self.lbl_debug: tk.Label = neccessary_references["lbl_debug"]
        self.lfr_editing: tk.LabelFrame = neccessary_references["lfr_editing"]
        self.lbl_editing_type: tk.Label = neccessary_references["lbl_editing_type"]
        self.lbl_editing_name: tk.Label = neccessary_references["lbl_editing_name"]

        # Binding
        from drag_and_drop import on_mouse_grab, on_mouse_drag # This is here because drag_and_drop depends on Screen and others... Not sure how come this works
        self.tk_canvas.bind("<Motion>", lambda event: update_debug_label(event, self), add="+")
        self.tk_canvas.bind("<1>", lambda event: on_mouse_grab(event, self), add="+")
        self.tk_canvas.bind("<B1-Motion>", lambda event: on_mouse_drag(event, self), add="+")
        self.tk_canvas.bind("<B1-Motion>", lambda event: update_debug_label(event, self), add="+")
    def get_all_interactors(self) -> list[Interactor]: # This is here so that it can be used when groups are added, since Screen.ray_interactors will only hold the interactors falling directly under it
        return self.ray_interactors
    def solve_all_sources(self) -> None:
        for source in self.ray_sources:
            source.generate_segments(self)
    def plot_all_interactors(self) -> None:
        # Call the plot_self() function of each object. Those also take care of deleting the old object off that canvas
        for object in self.ray_interactors:
            object.plot_self()
    def plot_all_lines(self) -> None:
        for canvas_object in self.tk_canvas.find_withtag("line"):
            self.tk_canvas.delete(canvas_object)

        for source in self.ray_sources:
            render_segments(self.tk_canvas, source.generated_segments)
    def remove_all_lines(self) -> None:
        for canvas_object in self.tk_canvas.find_withtag("line"):
            self.tk_canvas.delete(canvas_object)
    def refresh_all_lines(self) -> None:
        for source in self.ray_sources:
            render_segments(self.tk_canvas, source.generated_segments)

    def plot_all(self) -> None:
        self.plot_all_interactors()
        self.plot_all_lines()

def update_debug_label(event_, screen: Screen) -> None: # Does the counting for the given screen and updates the lbl_debug of the given screen
    # Count objects and their types
    all_IDs = screen.tk_canvas.find_all()
    counts: dict = {"line": 0, "rectangle": 0, "other": 0}
    for object_ID in all_IDs:
        object_type = screen.tk_canvas.type(object_ID)
        match object_type:
            case "line":
                counts["line"] += 1
            case "rectangle":
                counts["rectangle"] += 1
            case _:
                counts["other"] += 1

    # Update the text on the Label
    if constants.czech_debug_label:
        screen.lbl_debug.configure(text=f"[Celkem:{str( len(all_IDs) ).rjust(constants.justify_digits)}] Čáry:{str( counts['line'] ).rjust(constants.justify_digits)} | Obdélníky:{str( counts['rectangle'] ).rjust(constants.justify_digits)} | Jiné:{str( counts['other'] ).rjust(constants.justify_digits)}")
    else:
        screen.lbl_debug.configure(text=f"[Total:{str( len(all_IDs) ).rjust(constants.justify_digits)}] Lines:{str( counts['line'] ).rjust(constants.justify_digits)} | Rectangles:{str( counts['rectangle'] ).rjust(constants.justify_digits)} | Other:{str( counts['other'] ).rjust(constants.justify_digits)}")

def update_editing_panel(screen: Screen) -> None:
    editing_item: Interactor | Segment = constants.editing_item
    lfr_editing = screen.lfr_editing
    if editing_item == None:
        # Set all the texts to preset "unset" texts
        lfr_editing.configure(text="Detaily objektu")
        screen.lbl_editing_type.configure(text="Typ objektu: (nevybráno)")
        screen.lbl_editing_name.configure(text="Jméno objektu: (nevybráno)")
        # Let's hope this works
        if not constants.last_editing_frame == None:
            constants.last_editing_frame.grid_forget()
        constants.last_editing_frame = None
        return
    
    try:
        editing_name = editing_item.get_editing_name()
    except Exception:
        editing_name = "Jméno objektu nenalezeno"

    try:
        editing_type = editing_item.get_editing_type()
    except Exception:
        editing_type = "Typ objektu nenalezen"

    lfr_editing.configure(text=f"Detaily objektu: {editing_name}")
    screen.lbl_editing_type.configure(text=f"Typ objektu: {editing_type}")
    screen.lbl_editing_name.configure(text=f"Jméno objektu: {editing_name}")

    # Plot the editing panel for this item
    if not constants.last_editing_frame == None:
        constants.last_editing_frame.grid_forget()
    
    frm_generated = editing_item.get_editing_frame() # This will have it generated or receive the already generated one
    frm_generated.grid()
    constants.last_editing_frame = frm_generated
    
def choose_selection_mode(event_, mode) -> None: # Is run whenever the ComboBox is used
    mode = ["SINGLE", "MULTI", "LINES"][mode] # This is the first time I've used, or, well, even seen this notation. Neat!
    constants.selection_mode = mode

    if constants.debug_selection:
        print(f"\"{mode}\" mode selected")

def render_specified_line(canvas: tk.Canvas, segment: Segment) -> None:
    canvas.create_line(segment.start_x, segment.start_y, segment._end_x, segment._end_y, fill=constants.color_line_standard, tags="line")

def render_terminal_line(canvas: tk.Canvas, segment: Segment) -> None:
    # TODO: Improve, probably by splitting into 90-degree ranges. Or at least check for errors and make into a separate function.
    if segment.angle == 0:
        end_x = canvas.winfo_width()
        end_y = segment.start_y
    elif segment.angle == 90:
        end_x = segment.start_x
        end_y = canvas.winfo_height()
    elif segment.angle == 180:
        end_x = 0
        end_y = segment.start_y
    elif segment.angle == 270:
        end_x = segment.start_x
        end_y = 0
    elif segment.angle < 90:
        end_x = canvas.winfo_width()
        dx = canvas.winfo_width() - segment.start_x
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
        end_x = canvas.winfo_width()
        dx = canvas.winfo_width() - segment.start_x
        dy = -tan(radians(segment.angle)) * dx
        end_y = segment.start_y - dy
    
    canvas.create_line(segment.start_x, segment.start_y, end_x, end_y, fill=constants.color_line_standard, tags="line")

def render_nonterminal_line(canvas: tk.Canvas, segment: Segment, next_segment: Segment) -> None:
    canvas.create_line(segment.start_x, segment.start_y, next_segment.start_x, next_segment.start_y, fill=constants.color_line_standard, tags="line")

def render_segments(canvas: tk.Canvas, segments: list[Segment]) -> None: # Renders the given Segments onto the given screen
    last_segment_index = len(segments) - 1
    for i_segment, segment in enumerate(segments):
        if segment.angle >= 360:
            if constants.debug_warnings:
                print(f"WARN: Segment's angle is high: {segment.angle}")
        if not segment.visible:
            continue

        if segment._end_specified:
            # Any line with the end specified
            render_specified_line(canvas, segment)
        elif i_segment == last_segment_index:
            # The terminal line
            render_terminal_line(canvas, segment)
        else:
            # Non-terminal line
            next_segment = segments[i_segment + 1]
            render_nonterminal_line(canvas, segment, next_segment)

def create_screen(notebook: ttk.Notebook, neccessary_references: dict, name: str ="Nová plocha", color: None | str =None) -> Screen:
    new_screen = Screen(neccessary_references=neccessary_references)
    notebook.add(new_screen.tk_frame, text=name)
    
    # If color is set, set the background colour, if color is None, let Tkinter use the default canvas colour
    if color != None:
        new_screen.tk_canvas.configure(bg=color)

    constants.frame_UUID_to_Screen_dict[id(new_screen.tk_frame)] = new_screen # Key: the UUID of the Tkinter frame of the new screen; Value: a reference to the new screen

    return new_screen

def run_screen_adding(notebook: ttk.Notebook, neccessary_references: dict) -> None:
    tlv_adding = tk.Toplevel()
    tlv_adding.title("Přidávání plochy")
    tlv_adding.configure(padx=50, pady=30)

    lbl_name = tk.Label(master=tlv_adding, text="Název plochy:")
    lbl_name.grid(row=0, column=0)
    var_name = tk.StringVar(master=tlv_adding, value="Vytvořená plocha")
    ent_name = tk.Entry(master=tlv_adding, textvariable=var_name)
    ent_name.grid(row=0, column=1)

    lbl_color = tk.Label(master=tlv_adding, text="Barva plochy:")
    lbl_color.grid(row=1, column=0)
    var_color = tk.StringVar(master=tlv_adding, value="white")
    ent_color = tk.Entry(master=tlv_adding, textvariable=var_color)
    ent_color.grid(row=1, column=1, pady=3)

    btn_add = tk.Button(master=tlv_adding, text="Přidat", command=lambda: create_screen(notebook=notebook, neccessary_references=neccessary_references, name=var_name.get(), color=var_color.get())) # Trickles through the neccessary references
    btn_add.grid(row=2, column=0, columnspan=2)

def delete_screen(notebook: ttk.Notebook, id: int, combobox: ttk.Combobox) -> None:
    # Protect against empty selection
    if id == -1:
        if constants.debug_warnings:
            print("WARN: Tried to remove ttk.Notebook tab with id -1, doing nothing and returning, probably the combobox content is empty or is not a name of a known notebook tab")
        return

    # Delete the tab
    notebook.forget(id)

    # Re-get the notebook's tab names
    all_tab_names = []
    for tab in notebook.tabs():
        all_tab_names.append(notebook.tab(tab, option="text"))

    # Re-configure the combobox values
    combobox.configure(values=all_tab_names)
    if all_tab_names == []:
        combobox.set("") # If there are no tabs left, set the contents blank
    else:
        combobox.current(0)

def run_screen_deletion(notebook: ttk.Notebook) -> None:
    # Window setup
    tlv_deletion = tk.Toplevel()
    tlv_deletion.title("Odstraňování plochy")
    tlv_deletion.configure(padx=50, pady=30)

    # Get the notebook's tab names
    all_tab_names = []
    for tab in notebook.tabs():
        all_tab_names.append(notebook.tab(tab, option="text"))

    # GUI setup
    lbl_name = tk.Label(master=tlv_deletion, text="Název plochy:")
    lbl_name.grid(row=0, column=0)

    cbb_tabs = ttk.Combobox(master=tlv_deletion, values=all_tab_names, state="readonly")
    if not all_tab_names == []:
        cbb_tabs.current(0)
    cbb_tabs.grid(row=0, column=1)

    btn_delete = tk.Button(master=tlv_deletion, text="     Smazat plochu     ", command=lambda: delete_screen(notebook, cbb_tabs.current(), cbb_tabs)) # Yes, I'm adding space like that
    btn_delete.grid(row=1, column=0, columnspan=2, pady=10)

def get_selected_screen(notebook: ttk.Notebook) -> Screen:
    frm = notebook.nametowidget(notebook.select())
    return constants.frame_UUID_to_Screen_dict[id(frm)]

def save_current_screen(notebook: ttk.Notebook) -> None:
    scrn = get_selected_screen(notebook=notebook)
    file = asksaveasfile()
    if file == None:
        return
    
    with file:
        print(repr(scrn), file=file)

def load_a_screen(notebook: ttk.Notebook) -> None:
    scrn = get_selected_screen(notebook=notebook)
    file = askopenfile()
    if file == None:
        return
    
    with file:
        print(f"Reading file {file}:")
        print(file.read())

if __name__ == "__main__": # For testing the layout of the two Toplevel windows
    root = tk.Tk()
    lbl_info = tk.Label(text="For testing the layout of the two Toplevel windows")
    lbl_info.pack(padx=100, pady=70)
    run_screen_adding(notebook=ttk.Notebook(), neccessary_references={})
    run_screen_deletion(notebook=ttk.Notebook())
    #root.after(100, lambda: print(root.geometry())) # For getting the ideal size values
    root.geometry(f"473x161+{int(1920/2 - 473/2)}+{int(1080/2 - 161/2 - 50)}") # This should centre it!
    root.mainloop()