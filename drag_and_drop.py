from core_classes import Screen
from tkinter import Event
from constants import selection_mode, single_select_offset, select_all_interactors_near_offset, lines_select_offset

def on_enter(event):
    print("Running")
    print(locals())

def get_mouse_selected(event: Event, screen: Screen) -> list[int]:
    global selection_mode
    match selection_mode:
        case "SINGLE_SELECT":
            offset = single_select_offset
        case _:
            raise Exception("Selection mode does not match expected cases")
        
    x0 = event.x - offset
    x1 = event.x + offset
    y0 = event.y - offset
    y1 = event.y + offset
    overlapping = screen.tk_canvas.find_overlapping(x0, y0, x1, y1)    
    return overlapping

def on_mouse_grab(event: Event, screen: Screen) -> None: # Updates globals
    global selected_item_IDs
    global selection_original_coords
    selected_item_IDs = get_mouse_selected(event, screen)
    selection_original_coords = (event.x, event.y)

def on_mouse_drag(event: Event, screen: Screen) -> None: # Moves stuff on the given screen and calls for an update
    # Move stuff on the canvas
    global selection_original_coords
    move_x = event.x - selection_original_coords[0]
    move_y = event.y - selection_original_coords[1]
    for id in selected_item_IDs:
        screen.tk_canvas.move(id, move_x, move_y)
    selection_original_coords = (event.x, event.y)

    # Move stuff internally
    # Oh no...

    # Call for an update
    screen.solve_collisions()
    screen.plot_all_lines()