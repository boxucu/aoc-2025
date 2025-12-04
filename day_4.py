# ===== Functions =====
# count @ neighbors
def count_adjacent_at(grid, r, c):
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    # Check all 8 directions
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue  # skip itself

            nr = r + dr
            nc = c + dc

            # Check boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == "@":
                    count += 1

    return count

# count not . neighbors
def count_adjacent_notdot(grid, r, c):
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    # Check all 8 directions
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue  # skip itself

            nr = r + dr
            nc = c + dc

            # Check boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] != ".":
                    count += 1

    return count

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

# find movable @
def mark_target(grid):
    count = 0
    rows = len(grid)
    cols = len(grid[0])
    new_grid = grid
    for r in range(0, rows):
        for c in range(0, cols):
            if new_grid[r][c] == "@":
                at_count = count_adjacent_notdot(new_grid, r, c)
                if at_count < 4:
                    count += 1
                    new_grid = replace_char_at_index(new_grid, r, c, "X")
    
    return count, new_grid

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

# ===== Main =====
# initial
sum1 = 0
sum2 = 0

# read file
file_path = "/Users/boxu/Dev/aoc 2025/day_4_input"
with open(file_path, 'r') as file:
    maxtrix = file.read()
grid = maxtrix.split("\n")
sum1, new_grid = mark_target(grid)
# map_view = "\n".join(new_grid)
# print(map_view)

end_move = False
while not end_move:
    count, new_grid = mark_target(grid)
    sum2 += count
    grid = replace_all(new_grid, "X", ".")
    if count == 0:
        end_move = True

# result
print("answer for part 1 is ", sum1)
print("answer for part 2 is ", sum2)