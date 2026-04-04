from math import radians, sin, cos, sqrt

def _angle_to_vector(angle) -> tuple[int, int]:
    θ = radians(angle)
    return (cos(θ), sin(θ))

def _distance(x1, y1, x2, y2) -> float: # Distance between two points as per the Pythagorean theorem
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def _collide_seg_line(seg_x, seg_y, seg_angle, line_x1, line_y1, line_x2, line_y2) -> dict:
    return_dict = {}

    # Do intermediate calculations 1
    vector_seg = _angle_to_vector(seg_angle)
    vector_line = (line_x2 - line_x1, line_y2 - line_y1)
    denominator = vector_seg[0] * vector_line[1] - vector_line[0] * vector_seg[1]

    # Detect pararell and coincident lines that do not collide
    if denominator == 0:
        #print("Denominator is 0, parallel, or coincident while not actually on the box edge. Returning {\"boolean\": False}")
        return {"boolean": False}

    # Do intermediate calculations 2
    ua = (vector_line[0] * (seg_y - line_y1) - vector_line[1] * (seg_x - line_x1)) / (denominator)

    # Do final calculation
    x = seg_x + ua * (vector_seg[0])
    y = seg_y + ua * (vector_seg[1])

    # Detect lack of collision
    parameter_a = (x - seg_x) / (vector_seg[0]) if vector_seg[0] != 0 else (y - seg_y) / (vector_seg[1]) # The right calculation is in case segment is vertical
    parameter_b = (x - line_x1) / (vector_line[0]) if vector_line[0] != 0 else (y - line_y1) / (vector_line[1]) # The right calculation is in case line is vertical
    if (parameter_a >= 0) and (parameter_b >= 0 and parameter_b <= 1): # Set the collision as collided if the segment's vector goes in the correct direction and the point is in range on the line
        return_dict["boolean"] = True
    else: # Else, return no collision
        return {"boolean": False}

    # Fill in the return dictionary with correct values
    return_dict["x"] = x
    return_dict["y"] = y
    return_dict["distance_from_start"] = _distance(seg_x, seg_y, x, y)

    return return_dict

def collide_seg_box(seg_x, seg_y, seg_angle, box_x1, box_y1, box_x2, box_y2) -> dict:
    return_dict = {}

    # TODO: Decide what to do when hitting the exact corner of the box

    # Determine the collision type. This bit is a point-and-box collision
    if seg_x > box_x1 and seg_x < box_x2  and  seg_y > box_y1 and seg_y < box_y2: # The segment originates in the box
        return_dict["type"] = "internal"
    elif (seg_x == box_x1 or seg_x == box_x2  and  seg_y == box_y1 or seg_y == box_y2): # The segment originates on the edge of the box
        return_dict["type"] = "edge"
        # TODO: add handling of edge collisions
    elif seg_x < box_x1 or seg_x > box_x2 or seg_y < box_y1 or seg_y > box_y2: # The segment originates outside of the box
        return_dict["type"] = "external"
    else: # For testing, to catch in case I'm not testing edge cases correctly
        raise Exception("Edge case in point-and-box collision")
    
    # Get collision with each of the four lines
    candidate_collisions = []
    for candidate_collision in [
    _collide_seg_line(seg_x, seg_y, seg_angle, box_x1, box_y1, box_x2, box_y1), # Top horizontal line (lower y than the bottom one)
    _collide_seg_line(seg_x, seg_y, seg_angle, box_x1, box_y2, box_x2, box_y2), # Bottom horizontal line (higher y than the top one)
    _collide_seg_line(seg_x, seg_y, seg_angle, box_x1, box_y1, box_x1, box_y2), # Left vertical line
    _collide_seg_line(seg_x, seg_y, seg_angle, box_x2, box_y1, box_x2, box_y2)  # Right vertical line
    ]:
        if candidate_collision["boolean"] == True:
            candidate_collisions.append(candidate_collision)

    # If empty, no collision
    if candidate_collisions == []:
        return{"boolean": False}
    
    # Accept nearest collision
    accepted_collision = min(candidate_collisions, key= lambda collision: collision["distance_from_start"])

    # Correctly set up the return dictionary
    return_dict["boolean"] = True # If this code is reached, a collision that has boolean:True was accepted
    return_dict["x"] = accepted_collision["x"]
    return_dict["y"] = accepted_collision["y"]
    return_dict["distance_from_start"] = _distance(seg_x, seg_y, return_dict["x"], return_dict["y"])
    
    # One thing left, the resulting segments
    return_dict["resulting_segments"] = [] # TODO: Add snell's law here

    #print(f"Returning collision dictionary {return_dict}") # TODO: Add more debug constants
    return return_dict

if __name__ == "__main__":
    # TODO: Add test cases here
    print(_collide_seg_line(0, 0, 45, 0, 6, 1, 5))
    for x in range(0, 360, 45):
        print(_angle_to_vector(x))