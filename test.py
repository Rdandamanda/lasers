from main import *

class Self():
    x0 = 0
    y0 = 100
    x1 = 500
    y1 = 200

testray = Segment(0, 0, 45)
self = Self()

# Collide between 0 and 90°
def col_test(self, ray: Segment):
    # Collide with horizontal line:
    dy = self.y0 - ray.start_y
    return_list = []
    if dy > 0:
        dx = (1/tan(radians(ray.angle))) * dy
        print('dy: ', dy, "dx: ", dx)
        potential_endx = ray.start_x + dx
        potential_endy = ray.start_y + dy
        if self.x0 < potential_endx and potential_endx < self.x1:
            return_list.append(Segment(potential_endx, potential_endy, 360 - ray.angle))

    return return_list

for s in col_test(self, testray):
    print(s)