## Constant
from typing import TYPE_CHECKING

## Can be changed
# Any
load_debug_screen = True
load_extra_debug_screens = True
star_spokes_power_of_2 = 8

# Debug and limits:
debug_any: bool = True # Master option. If False, turns off all debugging (except the exit message)
debug_warnings: bool = True # Warnings in the console of type "WARN: "
debug_background_colors: bool = True # Gives vibrant colours to frames that shouldn't have visible backgrounds
debug_selection: bool = True # Prints currently selected and currently edited item(s) into the console any time anything is selected
debug_exiting: bool = True # Whether to print the exit message upon successfully exiting the program
exit_message = "Úspěšně ukončeno"

max_segments: int = 20 # Maximum number of segments per source

if debug_any == False:
    debug_warnings = False
    debug_background_colors = False
    debug_selection = False
    max_segments = max(max_segments, 200) # Makes max_segments at least 200

# Customisation
color_line_standard = "blue"

justify_digits = 4 # Input for the rjust() function in in the formatted string for the debug Label
monospace_font_of_choice = "Miriam Mono CLM"
czech_debug_label = True
if czech_debug_label:
    monospace_font_of_choice = "Cascadia Code Light" # Czech-compatible font

# Selection behaviour
single_select_offset = 0
multi_select_offset = 0
lines_select_offset = 10

## Internal
# Drag n' drop
selection_mode = "SINGLE" # "SINGLE": drags and edits one interactor, "MULTI": drags all under cursor, finds topmost for editing, "LINES": selects lines
selected_item_IDs = []
selected_internal_objects = []
selection_original_coords = (None, None)
editing_item = None