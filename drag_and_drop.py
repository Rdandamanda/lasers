import constants
from core_classes import Screen
from tkinter import Event

def on_enter(event):
    print("Running")
    print(locals())

def get_mouse_selected(event: Event, screen: Screen) -> list[int]:
    match constants.selection_mode:
        case "SINGLE_SELECT":
            offset = constants.single_select_offset
        case _:
            raise Exception("Selection mode does not match expected cases")
        
    x0 = event.x - offset
    x1 = event.x + offset
    y0 = event.y - offset
    y1 = event.y + offset
    overlapping = screen.tk_canvas.find_overlapping(x0, y0, x1, y1)

    # Filter answer to only include rectangles
    answer = []
    for id in overlapping:
        if screen.tk_canvas.type(id) == "rectangle":
            answer.append(id)
    
    return answer

def on_mouse_grab(event: Event, screen: Screen) -> None: # Updates variables in the constants module # TODO: this sounds terrible, those should probably be moved somewhere else, maybe make something for my program that is like a Tk() in Tkinter
    constants.selected_item_IDs = get_mouse_selected(event, screen)

    for id in constants.selected_item_IDs:
        constants.selected_item_internal_objects.append( screen.ID_to_interactor_dict[id] )
        
    constants.selection_original_coords = (event.x, event.y)

def on_mouse_drag(event: Event, screen: Screen) -> None: # Moves stuff on the given screen and calls for an update
    # Move stuff on the canvas
    move_x = event.x - constants.selection_original_coords[0]
    move_y = event.y - constants.selection_original_coords[1]
    for id in constants.selected_item_IDs: # TODO: Figure out how this works without a "global" declaration in this function
        screen.tk_canvas.move(id, move_x, move_y)
    constants.selection_original_coords = (event.x, event.y)

    # Move stuff internally
    # Oh no...
    for obj in constants.selected_item_internal_objects:
        obj.move(move_x, move_y)

    # Call for an update
    screen.solve_all_sources()
    screen.plot_all_lines()
    screen.plot_all_interactors()