## Constant

## Can be changed
# Any
load_debug_screen = True
load_extra_debug_screens = True
debug_level = 1
max_segments = 1000
star_spokes_power_of_2 = 8

colour_intermediate = "blue"
colour_final = "blue"

# Selection behaviour
single_select_offset = 0
select_all_interactors_near_offset = 20
lines_select_offset = 40

## Internal
global selection_mode
selection_mode = "SINGLE_SELECT" # "SELECT_ALL_INTERACTORS_NEAR", "LINES_SELECT"
global selected_item_IDs
selcted_item_IDs = []
global selection_original_coords
selection_original_coords = (None, None)