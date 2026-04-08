from math import radians, sin, cos, sqrt, atan2, degrees
from core_classes import Segment

def _angle_to_vector(angle) -> tuple[int, int]:
    θ = radians(angle)
    x = cos(θ)
    y = sin(θ)
    if False and x < 1e-16:
        x = 0
    if False and y < 1e-16:
        y = 0   
    return (x, y)

def _distance(x1, y1, x2, y2) -> float: # Distance between two points as per the Pythagorean theorem
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def _get_reflected_angle(seg_angle: float, line_angle: float) -> float:
    #print(f"Getting reflected angle for seg_angle {seg_angle} line_angle {line_angle}")
    # Input protection
    if not (seg_angle >= 0 and seg_angle <= 360):
        print(f"WARN [_get_reflected_angle]: seg_angle {seg_angle} not within 0 to 360, changing")
        seg_angle = seg_angle % 360
    if not (line_angle >= 0 and line_angle <= 360):
        print(f"WARN [_get_reflected_angle]: line_angle {line_angle} not within 0 to 360, changing")
        line_angle = line_angle % 360

    # Get the angle of the normal line, facing *into* the medium off of which it is reflecting
    if seg_angle >= 90 and seg_angle <= 180:
        normal_angle = line_angle + 90
    else:
        normal_angle = line_angle - 90
    
    # Calculate reflected angle
    x = normal_angle - seg_angle
    answer = normal_angle + 180 + x

    # Normalise and return the answer
    if answer >= 360:
        pass
        #print("WARN [_get_reflected_angle]: Result over 360, reducing")
    answer = answer % 360
    return answer

def _collide_seg_line(seg_x, seg_y, seg_angle, line_x1, line_y1, line_x2, line_y2) -> dict:
    return_dict = {}

    # Do intermediate calculations 1
    vector_seg = _angle_to_vector(seg_angle)
    vector_line = (line_x2 - line_x1, line_y2 - line_y1)
    denominator = vector_seg[0] * vector_line[1] - vector_line[0] * vector_seg[1]
    #print(vector_seg, vector_line, denominator)

    # Detect parallel and coincident lines that do not collide
    if denominator == 0:
        #print("Denominator is 0, parallel, or coincident while not actually on the box edge. Returning {\"boolean\": False}")
        return {"boolean": False}

    # Do intermediate calculations 2
    ua = (vector_line[0] * (seg_y - line_y1) - vector_line[1] * (seg_x - line_x1)) / (denominator)

    # Do collision coordinates calculation
    x = seg_x + ua * (vector_seg[0])
    y = seg_y + ua * (vector_seg[1])

    # Detect lack of collision
    parameter_a = (x - seg_x) / (vector_seg[0]) if abs(vector_seg[0]) > abs(vector_seg[1]) else (y - seg_y) / (vector_seg[1]) # The right calculation is in case segment is vertical
    parameter_b = (x - line_x1) / (vector_line[0]) if vector_line[0] != 0 else (y - line_y1) / (vector_line[1]) # The right calculation is in case line is vertical
    if (parameter_a >= 0) and (parameter_b >= 0 and parameter_b <= 1): # Set the collision as collided if the segment's vector goes in the correct direction and the point is in range on the line
        return_dict["boolean"] = True
    else: # Else, return no collision
        return {"boolean": False}

    return_dict["line_angle"] = degrees( atan2(vector_line[1], vector_line[0]) )

    # Fill in the return dictionary with correct values
    return_dict["x"] = x
    return_dict["y"] = y
    return_dict["distance_from_start"] = _distance(seg_x, seg_y, x, y)
    #print("Line angle ", return_dict["line_angle"], " Distance ", return_dict["distance_from_start"])
    if y < 140:
        breakpoint
    #print(parameter_a)

    return return_dict

