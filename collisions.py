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

    ua = ((line_x2 - line_x1) * (seg_y - line_y1) - (line_y2 - line_y1) * (seg_x - line_x1)) / (denominator + 1e-16) # TODO: Handle division by zero
    ub = (vector2[0] * (seg_y - line_y1) - vector1[1] * (seg_x - line_x1)) / (denominator + 1e-16)
    x = seg_x + ua * (vector1[0])
    y = line_y1 + ub * (vector2[1])
    #print(f"{line_y1} (line_y1) + {ub} (ub) * {vector2[1]} (vector2[1]) = {y} (y)")
    return_dict["x"] = x
    return_dict["y"] = y
    parameter_a = (x - seg_x) / vector1[0]
    parameter_b = (x - line_x1) / vector2[0]

    return_dict["boolean"] = True if (parameter_a >= 0) and (parameter_b >= 0 and parameter_b <= 1) else False
    return_dict["resulting_segments"] = []
    print("Yes" if return_dict["boolean"] == True else "No", parameter_a)

    return return_dict
    
def collide_line_box(line_x, line_y, line_angle, box_x1, box_y1, box_x2, box_y2) -> dict:
    return_dict = {}

    if line_x > box_x1 and line_x < box_x2  and  line_y > box_y1 and line_y < box_y2: # The line originates in the box
        return_dict["type"] = "internal"
    elif (line_x == box_x1 or line_x == box_x2  and  line_y == box_y1 or line_y == box_y2): # The line originates on the edge of the box
        return_dict["type"] = "edge"
    elif line_x < box_x1 or line_x > box_x2 or line_y < box_y1 or line_y > box_y2: # The line originates outside of the box
        return_dict["type"] = "external"
    else: # For testing, to catch in case I'm not testing edge cases correctly
        raise Exception("Edge case in point-and-box collision")
    
    candidate_collisions = []
    candidate_collisions.append(_collide_seg_line(line_x, line_y, line_angle, box_x1, box_y1, box_x2, box_y1))
    accepted_collision = candidate_collisions[0]
    if accepted_collision["boolean"] == False:
        return {"boolean": False} # TODO: Change

    """return_dict["boolean"] = True
    return_dict["resulting_segments"] = []
    return_dict["x"] = accepted_collision["x"]
    return_dict["y"] = accepted_collision["y"]"""
    return_dict = accepted_collision
    return_dict["distance_from_start"] = _distance(line_x, line_y, return_dict["x"], return_dict["y"])

    print(f"Returning collision dictionary {return_dict}")
    return return_dict

if __name__ == "__main__":
    # TODO: Add test cases here
    pass
    #print(_collide_line_line(0, 0, 0, 1, 45, -45))
    print(_collide_seg_line(0, 0, 45, 0, 6, 1, 5))