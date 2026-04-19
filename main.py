from constants import load_debug_screen, load_extra_debug_screens, monospace_font_of_choice
from core_classes import *
from default_interactors import *
from default_sources import *

from tkinter import ttk
do_os_check()

def create_item(notebook: ttk.Notebook, item_type: str, item_shape: str) -> None:
    screen = get_selected_screen(notebook=notebook)
    screen.ray_interactors.append(Obstacle_Rectangle(startup_Screen1, 200, 200, 350, 500))
    print(screen.ray_interactors)
    screen.solve_all_sources()
    screen.plot_all()

if __name__ == "__main__":
    # GUI setup
    root = tk.Tk()
    root.title("Nástroj na paprskovou optiku")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=0)
    root.rowconfigure(1, weight=1)
    
    font_of_choice_available: bool = do_font_check() # Tohle potřebuje být až tady, protože to potřebuje, aby existovala instance Tk()

    # Menu bar (upper, thin) setup
    menubar = tk.Menu(master=root)
    root.configure(menu=menubar)

    mnu_plochy = tk.Menu(master=menubar)
    menubar.add_cascade(label="Plochy", menu=mnu_plochy)
    # The screen adding and deletion commands are set later, they require a bunch of widgets exist

    menubar.add_command(label="Zavřít", command=root.quit)

    # Tool bar (lower, with custom buttons)
    frm_toolbar = tk.Frame(root)
    frm_toolbar.grid(row=0, column=0, sticky="ew")
    if constants.debug_background_colors:
        frm_toolbar.configure(bg="green")

    # Selection mode selection
    lbl_selection_label = tk.Label(master=frm_toolbar, text="Režim výběru: ")
    lbl_selection_label.grid(row=0, column=0, padx=(3, 0), pady=3)
    var_selection_mode = tk.StringVar()
    cbb_selection_mode = ttk.Combobox(master=frm_toolbar, values=["Vrchní objekt", "Všechny pod kurzorem", "Segmenty čar"], state="readonly", textvariable=var_selection_mode)
    cbb_selection_mode.grid(row=0, column=1, padx=(3, 0), pady=3)
    cbb_selection_mode.bind("<<ComboboxSelected>>", lambda event_: choose_selection_mode(event_, cbb_selection_mode.current()))
    cbb_selection_mode.current(0) # Set the default value as the first in the list

    # Refresh button
    sep_toolbar_separator_1 = ttk.Separator(master=frm_toolbar, orient=tk.VERTICAL)
    sep_toolbar_separator_1.grid(row=0, column=2, padx=(8, 7), pady=2, sticky="ns")
    btn_refresh = tk.Button(master=frm_toolbar, text="Aktualizovat obrazovku")
    btn_refresh.grid(row=0, column=3, pady=1)

    # Item adding section
    sep_toolbar_separator_2 = ttk.Separator(master=frm_toolbar, orient=tk.VERTICAL)
    sep_toolbar_separator_2.grid(row=0, column=4, padx=(7, 3), pady=2, sticky="ns")

    lbl_item_type = tk.Label(master=frm_toolbar, text="Přidávání objektu:")
    lbl_item_type.grid(row=0, column=5)
    var_item_type = tk.StringVar()
    cbb_item_type = ttk.Combobox(master=frm_toolbar, values=["Zrcadlo", "Překážka"], state="readonly", textvariable=var_item_type)
    cbb_item_type.grid(row=0, column=6, padx=(3, 0), pady=3)
    #cbb_item_type.bind("<<ComboboxSelected>>", lambda event_: choose_selection_mode(event_, cbb_selection_mode.current()))
    cbb_item_type.current(0) # Set the default value as the first in the list

    lbl_item_shape = tk.Label(master=frm_toolbar, text="; Tvar objektu:")
    lbl_item_shape.grid(row=0, column=7)
    var_item_shape = tk.StringVar()
    cbb_item_shape = ttk.Combobox(master=frm_toolbar, values=["Tenký vodorovný", "Tenký svislý", "Čtvercový"], state="readonly", textvariable=var_item_shape)
    cbb_item_shape.grid(row=0, column=8, padx=(3, 0), pady=3)
    #cbb_item_type.bind("<<ComboboxSelected>>", lambda event_: choose_selection_mode(event_, cbb_selection_mode.current()))
    cbb_item_shape.current(0) # Set the default value as the first in the list

    btn_add_object = tk.Button(master=frm_toolbar, text="Přidat objekt") # The command will be configured later, it needs the Notebook widget to exist
    btn_add_object.grid(row=0, column=9, padx=7, pady=1)

    # Panedwindow setup
    pnw_panes = ttk.Panedwindow(master=root, orient=tk.HORIZONTAL)
    pnw_panes.grid(sticky="nsew", row=1, column=0)

    # Left pane
    tvw_objects = ttk.Treeview()
    pnw_panes.add(tvw_objects, weight=0)

    # Central pane
    frm_screens = tk.Frame() # Obsahuje ntb_screens a lbl_debug a grp_grip
    if constants.debug_background_colors:
        frm_screens.configure(bg="red")
    frm_screens.columnconfigure(0, weight=1)
    frm_screens.rowconfigure(0, weight=1)
    pnw_panes.add(frm_screens, weight=1)

    ntb_Screens = ttk.Notebook(master=frm_screens)
    ntb_Screens.grid(columnspan=2, sticky="nsew")
    btn_add_object.configure(command=lambda: create_item(notebook=ntb_Screens, item_type=var_item_type.get(), item_shape=var_item_shape.get())) # The command can now be set, it requires a reference to the Notebook widget as an argument

    lbl_debug = tk.Label(master=frm_screens)
    if font_of_choice_available:
        lbl_debug.configure(font=(monospace_font_of_choice, 10))
    lbl_debug.grid(sticky="ew")

    grp_grip_center = ttk.Sizegrip(master=frm_screens)
    grp_grip_center.grid(column=1, row=1, sticky="ns")

    # Right pane
    frm_editing = tk.Frame()
    if constants.debug_background_colors:
        frm_editing.configure(bg="yellow")
    frm_editing.rowconfigure(0, weight=1)
    frm_editing.columnconfigure(0, weight=1)
    pnw_panes.add(frm_editing, weight=0)

    lfr_editing = tk.LabelFrame(master=frm_editing, text="Detaily objektu")
    lfr_editing.grid(sticky="nsew", padx=(0, 5))

    lbl_editing_type = tk.Label(master=lfr_editing, width=30, text="Typ objektu: (nevybráno)")
    lbl_editing_type.grid(pady=(10, 0))
    lbl_editing_name = tk.Label(master=lfr_editing, width=30, text="Jméno objektu: (nevybráno)")
    lbl_editing_name.grid(pady=(10, 0))
    sep_editing_pane = ttk.Separator(master=lfr_editing)
    sep_editing_pane.grid(sticky="ew", padx=7, pady=7)

    grp_grip_right = ttk.Sizegrip(master=frm_editing)
    grp_grip_right.grid(column=0, row=1, sticky="se")

    # Contains references to the neccessary widgets for Screen creation
    screen_dict: dict = {"lbl_debug": lbl_debug, "lfr_editing": lfr_editing, "lbl_editing_type": lbl_editing_type, "lbl_editing_name": lbl_editing_name}

    # The window is now ready for adding Screens
    mnu_plochy.add_command(label="Přidat plochu", command=lambda: run_screen_adding(notebook=ntb_Screens, neccessary_references=screen_dict)) # This lambda function can now be configured properly, that's why this is all the way here
    mnu_plochy.add_command(label="Odstranit plochu", command=lambda: run_screen_deletion(notebook=ntb_Screens))

    # The debug screen
    if load_debug_screen == True:
        # Tab setup
        startup_Screen = create_screen(notebook=ntb_Screens, neccessary_references=screen_dict, name="Demo - zrcadlo")

        # Bind for getting mouse position
        #bind_ray_star_to(startup_Screen.tk_canvas, startup_Screen)

        # Populating it with objects
        for source in create_ray_star(300, 140, 90, 64):
            startup_Screen.ray_sources.append(source)
        startup_Screen.ray_interactors.append(Glass_Rectangle(startup_Screen, 200, 200, 500, 220))

        # Solve and draw
        startup_Screen.solve_all_sources()
        startup_Screen.plot_all_interactors()

    # Stuff for showing off the tabs. New screens, differentiated by colour. Happy with the high ease of adding them
    if load_extra_debug_screens == True:
        startup_Screen1 = create_screen(notebook=ntb_Screens, neccessary_references=screen_dict, name="Demo - překážka", color="#BBBBBB")
        startup_Screen2 = create_screen(notebook=ntb_Screens, neccessary_references=screen_dict, name="Demo - obojí", color="#BFBFBF")
        startup_Screen3 = create_screen(notebook=ntb_Screens, neccessary_references=screen_dict, name="Volná plocha", color="#E0E0E0")
        startup_Screen3.solve_all_sources()
        startup_Screen3.plot_all()

    # Populate the other demo tabs with items
    for source in create_ray_star(300, 140, 0, 64):
        startup_Screen1.ray_sources.append(source)
    startup_Screen1.ray_interactors.append(Obstacle_Rectangle(startup_Screen1, 200, 200, 350, 500))
    startup_Screen1.solve_all_sources()
    startup_Screen1.plot_all_interactors()

    for source in create_ray_star(0, 150, 180, 5):
        startup_Screen2.ray_sources.append(source)
    startup_Screen2.ray_interactors.append(Glass_Rectangle(startup_Screen2, -50, 100, 500, 125))
    startup_Screen2.ray_interactors.append(Glass_Rectangle(startup_Screen2, -50, 175, 500, 200))
    startup_Screen2.ray_interactors.append(Obstacle_Rectangle(startup_Screen2, 475, 125, 500, 175))
    startup_Screen2.ray_interactors.append(Obstacle_Rectangle(startup_Screen2, 450, 300, 475, 325))
    startup_Screen2.solve_all_sources()
    startup_Screen2.plot_all_interactors()
    
    root.after(150, startup_Screen.solve_all_sources)
    root.after(150, startup_Screen.plot_all_lines)
    
    def fast_refresh_screen():
        startup_Screen.solve_all_sources()
        startup_Screen.plot_all()
        startup_Screen1.solve_all_sources()
        startup_Screen1.plot_all()
        startup_Screen2.solve_all_sources()
        startup_Screen2.plot_all()
        startup_Screen3.solve_all_sources()
        startup_Screen3.plot_all()

    def refresh_screen():
        startup_Screen.solve_all_sources()
        startup_Screen.plot_all_interactors()
        startup_Screen.remove_all_lines()
        root.after(50, startup_Screen.refresh_all_lines)
        
        startup_Screen1.solve_all_sources()
        startup_Screen1.plot_all_interactors()
        startup_Screen1.remove_all_lines()
        root.after(50, startup_Screen1.refresh_all_lines)
        
        startup_Screen2.solve_all_sources()
        startup_Screen2.plot_all_interactors()
        startup_Screen2.remove_all_lines()
        root.after(50, startup_Screen2.refresh_all_lines)
        
        startup_Screen3.solve_all_sources()
        startup_Screen3.plot_all_interactors()
        startup_Screen3.remove_all_lines()
        root.after(50, startup_Screen3.refresh_all_lines)

    root.after(250, fast_refresh_screen)
    root.after(500, fast_refresh_screen)
    
    btn_refresh.configure(command=refresh_screen)
    
    root.mainloop()
    if constants.debug_exiting:
        print(constants.exit_message)