def collide_seg_box(seg_x, seg_y, seg_angle, box_x1, box_y1, box_x2, box_y2, same_interactor: bool, last_collided_line: int) -> dict:
    return_dict = {}

    # Determine the collision type. This bit is a point-and-box collision
    if seg_x > box_x1 and seg_x < box_x2  and  seg_y > box_y1 and seg_y < box_y2: # The segment originates in the box
        return_dict["type"] = "internal"
        return{"boolean": True, "hide_original_segment": True, "distance_from_start": 0, "resulting_segments": [], "x": seg_x, "y": seg_y}
    elif (seg_x == box_x1 or seg_x == box_x2) and (seg_y == box_y1 or seg_y == box_y2): # The segment originates on the corner of the box
        return_dict["type"] = "corner"
        return{"boolean": False}
        # TODO: Decide what to do when hitting the exact corner of the box
    elif ((seg_x == box_x1 or seg_x == box_x2) and (seg_y >= box_y1 and seg_y <= box_y2))  or  ((seg_y == box_y1 or seg_y == box_y2) and (seg_x >= box_x1 and seg_x <= box_x2)): # The segment originates on the edge of the box
        return_dict["type"] = "edge"
        #print("WARN")
        return{"boolean": False} # TODO: This might be what is messing up the internal reflections
        # TODO: add handling of edge collisions
    elif seg_x < box_x1 or seg_x > box_x2 or seg_y < box_y1 or seg_y > box_y2: # The segment originates outside of the box
        return_dict["type"] = "external"
    else: # For testing, to catch in case I'm not testing edge cases correctly
        raise Exception("Edge case in point-and-box collision")
    #print(return_dict["type"])    

    # Get collision with each of the four lines
    candidate_collisions = []
    for line_num, candidate_collision in enumerate([
    _collide_seg_line(seg_x, seg_y, seg_angle, box_x1, box_y1, box_x2, box_y1), # Top horizontal line (lower y than the bottom one)
    _collide_seg_line(seg_x, seg_y, seg_angle, box_x1, box_y2, box_x2, box_y2), # Bottom horizontal line (higher y than the top one)
    _collide_seg_line(seg_x, seg_y, seg_angle, box_x1, box_y1, box_x1, box_y2), # Left vertical line
    _collide_seg_line(seg_x, seg_y, seg_angle, box_x2, box_y1, box_x2, box_y2)  # Right vertical line
    ]):
        #if (same_interactor and last_collided_line == line_num):
            #print("Discarding due to same interactor and line")
        if candidate_collision["boolean"] == True and candidate_collision["distance_from_start"] > 0 and not (same_interactor and last_collided_line == line_num): # Check collision for criteria
            candidate_collision["origin_line"] = line_num
            #print(candidate_collision["origin_line"], last_collided_interactor, last_collided_line)
            candidate_collisions.append(candidate_collision)
    #print(f"Top line: {_collide_seg_line(seg_x, seg_y, seg_angle, box_x1, box_y1, box_x2, box_y1)}")

    # If empty, no collision
    if candidate_collisions == []:
        return{"boolean": False}
    
    # Accept nearest collision
    accepted_collision = min(candidate_collisions, key= lambda collision: collision["distance_from_start"])
    #print("Set origin line to ", accepted_collision["origin_line"])

    # Correctly set up the return dictionary
    return_dict["boolean"] = True # If this code is reached, a collision that has boolean:True was accepted
    return_dict["x"] = accepted_collision["x"]
    return_dict["y"] = accepted_collision["y"]
    return_dict["distance_from_start"] = _distance(seg_x, seg_y, return_dict["x"], return_dict["y"])
    return_dict["origin_line"] = accepted_collision["origin_line"]
    
    # Create the resulting segments
    return_dict["resulting_segments"] = [] # If only blocking should take place, it's just this
    # If reflection should take place:
    new_angle = _get_reflected_angle(seg_angle, accepted_collision["line_angle"])
    return_dict["resulting_segments"] = [Segment(accepted_collision["x"], accepted_collision["y"], new_angle)]
    # If refraction should take place:
    # TODO: Add snell's law here
    #return_dict["resulting_segments"] = []

    #print(f"Returning collision dictionary {return_dict}") # TODO: Add more debug constants
    return return_dict

if __name__ == "__main__":
    print("Testing conversion of angles to vectors:")
    for x in range(0, 360, 90):
        x = x + 45 + 360 # To test angles that are over 360
        vector = _angle_to_vector(x)
        print(f"Angle: {x} Vector: ({round(vector[0], 1)}, {round(vector[1], 1)})")
    print(_collide_seg_line(0, 0, 90, -10, 100, 100, 100))
    print(collide_seg_box(0, 0, 90, -10, -100, 100, 200, True, None))