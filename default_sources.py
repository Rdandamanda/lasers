from core_classes import *

def bind_ray_star_to(tk_object, screen) -> None:
    tk_object.ray_star_source_ids = []
    tk_object.bind("<Motion>", lambda event: replace_ray_star_to_cursor(event=event, tk_object=tk_object, screen=screen, spokes=8))

def replace_ray_star_to_cursor(event, tk_object, screen: Screen, spokes) -> None:
    # Remove previously generated ray sources by Python object UUID
    # TODO: What the hell?
    # After a day of thinking, I came to the conclusion it's already time to add groupings of objects. Got a few very exciting ideas for those for later, too
    i = 0
    while i < len(screen.ray_sources):
        if id(screen.ray_sources[i]) in tk_object.ray_star_source_ids:
            screen.ray_sources.pop(i)
        else: # This. Was. A. Terrible error to find
            i += 1
    
    # Generate new sources
    generated_sources = create_ray_star(event.x, event.y, spokes)

    # Get and save the ids
    tk_object.ray_star_source_ids = [] # This can be cleared now
    for source in generated_sources:
        tk_object.ray_star_source_ids.append(id(source))
        screen.ray_sources.append(source)
    
    # Transfer the generated sources to the screen
    screen.solve_collisions()
    screen.plot_all_lines()

def create_ray_star(x, y, spokes: int) -> list[Source]:
    #Input protection
    if spokes < 0:
        raise Exception("Cannot have a negative number of spokes")
    if spokes == 0:
        return []
    
    output_ray_sources = []
    d_angle = 360 / spokes
    for n in range(spokes):
        output_ray_sources.append(Source(x, y, (d_angle*n)%360))
    return output_ray_sources