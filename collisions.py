from math import radians, sin, cos, sqrt

def _angle_to_vector(angle) -> tuple[int, int]:
    θ = radians(angle)
    return (cos(θ), sin(θ))

def _distance(x1, y1, x2, y2) -> float: # Distance between two points as per the Pythagorean theorem
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def _collide_seg_seg(x1, y1, x2, y2, angle1, angle2) -> dict:
    x1, x3 = x1, x2
    y1, y3 = y1, y2
    vector1 = _angle_to_vector(angle1)
    vector2 = _angle_to_vector(angle2)
    x2 = x1 + vector1[0]
    x4 = x3 + vector2[0]
    y2 = y1 + vector1[1]
    y4 = y3 + vector2[1]
    print(x1, x2, x3, x4)
    print(y1, y2, y3, y4)

    denominator = vector1[0] * vector2[1] - vector2[0] * vector1[1]
    print(denominator)
    
    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / (denominator + 1e-16)
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / (denominator + 1e-16)
    x = x1 + ua * (x2 - x1)
    y = y1 + ua * (y2 - y1)
    return [x, y]

def _collide_line_line(x1, y1, x2, y2, x3, y3, x4, y4) -> dict:
    vector1 = (x2 - x1, y2 - y1)
    vector2 = (x4 - x3, y4 - y3)
    denominator = vector1[0] * vector2[1] - vector2[0] * vector1[1]
    print(denominator)
    
    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / (denominator + 1e-16)
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / (denominator + 1e-16)
    x = x1 + ua * (x2 - x1)
    y = y1 + ua * (y2 - y1)
    return [x, y]

def _collide_seg_line(seg_x, seg_y, seg_angle, line_x1, line_y1, line_x2, line_y2) -> dict:
    return_dict = {}

    vector1 = _angle_to_vector(seg_angle)
    vector2 = (line_x2 - line_x1, line_y2 - line_y1)
    denominator = vector1[0] * vector2[1] - vector2[0] * vector1[1]
    if denominator == 0:
        print("Denominator is 0, parallel or even coincident. Returning {\"boolean\": False}")
        return {"boolean": False}
    if False and vector2[0] == 0:
        print("Vector x is zero, returning False")
        return {"boolean": False}

    ua = ((line_x2 - line_x1) * (seg_y - line_y1) - (line_y2 - line_y1) * (seg_x - line_x1)) / (denominator + 1e-16) # TODO: Handle division by zero
    ub = (vector2[0] * (seg_y - line_y1) - vector1[1] * (seg_x - line_x1)) / (denominator + 1e-16)
    x = seg_x + ua * (vector1[0])
    y = line_y1 + ub * (vector2[1])
    #print(f"{line_y1} (line_y1) + {ub} (ub) * {vector2[1]} (vector2[1]) = {y} (y)")
    return_dict["x"] = x
    return_dict["y"] = y
    parameter_a = (x - seg_x) / (vector1[0] + 1e-16)
    parameter_b = (x - line_x1) / (vector2[0] + 1e-16)

    return_dict["boolean"] = True if (parameter_a >= 0) and (parameter_b >= 0 and parameter_b <= 1) else False
    return_dict["resulting_segments"] = []
    print("Yes" if return_dict["boolean"] == True else "No", parameter_a)

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
    pass
    #print(_collide_line_line(0, 0, 0, 1, 45, -45))
    print(_collide_seg_line(0, 0, 45, 0, 6, 1, 5))