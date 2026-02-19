from constants import load_debug_screen, load_extra_debug_screens
from core_classes import *
from default_interactors import *
from default_sources import *

do_os_check()

if __name__ == "__main__":
    # GUI setup
    root = Tk()
    root.title("Ray optics tool")

    ntb_Screens = ttk.Notebook()
    ntb_Screens.grid()

    # The debug screen
    if load_debug_screen == True:
        # Tab setup
        startup_Screen = Screen()
        ntb_Screens.add(startup_Screen.tk_frame, text="Debug Screen")

        # Bind for getting mouse position
        bind_ray_star_to(root, startup_Screen)

        # Populating it with objects
        for source in create_ray_star(300, 140, 5):
            startup_Screen.ray_sources.append(source)
        startup_Screen.ray_interactors.append(o := Glass_Rectangle(200, 200, 500, 350))
        #startup_Screen.tk_canvas.tag_bind(o.canvas_rectangle, "<Enter>", on_enter)
        del o
        startup_Screen.ray_interactors.append(Glass_Rectangle(50, 50, 75, 75))

        # Solve and draw
        startup_Screen.solve_collisions()
        startup_Screen.plot_all()

    # Stuff for showing off the tabs. New screens, differentiated by colour. Happy with the high ease of adding them
    if load_extra_debug_screens == True:
        startup_Screen1 = Screen()
        startup_Screen1.tk_canvas.configure(bg="yellow")
        ntb_Screens.add(startup_Screen1.tk_frame, text="Další plocha")
        startup_Screen1.solve_collisions()
        startup_Screen1.plot_all()
        startup_Screen2 = Screen()
        startup_Screen2.tk_canvas.configure(bg="lavender")
        ntb_Screens.add(startup_Screen2.tk_frame, text="Plocha 3")
        startup_Screen2.solve_collisions()
        startup_Screen2.plot_all()

    root.mainloop()