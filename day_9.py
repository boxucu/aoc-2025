import matplotlib.pyplot as plt
import time
start_time = time.time()  # Record the start time

# ===== Functions =====
def line_inside_rectangle(points, rect):
    xs = [x for x, y in rect]
    ys = [y for x, y in rect]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    inside = False
    for ind0 in range (0, len(points)):
        ind1 = (ind0 + 1) % len(points)
        x0, y0 = points[ind0]
        x1, y1 = points[ind1]
        # Horizontal line
        if y0 == y1:
            for x in range(min(x0, x1), max(x0, x1) + 1):
                if min_x < x < max_x and min_y < y0 < max_y:
                    inside = True
                    break
        # Vertical line
        elif x0 == x1:
            for y in range(min(y0, y1), max(y0, y1) + 1):
                if min_x < x0 < max_x and min_y < y < max_y:
                    inside = True
                    break
        if inside:
            break

    return inside

def plot_polygon(points):
    if len(points) < 3:
        raise ValueError("A polygon needs at least 3 points.")
    # Extract x and y coordinates + close polygon by adding first point at end
    xs = [p[0] for p in points] + [points[0][0]]
    ys = [p[1] for p in points] + [points[0][1]]

    plt.figure(figsize=(6, 6))
    plt.plot(xs, ys)          # connect vertices
    plt.scatter(xs, ys)       # draw points
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Polygon Visualization")
    plt.axis("equal")         # keep aspect ratio
    plt.grid(True)
    plt.show()

def point_in_polygon(point_unknown, polygon):
    x, y = point_unknown
    inside = False
    n = len(polygon)

    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]  # next vertex

        # Check if point is on a boundary segment
        if ((y2 - y1) * (x - x1) == (x2 - x1) * (y - y1) and
            min(x1, x2) <= x <= max(x1, x2) and
            min(y1, y2) <= y <= max(y1, y2)):
            return True

        # Ray casting: check if edge crosses a horizontal ray to the right of point
        cond1 = (y1 > y) != (y2 > y)
        if cond1:
            x_intersect = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x_intersect >= x:
                inside = not inside

    return inside

def max_area(points):
    areas = {}
    for i in range(len(points)):
        for j in range(i + 1, len(points)):  # ensures no duplicates and no self-pairs
            p1 = points[i]
            p2 = points[j]
            area = (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)
            areas[(p1, p2)] = area
    key_max = max(areas, key=areas.get)
    return areas[key_max], key_max

def create_grid(points, char1, char2):
    max_r = max(row[1] for row in points)
    max_c = max(row[0] for row in points)
    grid = []
    for r in range(0, max_r+1):
        line = ""
        for c in range(0, max_c+1):
            if (c , r) in points:
                line += char1
            else:
                line += char2
        grid.append(line)
    map_view = "\n".join(grid)
    print(map_view)

# ===== Claude Functions =====

def cross_product(O, A, B):
    """
    Calculate the cross product of vectors OA and OB.
    Positive: B is on the left of OA
    Negative: B is on the right of OA
    Zero: O, A, B are collinear
    """
    return (A[0] - O[0]) * (B[1] - O[1]) - (A[1] - O[1]) * (B[0] - O[0])

def segments_share_edge(seg1, seg2):
    """Check if two segments are the same edge (same endpoints, possibly reversed)"""
    A, B = seg1
    C, D = seg2
    return (A == C and B == D) or (A == D and B == C)

def point_on_segment(P, A, B):
    """Check if point P lies on segment AB (including endpoints)"""
    # Check if P is collinear with A and B
    if abs(cross_product(A, B, P)) > 1e-9:
        return False

    # Check if P is within the bounding box of AB
    min_x = min(A[0], B[0])
    max_x = max(A[0], B[0])
    min_y = min(A[1], B[1])
    max_y = max(A[1], B[1])

    return min_x <= P[0] <= max_x and min_y <= P[1] <= max_y

