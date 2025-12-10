#!/bin/python3
from source import Source
from interactor import Interactor, Mirror
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
    for n in range(0, 720, 10):
        startup_Screen.add_source(Source(300, 140, (n / 2) % 360, "red", 4))
    startup_Screen.add_interactor(Mirror(100, 250, 1200, 300))

    startup_Screen.draw_all()

    root.mainloop()

if __name__ == "__main__":
    main()
