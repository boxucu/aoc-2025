# ===== Functions =====
# replace char in array
def replace_char_at_index(grid, r, c, new_char):
    line_new = grid[r][:c] + new_char + grid[r][c + 1:]
    grid_new = []
    for index in range (0, len(grid)):
        if index == r:
            grid_new.append(line_new)
        else:
            grid_new.append(grid[index])
    return grid_new

# replace all char
def replace_all(grid, char1, char2):
    rows = len(grid)
    cols = len(grid[0])
    new_grid = grid
    for r in range(0, rows):
        for c in range(0, cols):
            if new_grid[r][c] == char1:
                new_grid = replace_char_at_index(new_grid, r, c, char2)

    return new_grid

# print the char array
def print_array(grid):
    map_view = "\n".join(grid)
    print(map_view)

# ===== Main =====
# Initial
sum1 = 0
sum2 = 0

# Read file
# file_path = "/Users/boxu/Dev/aoc 2025/example_input"
file_path = "/Users/boxu/Dev/aoc 2025/day_7_input"

with open(file_path, 'r') as file:
    maxtrix = file.read()
grid = maxtrix.strip().split("\n")
rows = len(grid)
cols = len(grid[0])

rays = {grid[0].index("S"):1}
for r in range(1,rows):
    new_rays = {}
    for ray in rays:
        timeline = rays[ray]
        # passing through
        if grid[r][ray] == ".":
            if ray not in new_rays:
                new_rays[ray] = timeline
            else:
                new_rays[ray] += timeline
        # splitting
        elif grid[r][ray] == "^":
            sum1 += 1
            if ray - 1 > -1:
                if ray - 1 not in new_rays:
                    new_rays[ray - 1] = timeline
                else:
                    new_rays[ray - 1] += timeline
            if ray + 1 < cols:
                if ray + 1 not in new_rays:
                    new_rays[ray + 1] = timeline
                else:
                    new_rays[ray + 1] += timeline
    rays.clear()
    rays.update(new_rays)

    # for ray in rays:
    #     grid = replace_char_at_index(grid, r, ray, "|")
    # print_array(grid)

# sum the timelines in the end
sum2 = sum(rays.values())

# Result
print("answer for part 1 is ", sum1)
print("answer for part 2 is ", sum2)