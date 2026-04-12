import constants
from core_classes import Screen, update_editing_panel

from tkinter import Event
from math import sqrt

def _distance(x1, y1, x2, y2) -> float: # Distance between two points as per the Pythagorean theorem
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def get_mouse_selected(event: Event, screen: Screen) -> list[int]:
    # Set variables based on selection mode
    selection_mode = constants.selection_mode
    match selection_mode:
        case "SINGLE":
            offset = constants.single_select_offset
        case "MULTI":
            offset = constants.multi_select_offset
        case "LINES":
            offset = constants.lines_select_offset
        case _:
            raise Exception("Selection mode does not match expected cases")
        
    x0 = event.x - offset
    x1 = event.x + offset
    y0 = event.y - offset
    y1 = event.y + offset
    overlapping = screen.tk_canvas.find_overlapping(x0, y0, x1, y1) # From the documentation for tk.Canvas.find_overlapping(): "The items are returned in stacking order, with the lowest item first" 

    if len(overlapping) == 0: # If nothing selected, nothing selected
        return []

    # Create answer list based on selection mode
    answer = []
    for id in overlapping:
        if selection_mode == "LINES":
            # Filter answer to only include lines
            if screen.tk_canvas.type(id) == "line":
                answer.append(id)
        else:
            # Filter answer to only include rectangles # TODO: Make this work off of the tag system instead, since some interactors will not be rectangles
            if screen.tk_canvas.type(id) == "rectangle":
                answer.append(id)
    
    match selection_mode:
        case "SINGLE":
            return [overlapping[-1]] # This returns the topmost item (contained in a list)
        case "MULTI":
            return answer
        case "LINES":
            return answer
    
    return answer # Ideally, unreachable

def on_mouse_grab(event: Event, screen: Screen) -> None: # Updates variables in the constants module
    # Store event coordinates so that dragging works
    constants.selection_original_coords = (event.x, event.y)

    # Get the selected items
    constants.selected_item_IDs = get_mouse_selected(event, screen)

    # Create the constants.selected_internal_objects list according to the selection mode
    # Also set the item for the editing panel according to the selection mode
    if constants.selected_item_IDs == []: # If nothing selected, nothing selected
        constants.selected_internal_objects = []
        constants.editing_item = None
    else: # This can now count on at least something being selected (Or something having gone quite wrong)
        constants.selected_internal_objects = []

        selection_mode = constants.selection_mode
        match selection_mode:
            case "SINGLE":
                # Just one is selected anyway
                constants.selected_internal_objects.append( screen.ID_to_interactor_dict[constants.selected_item_IDs[0]] )
                constants.editing_item = constants.selected_internal_objects[0]
            case "MULTI":
                for id in constants.selected_item_IDs:
                    constants.selected_internal_objects.append( screen.ID_to_interactor_dict[id] )
                constants.editing_item = constants.selected_internal_objects[-1] # The topmost one in the canvas draw order
            case "LINES":
                pass # TODO: Implement lines
            case _:
                raise Exception("Selection mode does not match expected cases")

    # Update the editing label
    update_editing_panel(screen)

    if constants.debug_selection:
        len_1 = len(constants.selected_item_IDs)
        len_2 = len(constants.selected_internal_objects)
        print(f"{len_1} selected_item_IDs = {constants.selected_item_IDs}\n{len_2} selected_internal_objects = {constants.selected_internal_objects}\nediting_item = {constants.editing_item}\n- - -")

def on_mouse_drag(event: Event, screen: Screen) -> None: # Moves stuff on the given screen and calls for an update
    # Doesn't need to run if nothing is being dragged
    if constants.selected_internal_objects == []:
        return
    
    # Move stuff on the canvas
    move_x = event.x - constants.selection_original_coords[0]
    move_y = event.y - constants.selection_original_coords[1]
    for id in constants.selected_item_IDs: # TODO: Figure out how this works without a "global" declaration in this function
        screen.tk_canvas.move(id, move_x, move_y)
    constants.selection_original_coords = (event.x, event.y)

    # Move stuff internally
    # Oh no...
    for obj in constants.selected_internal_objects:
        obj.move(move_x, move_y)

    # Call for an update
    screen.solve_all_sources()
    screen.plot_all_lines()