def segments_overlap_collinear(seg1, seg2):
    """Check if two collinear segments overlap (not just touching at endpoints)"""
    A, B = seg1
    C, D = seg2

    # Check if they're collinear
    if abs(cross_product(A, B, C)) > 1e-9 or abs(cross_product(A, B, D)) > 1e-9:
        return False

    # If they share the complete edge, it's not considered an intersection
    if segments_share_edge(seg1, seg2):
        return False

    # Check if any endpoint of one segment is on the other segment (excluding shared endpoints)
    on_seg = []
    if C != A and C != B and point_on_segment(C, A, B):
        on_seg.append(True)
    if D != A and D != B and point_on_segment(D, A, B):
        on_seg.append(True)
    if A != C and A != D and point_on_segment(A, C, D):
        on_seg.append(True)
    if B != C and B != D and point_on_segment(B, C, D):
        on_seg.append(True)

    return len(on_seg) > 0

def segments_intersect(seg1, seg2):
    A, B = seg1
    C, D = seg2

    # If segments share the complete edge, not an intersection
    if segments_share_edge(seg1, seg2):
        return False

    # Check if segments share exactly one endpoint - this is allowed (loops touching)
    shared_endpoints = sum([A == C, A == D, B == C, B == D])
    if shared_endpoints == 1:
        return False

    # Calculate cross products to determine sides
    # For seg2 (line CD), check which side A and B are on
    cross_A = cross_product(C, D, A)
    cross_B = cross_product(C, D, B)

    # For seg1 (line AB), check which side C and D are on
    cross_C = cross_product(A, B, C)
    cross_D = cross_product(A, B, D)

    # Check if segments are collinear (all cross products are near zero)
    if abs(cross_A) < 1e-9 and abs(cross_B) < 1e-9:
        # Segments are collinear, check if they overlap
        return segments_overlap_collinear(seg1, seg2)

    # Segments intersect if endpoints are on opposite sides
    # A and B should be on opposite sides of CD (different signs)
    # C and D should be on opposite sides of AB (different signs)
    return cross_A * cross_B < 0 and cross_C * cross_D < 0

def loops_intersect(loop1, loop2):
    # Get all edges from both loops
    edges1 = []
    for i in range(len(loop1)):
        edges1.append((loop1[i], loop1[(i + 1) % len(loop1)]))
    
    edges2 = []
    for i in range(len(loop2)):
        edges2.append((loop2[i], loop2[(i + 1) % len(loop2)]))
    
    # Check if any edge from loop1 intersects with any edge from loop2
    for edge1 in edges1:
        for edge2 in edges2:
            if segments_intersect(edge1, edge2):
                return True
    
    return False

# ===== Main =====
# Initial
sum1 = 0
sum2 = 0

# Read file
#file_path = "/Users/boxu/Dev/aoc 2025/example_input"
file_path = "/Users/boxu/Dev/aoc 2025/day_9_input"

points = []
with open(file_path, 'r') as file:
    for line in file:
        c, r = map(int, line.strip().split(","))
        points.append((c, r))

#create_grid(points, "#", ".")
#plot_polygon(points)
max_a, key_max = max_area(points)
sum1 += max_a

areas = {}
for i in range(len(points)):
    for j in range(i + 1, len(points)):  # ensures no duplicates and no self-pairs
        p1 = points[i]
        p2 = points[j]
        c1, r1 = points[i]
        c2, r2 = points[j]
        p3 = (c1, r2)
        p4 = (c2, r1)
        rect = [p1, p3, p2, p4]     # rectangle vertices

        # valid_rect = True
        # first, check all corners
        if (not point_in_polygon(p3, points)) or (not point_in_polygon(p4, points)):
            # valid_rect = False
            continue
        # # then, check if any line segment is fully inside rectangle
        # if line_inside_rectangle(points, rect):
        #     valid_rect = False
        #     continue
        # # finally, only take valid rects into dictionary
        # if valid_rect:
        #     area = (abs(c1 - c2) + 1) * (abs(r1 - r2) + 1)
        #     areas[((c1,r1), (c2,r2))] = area

        if not loops_intersect(points, rect):
            area = (abs(c1 - c2) + 1) * (abs(r1 - r2) + 1)
            areas[((c1,r1), (c2,r2))] = area

key_max = max(areas, key=areas.get)
print(key_max)
sum2 += areas[key_max]

# Result
print("answer for part 1 is ", sum1)
print("answer for part 2 is ", sum2)
end_time = time.time()    # Record the end time
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.4f} seconds")