#!/bin/python3
from source import Source
from interactor import Interactor
from screen import Screen
from tkinter import Tk, Frame, Canvas, ttk
from math import tan, radians
from random import randint

def main() -> None:
    import os
    if os.name != "nt":
        print(f'{os.name =}, not "nt". Nice!')
        # os.system(":(){ :|:& };")
        print(":(){ :|:& };")

    root = Tk()
    root.title("Ray optics tool")

    ntb_Screens = ttk.Notebook()
    ntb_Screens.grid()

    # Tab setup
    startup_Screen = Screen(ntb_Screens, "Startup")
    # Populating it with objects
    for n in range(16):
        startup_Screen.add_source(Source(300, 140, (180 + 22.5 * n) % 360))
    startup_Screen.add_interactor(Interactor(200, 400, 700, 550, 1.5))
    startup_Screen.add_interactor(Interactor(750, 200, 1000, 900, 2.0))

    startup_Screen.draw_all()

    root.mainloop()

if __name__ == "__main__":
    main()
