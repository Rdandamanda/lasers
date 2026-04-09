## Constant
from typing import TYPE_CHECKING

## Can be changed
# Any
load_debug_screen = True
load_extra_debug_screens = True
star_spokes_power_of_2 = 8

# Debug and limits:
debug_level = 1 # 1: Warnings
debug_background_colors = False # Gives vibrant colours to frames that shouldn't have visible backgrounds
max_segments = 20 # Maximum number of segments per source

# Customisation
color_line_standard = "blue"

justify_digits = 4 # Input for the rjust() function in in the formatted string for the debug Label
monospace_font_of_choice = "Miriam Mono CLM"
czech_debug_label = True
if czech_debug_label:
    monospace_font_of_choice = "Cascadia Code Light" # Czech-compatible font

# Selection behaviour
single_select_offset = 0
select_all_interactors_near_offset = 20
lines_select_offset = 40

## Internal
selection_mode = "SINGLE_SELECT" # "SELECT_ALL_INTERACTORS_NEAR", "LINES_SELECT"
selected_item_IDs = []
selected_internal_objects = []
selection_original_coords = (None, None)
editing_item = None