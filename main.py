from constants import load_debug_screen, load_extra_debug_screens, monospace_font_of_choice
from core_classes import *
from default_interactors import *
from default_sources import *

from tkinter import ttk
do_os_check()

if __name__ == "__main__":
    # GUI setup
    root = tk.Tk()
    root.title("Ray optics tool")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    font_of_choice_available: bool = do_font_check() # Tohle potřebuje být až tady, protože to potřebuje, aby existovala instance Tk()

    menubar = tk.Menu(root)
    menubar.add_command(label="Soubor")
    menubar.add_command(label="Zavřít", command=root.quit)
    root.configure(menu=menubar)

    pnw_panes = ttk.Panedwindow(master=root, orient=tk.HORIZONTAL)
    pnw_panes.grid(sticky="nsew", row=0, column=0)

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

    lbl_debug = tk.Label(master=frm_screens)
    if font_of_choice_available:
        lbl_debug.configure(font=(monospace_font_of_choice, 10))
    lbl_debug.grid(sticky="ew")

    grp_grip = ttk.Sizegrip(master=frm_screens)
    grp_grip.grid(column=1, row=1, sticky="ns")

    # The debug screen
    if load_debug_screen == True:
        # Tab setup
        screen_dict: dict = {"lbl_debug": lbl_debug}
        startup_Screen = Screen(neccessary_references=screen_dict)
        ntb_Screens.add(startup_Screen.tk_frame, text="Debug Screen")

        # Bind for getting mouse position
        #bind_ray_star_to(startup_Screen.tk_canvas, startup_Screen)

        # Populating it with objects
        for source in create_ray_star(300, 140, 5):
            startup_Screen.ray_sources.append(source)
        startup_Screen.ray_interactors.append(o := Glass_Rectangle(startup_Screen, 200, 200, 500, 350))
        #startup_Screen.tk_canvas.tag_bind(o.canvas_rectangle, "<Enter>", on_enter)
        del o
        startup_Screen.ray_interactors.append(Glass_Rectangle(startup_Screen, 50, 50, 75, 75))

        # Solve and draw
        startup_Screen.solve_all_sources()
        startup_Screen.plot_all()

    # Stuff for showing off the tabs. New screens, differentiated by colour. Happy with the high ease of adding them
    if load_extra_debug_screens == True:
        startup_Screen1 = Screen(neccessary_references=screen_dict)
        startup_Screen1.tk_canvas.configure(bg="yellow")
        ntb_Screens.add(startup_Screen1.tk_frame, text="Další plocha")
        startup_Screen1.solve_all_sources()
        startup_Screen1.plot_all()
        startup_Screen2 = Screen(neccessary_references=screen_dict)
        startup_Screen2.tk_canvas.configure(bg="lavender")
        ntb_Screens.add(startup_Screen2.tk_frame, text="Plocha 3")
        startup_Screen2.solve_all_sources()
        startup_Screen2.plot_all()

    root.mainloop()
    if constants.debug_level >= 1:
        print("Úspěšně ukončeno")